from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "chat_pops.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS pops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(30) UNIQUE NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    setor VARCHAR(100) NOT NULL,
    versao VARCHAR(40) NOT NULL,
    objetivo TEXT NOT NULL,
    materiais TEXT NOT NULL,
    passos_execucao TEXT NOT NULL,
    alertas_seguranca TEXT NOT NULL,
    palavras_chave VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ATIVO'
);

CREATE TABLE IF NOT EXISTS lacunas_protocolos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    termo_buscado VARCHAR(150) UNIQUE NOT NULL,
    pergunta_exemplo TEXT NOT NULL,
    quantidade_buscas INTEGER NOT NULL DEFAULT 1,
    ultima_ocorrencia TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs_consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pergunta TEXT NOT NULL,
    codigo_pop_retornado VARCHAR(30) NULL,
    foi_encontrado BOOLEAN NOT NULL,
    latencia_ms INTEGER NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_POPS: list[dict[str, str]] = [
    {
        "codigo": "POP.ENF.001",
        "titulo": "Punção Venosa Periférica com Cateter Sobre Agulha",
        "setor": "Divisão de Enfermagem",
        "versao": "v3.2 - 2026 [DEMO]",
        "objetivo": "Padronizar a instalação e estabilização de acesso venoso periférico seguro para terapia infusional em pacientes adultos, prevenindo flebite, infiltração e acidentes com perfurocortantes.",
        "materiais": (
            "Bandeja limpa e desinfetada com álcool 70%\n"
            "Luvas de procedimento e óculos de proteção individual\n"
            "Garrote desinfetado e swabs de clorexidina alcoólica 0,5%\n"
            "Cateter periférico sobre agulha estéril (20G ou 22G conforme rede venosa)\n"
            "Cobertura estéril transparente semipermeável datada\n"
            "Extensor luer-lock de 2 vias preenchido + seringa 10 mL com SF 0,9%"
        ),
        "passos_execucao": (
            "1. Higienizar as mãos conforme os 5 momentos da OMS e reunir os materiais na bandeja desinfetada.\n"
            "2. Orientar o paciente sobre o procedimento e selecionar veia calibrosa e retilínea, preferencialmente no membro superior não dominante.\n"
            "3. Posicionar o garrote 10 cm acima do sítio escolhido e realizar antissepsia com clorexidina alcoólica 0,5% em fricção por 30 segundos, aguardando secagem espontânea completa.\n"
            "4. Tracionar a pele, inserir o cateter com bisel voltado para cima em ângulo de 15° a 30° até visualizar refluxo sanguíneo na câmara.\n"
            "5. Avançar apenas o cateter flexível, retrair o mandril com dispositivo de segurança, soltar o garrote e acoplar o extensor salinizado.\n"
            "6. Testar permeabilidade com flushing pulsátil de SF 0,9%, estabilizar com película estéril transparente e registrar data, calibre e rubrica na borda do curativo."
        ),
        "alertas_seguranca": (
            "Jamais reencapar agulhas; descartar o mandril imediatamente em coletor rígido de perfurocortantes à beira-leito.\n"
            "Proibido tornar a palpar o sítio venoso após a antissepsia com clorexidina.\n"
            "Respeitar o limite máximo de 2 tentativas por profissional; na falha, acionar enfermeiro sênior ou time de terapia infusional.\n"
            "Programar troca em até 96 horas ou remoção imediata diante de dor, hiperemia, cordão venoso palpável ou infiltração."
        ),
        "palavras_chave": "puncao venosa periferica, acesso venoso, jelco, abocath, cateter periferico, soro, veia, flebite",
        "status": "ATIVO",
    },
    {
        "codigo": "POP.CCIH.002",
        "titulo": "Higienização Simples e Fricção Antisséptica das Mãos",
        "setor": "CCIH",
        "versao": "v4.0 - 2026 [DEMO]",
        "objetivo": "Eliminar a microbiota transitória e reduzir a microbiota residente das mãos da equipe multiprofissional, interrompendo a cadeia de transmissão de Infecções Relacionadas à Assistência à Saúde (IRAS).",
        "materiais": (
            "Dispensador de preparação alcoólica a 70% (gel ou solução glicerinada)\n"
            "Pia exclusiva de lavagem com água corrente potável\n"
            "Sabonete líquido neutro ou clorexidina degermante 2% (áreas críticas)\n"
            "Papel-toalha descartável não reciclado em suporte fechado\n"
            "Lixeira com tampa acionada por pedal"
        ),
        "passos_execucao": (
            "1. Retirar adornos (anéis, pulseiras e relógio) antes do início do turno; manter unhas curtas.\n"
            "2. Na ausência de sujidade visível, aplicar preparação alcoólica 70% cobrindo toda a superfície das mãos e friccionar por 20 a 30 segundos até secar.\n"
            "3. Na presença de sujidade visível ou exposição a fluidos corporais, higienizar com água e sabonete líquido por 40 a 60 segundos.\n"
            "4. Friccionar palmas, dorso com dedos entrelaçados, espaços interdigitais, dorso dos dedos, polegares em movimento rotacional e polpas digitais.\n"
            "5. Enxaguar no sentido dos dedos para os punhos sem tocar na torneira e secar com papel-toalha descartável."
        ),
        "alertas_seguranca": (
            "Executar obrigatoriamente nos 5 Momentos da OMS: antes de tocar o paciente, antes de procedimento limpo/asséptico, após risco de exposição a fluidos, após tocar o paciente e após tocar superfícies próximas.\n"
            "O uso de luvas jamais substitui a higienização das mãos antes do calçamento e imediatamente após a retirada.\n"
            "Em casos suspeitos ou confirmados de Clostridioides difficile, utilizar exclusivamente água e sabonete (esporos resistem ao álcool)."
        ),
        "palavras_chave": "higienizacao das maos, lavagem das maos, alcool gel, 5 momentos oms, ccih, iras, antissepsia maos, zero adorno",
        "status": "ATIVO",
    },
    {
        "codigo": "POP.ENF.003",
        "titulo": "Sondagem Vesical de Demora (Sistema Fechado Estéril)",
        "setor": "Divisão de Enfermagem",
        "versao": "v2.5 - 2026 [DEMO]",
        "objetivo": "Assegurar a drenagem urinária contínua por técnica rigorosamente estéril em sistema fechado, prevenindo Infecção do Trato Urinário Associada a Cateter Vesical (ITU-AC) e trauma uretral.",
        "materiais": (
            "Kit estéril de cateterismo vesical (cuba-rim, cúpula, pinça Pean e campo fenestrado)\n"
            "Luvas estéreis + luvas de procedimento, máscara cirúrgica e óculos de proteção\n"
            "Cateter de Foley estéril 2 vias (14Fr ou 16Fr adulto) + bolsa coletora sistema fechado\n"
            "Clorexidina aquosa 0,2% + gazes estéreis\n"
            "Seringa 20 mL estéril + água destilada estéril (ampolas de 10 mL para o balonete)\n"
            "Gel de lidocaína 2% estéril em bisnaga de uso único lacrada + dispositivo fixador de coxa"
        ),
        "passos_execucao": (
            "1. Conferir prescrição médica e indicação clínica estrita; higienizar as mãos e preservar a privacidade do leito com biombo.\n"
            "2. Calçar luvas de procedimento e realizar higiene íntima prévia com água e sabonete neutro; retirar luvas e higienizar novamente as mãos.\n"
            "3. Abrir o campo estéril, conectar previamente o cateter de Foley à bolsa coletora de sistema fechado antes da inserção.\n"
            "4. Calçar luvas estéreis, realizar antissepsia do meato uretral com clorexidina aquosa 0,2% em sentido unidirecional e posicionar o campo fenestrado.\n"
            "5. Lubrificar a uretra/cateter com lidocaína gel estéril de uso único, introduzir suavemente até retorno urinário mais 3 a 5 cm (até a bifurcação no sexo masculino) e insuflar o balonete exclusivamente com água destilada estéril.\n"
            "6. Tracionar delicadamente até ancoragem, fixar na face anterolateral da coxa ou hipogástrio e posicionar bolsa coletora abaixo do nível da bexiga sem tocar o piso."
        ),
        "alertas_seguranca": (
            "Procedimento privativo do Enfermeiro na equipe de enfermagem (Resolução COFEN vigente).\n"
            "Jamais insuflar o balonete com soro fisiológico 0,9% (risco de cristalização e obstrução na retirada) nem desconectar a junção cateter-bolsa.\n"
            "Diante de resistência uretral ou dor intensa, interromper imediatamente a progressão e acionar avaliação médica.\n"
            "Reavaliar diariamente a permanência do cateter para remoção precoce (bundle de prevenção de ITU-AC)."
        ),
        "palavras_chave": "sondagem vesical de demora, svd, cateterismo vesical, sonda foley, bolsa coletora, urina, itu, retencao urinaria",
        "status": "ATIVO",
    },
    {
        "codigo": "POP.FARM.004",
        "titulo": "Administração Segura de Medicamentos (Protocolo dos 9 Certos)",
        "setor": "Farmácia Clínica & Enfermagem",
        "versao": "v3.1 - 2026 [DEMO]",
        "objetivo": "Prevenir eventos adversos evitáveis na cadeia medicamentosa hospitalar mediante conferência estruturada dos 9 Certos e dupla checagem independente para Medicamentos Potencialmente Perigosos (MPP).",
        "materiais": (
            "Prescrição eletrônica vigente e legível no posto de enfermagem\n"
            "Bandeja individual desinfetada e etiquetas padronizadas de identificação de seringa/bolsa\n"
            "Medicamento dispensado por dose individualizada pela Farmácia Hospitalar\n"
            "Diluente compatível (SF 0,9% ou SG 5% conforme estabilidade farmacêutica)\n"
            "Swabs de álcool isopropílico 70% para desinfecção de ampolas, frascos e conectores\n"
            "Equipamentos de proteção individual (luvas e máscara quando antimicrobiano/citotóxico)"
        ),
        "passos_execucao": (
            "1. Higienizar as mãos e preparar a medicação em bancada limpa e livre de distrações, conferindo integridade e validade do fármaco.\n"
            "2. Executar a tripla leitura do rótulo confrontando os 9 Certos: paciente, medicamento, via, hora, dose, registro, orientação, forma farmacêutica e resposta esperada.\n"
            "3. Para Medicamentos Potencialmente Perigosos (insulinas, anticoagulantes, eletrólitos concentrados, vasopressores e opioides), realizar dupla checagem independente com segundo enfermeiro.\n"
            "4. Desinfetar o septo do frasco-ampola e o conector luer-lock com álcool 70% por 15 segundos antes da aspiração e da administração.\n"
            "5. Conferir no leito dois identificadores institucionais na pulseira do paciente antes de administrar e explicar a finalidade do fármaco.\n"
            "6. Checar imediatamente na prescrição eletrônica e monitorar sinais precoces de reação infusional ou alergia."
        ),
        "alertas_seguranca": (
            "Jamais administrar medicamento preparado por outro profissional sem rotulagem completa ou baseado apenas em ordem verbal fora de emergência vital.\n"
            "Cloreto de Potássio (KCl 19,1%) concentrado possui tarja vermelha de alta vigilância: proibida administração em bolus endovenoso sob qualquer hipótese.\n"
            "Em caso de reação adversa aguda, interromper imediatamente a infusão, manter o acesso venoso pérvio com SF 0,9% novo e acionar equipe médica + notificação Vigihosp."
        ),
        "palavras_chave": "administracao segura de medicamentos, 9 certos, medicacao, alta vigilancia, mpp, dupla checagem, diluicao, kcl, insulina",
        "status": "ATIVO",
    },
    {
        "codigo": "POP.ENF.005",
        "titulo": "Curativo Limpo e Asséptico de Ferida Operatória",
        "setor": "Comissão de Pele & Enfermagem",
        "versao": "v2.1 - 2026 [DEMO]",
        "objetivo": "Promover cicatrização por primeira intenção e prevenir Infecção de Sítio Cirúrgico (ISC) mediante limpeza atraumática com técnica asséptica no pós-operatório.",
        "materiais": (
            "Pacote de curativo estéril (pinças anatômica, dente-de-rato e Kelly) ou luvas estéreis\n"
            "Luvas de procedimento, máscara cirúrgica e óculos de proteção\n"
            "Frasco de Soro Fisiológico 0,9% amornado/temperatura ambiente + agulha 40x12 (jato leve)\n"
            "Gazes estéreis 7,5 x 7,5 cm e cobertura primária estéril indicada\n"
            "Fita microporosa hipoalergênica ou filme transparente para fixação\n"
            "Saco branco leitoso para descarte de resíduos infectantes (Grupo A)"
        ),
        "passos_execucao": (
            "1. Manter o curativo oclusivo estéril de centro cirúrgico fechado nas primeiras 24 a 48 horas, salvo saturação intensa ou descolamento.\n"
            "2. Higienizar as mãos, orientar o paciente, calçar luvas de procedimento e remover a cobertura anterior umedecendo as bordas com SF 0,9% para evitar trauma epidérmico.\n"
            "3. Descartar a cobertura suja e as luvas de procedimento; higienizar novamente as mãos e abrir o pacote de curativo estéril.\n"
            "4. Limpar a incisão cirúrgica do local menos contaminado (linha de sutura) para o mais contaminado (pele perilesional), em movimentos únicos sem retorno.\n"
            "5. Secar apenas a pele perilesional com gaze estéril sem friccionar os pontos, aplicar cobertura estéril seca e datar a borda externa."
        ),
        "alertas_seguranca": (
            "Em paciente com múltiplos curativos no mesmo turno, iniciar rigorosamente pela incisão limpa/fechada antes de abordar feridas abertas ou infectadas.\n"
            "Não utilizar soluções antissépticas citotóxicas (PVPI tópico ou água oxigenada) diretamente sobre tecido de granulação ou incisão limpa.\n"
            "Comunicar imediatamente deiscência de sutura, exsudato purulento, calor local acentuado ou febre (critérios de ISC para vigilância da CCIH)."
        ),
        "palavras_chave": "curativo limpo, ferida operatoria, incisao cirurgica, asseptico, pontos, sutura, isc, comissao de pele",
        "status": "ATIVO",
    },
    {
        "codigo": "POP.ENF.006",
        "titulo": "Punção e Manutenção de Cateter Totalmente Implantado (Port-a-Cath)",
        "setor": "Unidade de Oncologia",
        "versao": "v1.9 - Em Revisão [DEMO]",
        "objetivo": "Protocolo em atualização pela Comissão de Terapia Infusional e CCIH quanto à padronização de solução de lock e calibre de agulha Huber.",
        "materiais": "Agulha tipo Huber estéril, campo fenestrado, luvas estéreis e clorexidina alcoólica 0,5%.",
        "passos_execucao": "1. Documento temporariamente suspenso para revisão normativa (RN02).",
        "alertas_seguranca": "Atenção: protocolo em revisão institucional. Consulte a chefia da Unidade de Oncologia.",
        "palavras_chave": "port-a-cath, cateter totalmente implantado, agulha huber, oncologia, quimioterapia",
        "status": "EM_REVISAO",
    },
]

