from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


StatusPop = Literal["ATIVO", "EM_REVISAO"]


class PopBase(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=30, examples=["POP.ENF.001"])
    titulo: str = Field(..., min_length=5, max_length=200)
    setor: str = Field(..., min_length=2, max_length=100)
    versao: str = Field(..., min_length=2, max_length=40, examples=["v3.2 - 2026 [DEMO]"])
    objetivo: str = Field(..., min_length=10)
    materiais: str = Field(..., min_length=5)
    passos_execucao: str = Field(..., min_length=10)
    alertas_seguranca: str = Field(..., min_length=5)
    palavras_chave: str = Field(..., min_length=3, max_length=255)
    status: StatusPop = Field(default="ATIVO")

    @field_validator("codigo")
    @classmethod
    def normalizar_codigo(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if not cleaned:
            raise ValueError("O código do POP é obrigatório.")
        return cleaned


class PopCreate(PopBase):
    pass


class PopOut(PopBase):
    id: int
    materiais_lista: list[str] = Field(default_factory=list)
    passos_lista: list[str] = Field(default_factory=list)
    alertas_lista: list[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    pergunta: str = Field(..., min_length=2, max_length=600)
    setor_usuario: Optional[str] = Field(default=None, max_length=100)


class ChatResponse(BaseModel):
    resposta: str
    foi_encontrado: bool
    modo_execucao: Literal["gemini_interactions", "fallback_deterministico"]
    latencia_ms: int
    aviso_lgpd: Optional[str] = None
    pop_citado: Optional[PopOut] = None
    lacuna_registrada: Optional[str] = None
    total_buscas_lacuna: Optional[int] = None


class LacunaOut(BaseModel):
    id: int
    termo_buscado: str
    pergunta_exemplo: str
    quantidade_buscas: int
    ultima_ocorrencia: str


class LogConsultaOut(BaseModel):
    id: int
    pergunta: str
    codigo_pop_retornado: Optional[str]
    foi_encontrado: bool
    latencia_ms: int
    criado_em: str


class PopMaisBuscadoOut(BaseModel):
    codigo: str
    titulo: str
    setor: str
    total_consultas: int


class AnalyticsResumoOut(BaseModel):
    total_consultas: int
    consultas_com_cobertura: int
    total_lacunas_distintas: int
    taxa_cobertura_percentual: float
    latencia_media_ms: float
    total_pops_ativos: int
    total_pops_revisao: int
    pops_mais_buscados: list[PopMaisBuscadoOut]
    lacunas_prioritarias: list[LacunaOut]
    ultimos_logs: list[LogConsultaOut]
