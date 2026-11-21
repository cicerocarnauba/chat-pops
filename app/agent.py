from __future__ import annotations

import json
import os
import re
import sqlite3
import time
from typing import Any, Optional

from app.repository import (
    buscar_pops_ativos,
    extrair_termo_lacuna,
    obter_pop_por_codigo,
    registrar_lacuna,
    registrar_log_consulta,
)
from app.schemas import ChatResponse, PopOut

MODEL_ID = "gemini-4-hydrogen"

SYSTEM_INSTRUCTION = (
    "Você é o chat-pops, Copiloto Institucional de Procedimentos Operacionais Padrão (POPs) "
    "do Hospital Universitário (HU-UFC / PET Saúde Digital). "
    "REGRAS INVIOLÁVEIS:\n"
    "1. Sempre chame primeiro a ferramenta `buscar_pops_sql` para consultar a base oficial.\n"
    "2. Se `buscar_pops_sql` retornar um POP ativo, responda em português claro e objetivo usando "
    "EXCLUSIVAMENTE os dados retornados do banco, citando obrigatoriamente o código e a versão.\n"
    "3. Se `buscar_pops_sql` retornar lista vazia, chame obrigatoriamente `registrar_lacuna_sql` "
    "e recuse gerar qualquer conduta, lista de materiais ou passo a passo por conta própria.\n"
    "4. Nunca solicite nem repita dados pessoais de pacientes (LGPD)."
)

GEMINI_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "name": "buscar_pops_sql",
        "description": "Busca POPs homologados com status ATIVO no banco SQL por código, título ou palavras-chave.",
        "parameters": {
            "type": "object",
            "properties": {
                "termo_busca": {
                    "type": "string",
                    "description": "Código oficial (ex.: POP.ENF.001) ou procedimento clínico buscado.",
                }
            },
            "required": ["termo_busca"],
        },
    },
    {
        "type": "function",
        "name": "registrar_lacuna_sql",
        "description": "Registra demanda de protocolo inexistente na fila da CCIH/gestão hospitalar.",
        "parameters": {
            "type": "object",
            "properties": {
                "termo_buscado": {
                    "type": "string",
                    "description": "Nome normalizado do procedimento não localizado.",
                },
                "pergunta_original": {
                    "type": "string",
                    "description": "Pergunta feita pelo profissional.",
                },
            },
            "required": ["termo_buscado", "pergunta_original"],
        },
    },
]

PADROES_PII = [
    (re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "[CPF REMOVIDO - LGPD]"),
    (re.compile(r"\b(?:prontu[aá]rio|leito\s+do\s+sr|paciente\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)", re.IGNORECASE), "[DADO PESSOAL OMITIDO - LGPD]"),
]


def sanitizar_pii_lgpd(pergunta: str) -> tuple[str, Optional[str]]:
    texto = pergunta.strip()
    alterado = False
    for regex, substituto in PADROES_PII:
        novo_texto, n = regex.subn(substituto, texto)
        if n > 0:
            texto = novo_texto
            alterado = True
    aviso = (
        "Conformidade LGPD (RNF03): Identificadores pessoais/clínicos foram omitidos automaticamente antes do processamento e registro."
        if alterado
        else None
    )
    return texto, aviso


def formatar_resposta_deterministica(pop: PopOut) -> str:
    return (
        f"Protocolo oficial localizado: **{pop.codigo} — {pop.titulo}** "
        f"({pop.setor} · Versão `{pop.versao}`).\n\n"
        f"**Objetivo:** {pop.objetivo}\n\n"
        f"Os **{len(pop.materiais_lista)} itens de bandeja**, as **{len(pop.passos_lista)} etapas homologadas** "
        f"e os **alertas críticos de biossegurança** estão abertos na folha normativa ao lado para conferência imediata."
    )