SEED_LACUNAS: list[tuple[str, str, int]] = [
    ("punção de port-a-cath [demo]", "Como realizar a heparinização e punção do Port-a-Cath na enfermaria? [DEMO]", 6),
    ("coleta de hemocultura pareada [demo]", "Qual o volume por frasco e intervalo para coleta de hemocultura pareada? [DEMO]", 4),
    ("aspiração endotraqueal sistema fechado [demo]", "Quais passos do POP de aspiração traqueal em paciente intubado? [DEMO]", 3),
]

SEED_LOGS: list[tuple[str, str | None, int, int]] = [
    ("Quais materiais separar para punção venosa periférica? [DEMO]", "POP.ENF.001", 1, 18),
    ("5 momentos para higienização das mãos na UTI [DEMO]", "POP.CCIH.002", 1, 14),
    ("Qual líquido usar no balonete da sonda vesical de demora? [DEMO]", "POP.ENF.003", 1, 21),
    ("Dupla checagem de medicamentos potencialmente perigosos [DEMO]", "POP.FARM.004", 1, 16),
    ("Bandeja para punção venosa periférica adulto [DEMO]", "POP.ENF.001", 1, 12),
    ("Como realizar punção do Port-a-Cath? [DEMO]", None, 0, 15),
    ("Volume por frasco na coleta de hemocultura pareada [DEMO]", None, 0, 13),
    ("POP de aspiração endotraqueal sistema fechado [DEMO]", None, 0, 17),
]


