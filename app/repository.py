from __future__ import annotations

import re
import sqlite3
import unicodedata
from typing import Optional

from app.schemas import (
    AnalyticsResumoOut,
    LacunaOut,
    LogConsultaOut,
    PopCreate,
    PopMaisBuscadoOut,
    PopOut,
)

STOPWORDS_PT = {
    "a", "as", "o", "os", "um", "uma", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "por", "para", "com", "sem", "sob",
    "qual", "quais", "como", "fazer", "realizar", "preciso", "precisa",
    "quero", "busque", "buscar", "mostrar", "mostre", "sobre", "pop",
    "procedimento", "protocolo", "materiais", "material", "bandeja",
    "passo", "passos", "etapas", "execucao", "cuidados", "alerta",
    "alertas", "adulto", "paciente", "enfermaria", "plantao", "que", "e",
}


def normalizar_texto(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto or "")
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", sem_acento.lower()).strip()


def _quebrar_linhas(texto: str) -> list[str]:
    linhas = []
    for raw in (texto or "").splitlines():
        item = re.sub(r"^\s*(?:[-•*]|\d+[\.\)])\s*", "", raw.strip())
        if item:
            linhas.append(item)
    return linhas


def row_to_pop(row: sqlite3.Row) -> PopOut:
    data = dict(row)
    return PopOut(
        **data,
        materiais_lista=_quebrar_linhas(data["materiais"]),
        passos_lista=_quebrar_linhas(data["passos_execucao"]),
        alertas_lista=_quebrar_linhas(data["alertas_seguranca"]),
    )


def extrair_termo_lacuna(pergunta: str) -> str:
    norm = normalizar_texto(pergunta)
    codigo_match = re.search(r"\bpop[\.\-\s]?[a-z]{2,6}[\.\-\s]?\d{2,4}\b", norm)
    if codigo_match:
        return codigo_match.group(0).upper().replace(" ", ".")
    tokens = [
        tok for tok in re.findall(r"[a-z0-9\-]{3,}", norm)
        if tok not in STOPWORDS_PT
    ]
    if not tokens:
        return norm[:80] or "procedimento nao especificado"
    return " ".join(tokens[:5])


def buscar_pops_ativos(
    conn: sqlite3.Connection,
    termo_busca: str,
    setor: Optional[str] = None,
) -> list[PopOut]:
    """Executa consulta determinística na tabela pops filtrando estritamente status = 'ATIVO' (RN02)."""
    rows = conn.execute(
        "SELECT * FROM pops WHERE status = 'ATIVO' ORDER BY codigo ASC"
    ).fetchall()

    q_norm = normalizar_texto(termo_busca)
    if not q_norm:
        return []

    codigo_direto = re.sub(r"[^a-z0-9]", "", q_norm)
    tokens = [
        t for t in re.findall(r"[a-z0-9]{2,}", q_norm)
        if t not in STOPWORDS_PT
    ]
    if not tokens and len(q_norm) >= 2:
        tokens = re.findall(r"[a-z0-9]{2,}", q_norm)

    setor_norm = normalizar_texto(setor) if setor else ""
    scored: list[tuple[int, PopOut]] = []

    for row in rows:
        codigo_norm = re.sub(r"[^a-z0-9]", "", normalizar_texto(row["codigo"]))
        titulo_norm = normalizar_texto(row["titulo"])
        chaves_norm = normalizar_texto(row["palavras_chave"])
        setor_row_norm = normalizar_texto(row["setor"])
        corpo_norm = normalizar_texto(f"{row['objetivo']} {row['materiais']}")

        score = 0
        if codigo_direto and (codigo_direto == codigo_norm or codigo_norm in codigo_direto):
            score += 120

        if q_norm in titulo_norm or q_norm in chaves_norm:
            score += 60

        matched_tokens = 0
        for tok in tokens:
            tok_clean = re.sub(r"[^a-z0-9]", "", tok)
            if tok_clean and tok_clean == codigo_norm:
                score += 100
                matched_tokens += 1
            elif tok in titulo_norm:
                score += 25
                matched_tokens += 1
            elif tok in chaves_norm:
                score += 20
                matched_tokens += 1
            elif len(tok) >= 4 and tok in corpo_norm:
                score += 6
                matched_tokens += 1

        if tokens and matched_tokens == 0 and score == 0:
            continue

        # Previne falso-positivo clínico por palavra isolada genérica (ex.: "agulha")
        min_tokens = 1 if len(tokens) <= 2 else max(2, (len(tokens) + 1) // 2)
        if score < 60 and matched_tokens < min_tokens:
            continue

        if setor_norm and setor_norm in setor_row_norm:
            score += 8

        if score >= 20:
            scored.append((score, row_to_pop(row)))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in scored]