def formatar_recusa_segura(termo: str, total_buscas: int, em_revisao_codigo: Optional[str] = None) -> str:
    nota_revisao = (
        f" Nota institucional: o documento `{em_revisao_codigo}` encontra-se com status `EM_REVISAO` (suspenso para orientação clínica conforme RN02)."
        if em_revisao_codigo
        else ""
    )
    return (
        f"**Recusa Segura (RN01/RF03):** Não há Procedimento Operacional Padrão com status `ATIVO` "
        f"homologado na base oficial para **\"{termo}\"**.\n\n"
        f"Por segurança assistencial e prevenção de alucinações, o `chat-pops` não gera condutas livres fora do banco SQL.{nota_revisao} "
        f"Sua demanda foi registrada automaticamente para a CCIH / Divisão de Enfermagem "
        f"(total acumulado: **{total_buscas} solicitações**)."
    )


def _checar_pop_em_revisao(conn: sqlite3.Connection, pergunta: str) -> Optional[str]:
    rows = conn.execute("SELECT codigo, titulo, palavras_chave FROM pops WHERE status != 'ATIVO'").fetchall()
    from app.repository import normalizar_texto

    q_norm = normalizar_texto(pergunta)
    for r in rows:
        if (
            normalizar_texto(r["codigo"]) in q_norm
            or any(
                chave.strip() and chave.strip() in q_norm
                for chave in normalizar_texto(r["palavras_chave"]).split(",")
            )
        ):
            return r["codigo"]
    return None


def _executar_com_gemini(
    conn: sqlite3.Connection,
    pergunta_limpa: str,
    setor_usuario: Optional[str],
    api_key: str,
    llm_client: Any = None,
) -> tuple[str, Optional[PopOut], Optional[tuple[str, int]]]:
    if llm_client is None:
        from google import genai

        llm_client = genai.Client(api_key=api_key)

    pop_encontrado: Optional[PopOut] = None
    lacuna_info: Optional[tuple[str, int]] = None

    prompt_entrada = (
        f"[Setor do profissional: {setor_usuario}] {pergunta_limpa}"
        if setor_usuario
        else pergunta_limpa
    )

    interaction = llm_client.interactions.create(
        model=MODEL_ID,
        input=prompt_entrada,
        system_instruction=SYSTEM_INSTRUCTION,
        tools=GEMINI_TOOLS,
        store=False,
    )

    # Executa até 3 rodadas de chamadas de função determinísticas
    for _ in range(3):
        steps = getattr(interaction, "steps", None) or []
        function_calls = [s for s in steps if getattr(s, "type", None) == "function_call"]
        if not function_calls:
            break

        tool_results_input = []
        for call in function_calls:
            args = getattr(call, "arguments", None) or {}
            if isinstance(args, str):
                args = json.loads(args)

            if call.name == "buscar_pops_sql":
                termo = str(args.get("termo_busca") or pergunta_limpa)
                encontrados = buscar_pops_ativos(conn, termo, setor=setor_usuario)
                if encontrados:
                    pop_encontrado = encontrados[0]
                    payload = {
                        "encontrado": True,
                        "pop": pop_encontrado.model_dump(),
                    }
                else:
                    payload = {"encontrado": False, "pops": []}
            elif call.name == "registrar_lacuna_sql":
                termo_lac = str(args.get("termo_buscado") or extrair_termo_lacuna(pergunta_limpa))
                lacuna_info = registrar_lacuna(conn, termo_lac, pergunta_limpa)
                payload = {
                    "registrado": True,
                    "termo_buscado": lacuna_info[0],
                    "quantidade_buscas": lacuna_info[1],
                }
            else:
                payload = {"erro": f"Ferramenta desconhecida: {call.name}"}

            tool_results_input.append(
                {
                    "type": "function_result",
                    "call_id": call.id,
                    "name": call.name,
                    "result": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
                }
            )

        # Se store=False desabilita previous_interaction_id em chamadas reais sem estado,
        # sintetizamos resposta fundamentada com os dados SQL já validados ou continuamos quando suportado.
        if getattr(interaction, "id", None):
            try:
                interaction = llm_client.interactions.create(
                    model=MODEL_ID,
                    previous_interaction_id=interaction.id,
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=GEMINI_TOOLS,
                    input=tool_results_input,
                )
            except Exception:
                break
        else:
            break

    texto_modelo = (getattr(interaction, "output_text", None) or "").strip()

    # Garantia determinística das Regras de Negócio RN01, RN02, RN03 e RNF01:
    if pop_encontrado is None:
        diretos = buscar_pops_ativos(conn, pergunta_limpa, setor=setor_usuario)
        if diretos:
            pop_encontrado = diretos[0]

    if pop_encontrado is not None:
        if not texto_modelo or pop_encontrado.codigo not in texto_modelo:
            texto_modelo = formatar_resposta_deterministica(pop_encontrado)
        elif pop_encontrado.versao not in texto_modelo:
            texto_modelo = f"{texto_modelo}\n\n*(Referência oficial: {pop_encontrado.codigo} · {pop_encontrado.versao})*"
        return texto_modelo, pop_encontrado, None

    if lacuna_info is None:
        termo_auto = extrair_termo_lacuna(pergunta_limpa)
        lacuna_info = registrar_lacuna(conn, termo_auto, pergunta_limpa)

    revisao_cod = _checar_pop_em_revisao(conn, pergunta_limpa)
    texto_seguro = formatar_recusa_segura(lacuna_info[0], lacuna_info[1], revisao_cod)
    return texto_seguro, None, lacuna_info