def resolve_db_path(db_path: str | Path | None = None) -> Path:
    if db_path is not None:
        return Path(db_path)
    env_path = os.getenv("CHAT_POPS_DB_PATH")
    return Path(env_path) if env_path else DEFAULT_DB_PATH


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    target = resolve_db_path(db_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path | None = None, seed: bool = True) -> None:
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        if seed:
            count = conn.execute("SELECT COUNT(*) FROM pops").fetchone()[0]
            if count == 0:
                conn.executemany(
                    """
                    INSERT INTO pops (
                        codigo, titulo, setor, versao, objetivo,
                        materiais, passos_execucao, alertas_seguranca,
                        palavras_chave, status
                    ) VALUES (
                        :codigo, :titulo, :setor, :versao, :objetivo,
                        :materiais, :passos_execucao, :alertas_seguranca,
                        :palavras_chave, :status
                    )
                    """,
                    SEED_POPS,
                )
                conn.executemany(
                    """
                    INSERT INTO lacunas_protocolos (
                        termo_buscado, pergunta_exemplo, quantidade_buscas
                    ) VALUES (?, ?, ?)
                    """,
                    SEED_LACUNAS,
                )
                conn.executemany(
                    """
                    INSERT INTO logs_consultas (
                        pergunta, codigo_pop_retornado, foi_encontrado, latencia_ms
                    ) VALUES (?, ?, ?, ?)
                    """,
                    SEED_LOGS,
                )
        conn.commit()