def listar_pops(
    conn: sqlite3.Connection,
    termo: Optional[str] = None,
    setor: Optional[str] = None,
    incluir_inativos: bool = False,
) -> list[PopOut]:
    sql = "SELECT * FROM pops"
    clauses = []
    if not incluir_inativos:
        clauses.append("status = 'ATIVO'")
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY CASE WHEN status = 'ATIVO' THEN 0 ELSE 1 END, codigo ASC"

    rows = conn.execute(sql).fetchall()
    pops = [row_to_pop(r) for r in rows]

    if setor:
        s_norm = normalizar_texto(setor)
        pops = [p for p in pops if s_norm in normalizar_texto(p.setor)]

    if termo:
        t_norm = normalizar_texto(termo)
        pops = [
            p
            for p in pops
            if t_norm in normalizar_texto(p.codigo)
            or t_norm in normalizar_texto(p.titulo)
            or t_norm in normalizar_texto(p.palavras_chave)
            or t_norm in normalizar_texto(p.setor)
        ]

    return pops


def obter_pop_por_codigo(conn: sqlite3.Connection, codigo: str) -> Optional[PopOut]:
    alvo = codigo.strip().upper()
    row = conn.execute(
        "SELECT * FROM pops WHERE UPPER(codigo) = ?",
        (alvo,),
    ).fetchone()
    return row_to_pop(row) if row else None