def processar_consulta_chat(
    conn: sqlite3.Connection,
    pergunta: str,
    setor_usuario: Optional[str] = None,
    api_key: Optional[str] = None,
    llm_client: Any = None,
) -> ChatResponse:
    inicio = time.perf_counter()
    pergunta_limpa, aviso_lgpd = sanitizar_pii_lgpd(pergunta)

    chave_efetiva = (api_key or os.getenv("GEMINI_API_KEY") or "").strip()
    modo: str = "fallback_deterministico"
    pop_citado: Optional[PopOut] = None
    lacuna_info: Optional[tuple[str, int]] = None

    if chave_efetiva or llm_client is not None:
        try:
            resposta_txt, pop_citado, lacuna_info = _executar_com_gemini(
                conn=conn,
                pergunta_limpa=pergunta_limpa,
                setor_usuario=setor_usuario,
                api_key=chave_efetiva or "mock-key",
                llm_client=llm_client,
            )
            modo = "gemini_interactions"
        except Exception:
            modo = "fallback_deterministico"
            resposta_txt = ""
    else:
        resposta_txt = ""

    if modo == "fallback_deterministico":
        encontrados = buscar_pops_ativos(conn, pergunta_limpa, setor=setor_usuario)
        if encontrados:
            pop_citado = encontrados[0]
            resposta_txt = formatar_resposta_deterministica(pop_citado)
        else:
            termo_lac = extrair_termo_lacuna(pergunta_limpa)
            lacuna_info = registrar_lacuna(conn, termo_lac, pergunta_limpa)
            revisao_cod = _checar_pop_em_revisao(conn, pergunta_limpa)
            resposta_txt = formatar_recusa_segura(lacuna_info[0], lacuna_info[1], revisao_cod)

    latencia_ms = max(1, int((time.perf_counter() - inicio) * 1000))
    foi_encontrado = pop_citado is not None

    registrar_log_consulta(
        conn=conn,
        pergunta=pergunta_limpa,
        codigo_pop_retornado=pop_citado.codigo if pop_citado else None,
        foi_encontrado=foi_encontrado,
        latencia_ms=latencia_ms,
    )

    return ChatResponse(
        resposta=resposta_txt,
        foi_encontrado=foi_encontrado,
        modo_execucao=modo,  # type: ignore[arg-type]
        latencia_ms=latencia_ms,
        aviso_lgpd=aviso_lgpd,
        pop_citado=pop_citado,
        lacuna_registrada=lacuna_info[0] if lacuna_info else None,
        total_buscas_lacuna=lacuna_info[1] if lacuna_info else None,
    )
