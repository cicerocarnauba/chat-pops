from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.agent import processar_consulta_chat
from app.database import get_connection, init_db
from app.main import app


@pytest.fixture()
def test_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    db_file = tmp_path / "test_chat_pops.db"
    monkeypatch.setenv("CHAT_POPS_DB_PATH", str(db_file))
    init_db(db_file, seed=True)
    return db_file


@pytest.fixture()
def client(test_db: Path) -> TestClient:
    with TestClient(app) as c:
        yield c


def test_seed_cinco_pops_ativos_e_um_em_revisao(client: TestClient):
    res_ativos = client.get("/api/v1/pops")
    assert res_ativos.status_code == 200
    ativos = res_ativos.json()
    assert len(ativos) == 5
    codigos = {p["codigo"] for p in ativos}
    assert codigos == {
        "POP.ENF.001",
        "POP.CCIH.002",
        "POP.ENF.003",
        "POP.FARM.004",
        "POP.ENF.005",
    }

    res_todos = client.get("/api/v1/pops?incluir_inativos=true")
    assert res_todos.status_code == 200
    assert len(res_todos.json()) == 6


def test_consulta_chat_positiva_retorna_pop_oficial_e_cita_codigo_versao(client: TestClient):
    res = client.post(
        "/api/v1/chat",
        json={"pergunta": "Quais materiais preciso para punção venosa periférica?"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["foi_encontrado"] is True
    assert body["modo_execucao"] == "fallback_deterministico"
    assert body["pop_citado"]["codigo"] == "POP.ENF.001"
    assert "POP.ENF.001" in body["resposta"]
    assert "v3.2" in body["resposta"]
    assert len(body["pop_citado"]["materiais_lista"]) >= 5


def test_rn02_pop_em_revisao_nao_orienta_e_registra_lacuna(client: TestClient):
    # POP.ENF.006 (Port-a-Cath) está com status EM_REVISAO no seed
    res = client.post(
        "/api/v1/chat",
        json={"pergunta": "Como puncionar e heparinizar um Port-a-Cath com agulha Huber?"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["foi_encontrado"] is False
    assert body["pop_citado"] is None
    assert "Recusa Segura" in body["resposta"]
    assert "POP.ENF.006" in body["resposta"]
    assert body["lacuna_registrada"] is not None
    assert body["total_buscas_lacuna"] >= 1


def test_rf03_lacuna_incrementa_contador_e_aparece_no_analytics(client: TestClient):
    antes = client.get("/api/v1/analytics/resumo").json()
    pergunta = "Qual o protocolo para passagem de balão intra-aórtico na UTI?"
    r1 = client.post("/api/v1/chat", json={"pergunta": pergunta}).json()
    r2 = client.post("/api/v1/chat", json={"pergunta": pergunta}).json()

    assert r1["foi_encontrado"] is False
    assert r2["total_buscas_lacuna"] == r1["total_buscas_lacuna"] + 1

    resumo = client.get("/api/v1/analytics/resumo").json()
    assert resumo["total_consultas"] == antes["total_consultas"] + 2
    assert resumo["consultas_com_cobertura"] == antes["consultas_com_cobertura"]
    termos = [l["termo_buscado"] for l in resumo["lacunas_prioritarias"]]
    assert r1["lacuna_registrada"] in termos


def test_rf05_cadastro_novo_pop_e_consulta_imediata(client: TestClient):
    novo_pop = {
        "codigo": "POP.CCIH.010",
        "titulo": "Coleta Asséptica de Hemocultura Pareada",
        "setor": "CCIH",
        "versao": "v1.0 - 2026",
        "objetivo": "Padronizar coleta pareada de sangue periférico para diagnóstico de bacteremia.",
        "materiais": "Luvas estéreis\nClorexidina alcoólica 0,5%\n2 pares de frascos de hemocultura",
        "passos_execucao": "1. Desinfetar septo dos frascos com álcool 70%.\n2. Antissepsia da pele por 30s e punção de dois sítios distintos.",
        "alertas_seguranca": "Coletar antes da primeira dose do antibiótico; não refrigerar frascos.",
        "palavras_chave": "hemocultura, bacteremia, sepse, coleta sangue",
        "status": "ATIVO",
    }
    post_res = client.post("/api/v1/pops", json=novo_pop)
    assert post_res.status_code == 201

    # Duplicidade deve retornar 409 Conflict
    dup_res = client.post("/api/v1/pops", json=novo_pop)
    assert dup_res.status_code == 409

    # Agora o chat deve localizar o novo POP imediatamente
    chat_res = client.post(
        "/api/v1/chat",
        json={"pergunta": "Como coletar hemocultura pareada para sepse?"},
    )
    assert chat_res.status_code == 200
    assert chat_res.json()["foi_encontrado"] is True
    assert chat_res.json()["pop_citado"]["codigo"] == "POP.CCIH.010"


def test_rnf03_sanitizacao_lgpd_remove_cpf_antes_de_logar(client: TestClient):
    res = client.post(
        "/api/v1/chat",
        json={"pergunta": "Punção venosa para paciente CPF 123.456.789-00 no leito 4"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["aviso_lgpd"] is not None

    resumo = client.get("/api/v1/analytics/resumo").json()
    ultima_pergunta = resumo["ultimos_logs"][0]["pergunta"]
    assert "123.456.789-00" not in ultima_pergunta
    assert "[CPF REMOVIDO - LGPD]" in ultima_pergunta


def test_orquestracao_gemini_interactions_com_stub_desacoplado(test_db: Path):
    @dataclass
    class FakeStep:
        type: str
        id: str = ""
        name: str = ""
        arguments: dict[str, Any] | None = None

    @dataclass
    class FakeInteraction:
        id: str
        steps: list[FakeStep]
        output_text: str

    class FakeInteractionsResource:
        def __init__(self):
            self.calls = 0

        def create(self, **kwargs):
            self.calls += 1
            if self.calls == 1:
                return FakeInteraction(
                    id="int_mock_01",
                    steps=[
                        FakeStep(
                            type="function_call",
                            id="call_01",
                            name="buscar_pops_sql",
                            arguments={"termo_busca": "POP.ENF.003"},
                        )
                    ],
                    output_text="",
                )
            return FakeInteraction(
                id="int_mock_02",
                steps=[],
                output_text=(
                    "Conforme o protocolo oficial POP.ENF.003 (v2.5 - 2026 [DEMO]), "
                    "utilize água destilada estéril no balonete e mantenha sistema fechado."
                ),
            )

    class FakeGenAIClient:
        def __init__(self):
            self.interactions = FakeInteractionsResource()

    with get_connection(test_db) as conn:
        fake_client = FakeGenAIClient()
        resp = processar_consulta_chat(
            conn=conn,
            pergunta="Posso usar soro fisiológico no balonete da sonda vesical?",
            llm_client=fake_client,
        )
        assert resp.modo_execucao == "gemini_interactions"
        assert resp.foi_encontrado is True
        assert resp.pop_citado is not None
        assert resp.pop_citado.codigo == "POP.ENF.003"
        assert "POP.ENF.003" in resp.resposta
        assert fake_client.interactions.calls == 2


def test_spa_servida_na_raiz(client: TestClient):
    res = client.get("/")
    assert res.status_code == 200
    assert "chat-pops" in res.text