def criar_pop(conn: sqlite3.Connection, dados: PopCreate) -> PopOut:
    existente = obter_pop_por_codigo(conn, dados.codigo)
    if existente:
        raise ValueError(f"Já existe um POP cadastrado com o código {dados.codigo}.")

    cur = conn.execute(
        """
        INSERT INTO pops (
            codigo, titulo, setor, versao, objetivo,
            materiais, passos_execucao, alertas_seguranca,
            palavras_chave, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados.codigo,
            dados.titulo.strip(),
            dados.setor.strip(),
            dados.versao.strip(),
            dados.objetivo.strip(),
            dados.materiais.strip(),
            dados.passos_execucao.strip(),
            dados.alertas_seguranca.strip(),
            dados.palavras_chave.strip(),
            dados.status,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM pops WHERE id = ?", (cur.lastrowid,)).fetchone()
    return row_to_pop(row)


def registrar_lacuna(
    conn: sqlite3.Connection,
    termo_buscado: str,
    pergunta_original: str,
) -> tuple[str, int]:
    termo_limpo = normalizar_texto(termo_buscado)[:150] or extrair_termo_lacuna(pergunta_original)
    conn.execute(
        """
        INSERT INTO lacunas_protocolos (termo_buscado, pergunta_exemplo, quantidade_buscas, ultima_ocorrencia)
        VALUES (?, ?, 1, CURRENT_TIMESTAMP)
        ON CONFLICT(termo_buscado) DO UPDATE SET
            quantidade_buscas = lacunas_protocolos.quantidade_buscas + 1,
            pergunta_exemplo = excluded.pergunta_exemplo,
            ultima_ocorrencia = CURRENT_TIMESTAMP
        """,
        (termo_limpo, pergunta_original.strip()),
    )
    conn.commit()
    row = conn.execute(
        "SELECT termo_buscado, quantidade_buscas FROM lacunas_protocolos WHERE termo_buscado = ?",
        (termo_limpo,),
    ).fetchone()
    return row["termo_buscado"], int(row["quantidade_buscas"])


def registrar_log_consulta(
    conn: sqlite3.Connection,
    pergunta: str,
    codigo_pop_retornado: Optional[str],
    foi_encontrado: bool,
    latencia_ms: int,
) -> None:
    conn.execute(
        """
        INSERT INTO logs_consultas (pergunta, codigo_pop_retornado, foi_encontrado, latencia_ms)
        VALUES (?, ?, ?, ?)
        """,
        (pergunta, codigo_pop_retornado, 1 if foi_encontrado else 0, max(1, int(latencia_ms))),
    )
    conn.commit()


def obter_resumo_analytics(conn: sqlite3.Connection) -> AnalyticsResumoOut:
    totais = conn.execute(
        """
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(CASE WHEN foi_encontrado = 1 THEN 1 ELSE 0 END), 0) AS cobertas,
            COALESCE(AVG(latencia_ms), 0) AS latencia_media
        FROM logs_consultas
        """
    ).fetchone()

    total_consultas = int(totais["total"] or 0)
    cobertas = int(totais["cobertas"] or 0)
    taxa = round((cobertas / total_consultas) * 100, 1) if total_consultas > 0 else 100.0
    latencia_media = round(float(totais["latencia_media"] or 0.0), 1)

    status_counts = conn.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN status = 'ATIVO' THEN 1 ELSE 0 END), 0) AS ativos,
            COALESCE(SUM(CASE WHEN status != 'ATIVO' THEN 1 ELSE 0 END), 0) AS revisao
        FROM pops
        """
    ).fetchone()

    ranking_pops_rows = conn.execute(
        """
        SELECT
            p.codigo,
            p.titulo,
            p.setor,
            COUNT(l.id) AS total_consultas
        FROM pops p
        JOIN logs_consultas l ON l.codigo_pop_retornado = p.codigo
        WHERE l.foi_encontrado = 1
        GROUP BY p.codigo, p.titulo, p.setor
        ORDER BY total_consultas DESC, p.codigo ASC
        LIMIT 5
        """
    ).fetchall()

    lacunas_rows = conn.execute(
        """
        SELECT id, termo_buscado, pergunta_exemplo, quantidade_buscas, ultima_ocorrencia
        FROM lacunas_protocolos
        ORDER BY quantidade_buscas DESC, ultima_ocorrencia DESC
        LIMIT 10
        """
    ).fetchall()

    total_lacunas = int(
        conn.execute("SELECT COUNT(*) FROM lacunas_protocolos").fetchone()[0]
    )

    logs_rows = conn.execute(
        """
        SELECT id, pergunta, codigo_pop_retornado, foi_encontrado, latencia_ms, criado_em
        FROM logs_consultas
        ORDER BY id DESC
        LIMIT 12
        """
    ).fetchall()

    return AnalyticsResumoOut(
        total_consultas=total_consultas,
        consultas_com_cobertura=cobertas,
        total_lacunas_distintas=total_lacunas,
        taxa_cobertura_percentual=taxa,
        latencia_media_ms=latencia_media,
        total_pops_ativos=int(status_counts["ativos"] or 0),
        total_pops_revisao=int(status_counts["revisao"] or 0),
        pops_mais_buscados=[PopMaisBuscadoOut(**dict(r)) for r in ranking_pops_rows],
        lacunas_prioritarias=[LacunaOut(**dict(r)) for r in lacunas_rows],
        ultimos_logs=[
            LogConsultaOut(
                id=r["id"],
                pergunta=r["pergunta"],
                codigo_pop_retornado=r["codigo_pop_retornado"],
                foi_encontrado=bool(r["foi_encontrado"]),
                latencia_ms=r["latencia_ms"],
                criado_em=str(r["criado_em"]),
            )
            for r in logs_rows
        ],
    )
