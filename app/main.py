from __future__ import annotations

import json
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, File, Header, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.agent import processar_consulta_chat
from app.database import get_connection, init_db
from app.repository import (
    criar_pop,
    listar_pops,
    obter_pop_por_codigo,
    obter_resumo_analytics,
)
from app.schemas import AnalyticsResumoOut, ChatRequest, ChatResponse, PopCreate, PopOut

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db(seed=True)
    yield


app = FastAPI(
    title="chat-pops API — Copiloto de POPs Hospitalares",
    description="API B2E auditável para consulta estruturada de Procedimentos Operacionais Padrão (HU-UFC / PET Saúde Digital).",
    version="1.0.0",
    lifespan=lifespan,
)


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "servico": "chat-pops", "versao": "1.0.0"}


@app.post("/api/v1/chat", response_model=ChatResponse)
def consultar_chat(
    payload: ChatRequest,
    x_gemini_api_key: Optional[str] = Header(default=None),
    conn=Depends(get_db),
):
    return processar_consulta_chat(
        conn=conn,
        pergunta=payload.pergunta,
        setor_usuario=payload.setor_usuario,
        api_key=x_gemini_api_key,
    )


@app.get("/api/v1/pops", response_model=list[PopOut])
def listar_catalogo_pops(
    termo: Optional[str] = Query(default=None),
    setor: Optional[str] = Query(default=None),
    incluir_inativos: bool = Query(default=False),
    conn=Depends(get_db),
):
    return listar_pops(conn, termo=termo, setor=setor, incluir_inativos=incluir_inativos)


@app.get("/api/v1/pops/{codigo}", response_model=PopOut)
def buscar_pop_codigo(codigo: str, conn=Depends(get_db)):
    pop = obter_pop_por_codigo(conn, codigo)
    if not pop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"POP '{codigo.upper()}' não encontrado na base oficial.",
        )
    return pop


@app.post("/api/v1/pops", response_model=PopOut, status_code=status.HTTP_201_CREATED)
def cadastrar_novo_pop(payload: PopCreate, conn=Depends(get_db)):
    try:
        return criar_pop(conn, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@app.post("/api/v1/pops/extrair-arquivo")
async def extrair_rascunho_arquivo(arquivo: UploadFile = File(...)):
    """Auxilia a tela de importação convertendo arquivos .json, .md ou .txt em campos estruturados."""
    conteudo_bytes = await arquivo.read()
    if len(conteudo_bytes) > 512_000:
        raise HTTPException(status_code=413, detail="Arquivo excede o limite de 500 KB.")

    nome = (arquivo.filename or "protocolo.txt").lower()
    texto = conteudo_bytes.decode("utf-8", errors="replace").strip()

    if nome.endswith(".json"):
        try:
            dados = json.loads(texto)
            if isinstance(dados, list) and dados:
                dados = dados[0]
            if not isinstance(dados, dict):
                raise ValueError("JSON inválido")
            return dados
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Não foi possível interpretar o arquivo JSON.") from exc

    def capturar_secao(rotulos: list[str]) -> str:
        padrao = "|".join(rotulos)
        m = re.search(
            rf"(?:^|\n)#*\s*(?:{padrao})\s*:?\s*\n(.*?)(?=\n#+\s|\n[A-ZÁÉÍÓÚÇ][A-Za-zÁ-ú\s/]+:\s*\n|\Z)",
            texto,
            flags=re.IGNORECASE | re.DOTALL,
        )
        return m.group(1).strip() if m else ""

    codigo_m = re.search(r"\b(POP\.[A-Z]{2,8}\.\d{2,4})\b", texto, re.IGNORECASE)
    linhas = [ln.strip("# ").strip() for ln in texto.splitlines() if ln.strip()]

    return {
        "codigo": codigo_m.group(1).upper() if codigo_m else "POP.ENF.007",
        "titulo": linhas[0][:180] if linhas else "Novo Procedimento Importado",
        "setor": "Divisão de Enfermagem",
        "versao": "v1.0 - 2026",
        "objetivo": capturar_secao(["objetivo", "finalidade"]) or "Padronizar a execução segura do procedimento conforme diretriz institucional.",
        "materiais": capturar_secao(["materiais", "bandeja", "insumos"]) or "",
        "passos_execucao": capturar_secao(["passos", "execução", "execucao", "procedimento", "etapas"]) or texto[:1200],
        "alertas_seguranca": capturar_secao(["alertas", "biossegurança", "biosseguranca", "cuidados", "pontos críticos"]) or "",
        "palavras_chave": "",
        "status": "ATIVO",
    }


@app.get("/api/v1/analytics/resumo", response_model=AnalyticsResumoOut)
def resumo_analytics(conn=Depends(get_db)):
    return obter_resumo_analytics(conn)


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def serve_spa():
    return FileResponse(str(STATIC_DIR / "index.html"))
