# Fase 1: Elicitação de Requisitos — `chat-pops`

**Projeto:** `chat-pops` (Copiloto de Procedimentos Operacionais Padrão Hospitalares)  
**Contexto:** Hospital Universitário (HU-UFC) / Ecossistema PET Saúde Digital  
**Público-Alvo (Atores):** Enfermeiros, Técnicos de Enfermagem, Residentes Multiprofissionais, Internos e Gestores da Comissão de Padronização (CCIH / Divisão de Enfermagem).

---

## 1. Definição do Problema ("Qual é a dor real?")

### 1.1. Gargalo Operacional no Plantão
Em Hospitais Universitários com alta rotatividade de estudantes, internos e residentes, a execução de procedimentos assistenciais deve seguir estritamente os **Procedimentos Operacionais Padrão (POPs)** homologados pela instituição (ex.: `POP.ENF.001`, `POP.CCIH.014`). Atualmente, esses documentos encontram-se distribuídos em dezenas de arquivos PDF longos (15 a 40 páginas) na intranet hospitalar, dificultando a consulta rápida durante o plantão para checar listas de materiais de bandeja, etapas de execução e alertas de biossegurança.

### 1.2. Decisão de Produto e Mitigação de Risco Clínico
Durante a concepção do produto, **descartou-se o uso de IA generativa voltada diretamente ao paciente final** para orientações clínicas, pois o risco de alucinação de um LLM em condutas de saúde supera o benefício.  
Em vez disso, o `chat-pops` adota uma abordagem **B2E (Business-to-Employee) com Human-in-the-Loop**:
1. O usuário final é um **profissional ou residente qualificado**;
2. O modelo de IA **não gera condutas livres**: ele atua estritamente como uma interface conversacional conectada à **base relacional oficial de POPs do hospital**, citando obrigatoriamente o código e a versão do protocolo homologado.

---

## 2. Requisitos Funcionais (RFs)

| ID | Requisito | Descrição |
| :--- | :--- | :--- |
| **RF01** | **Consulta de POPs via Linguagem Natural e SQL** | O sistema deve permitir que o profissional consulte protocolos em linguagem natural (ex.: *"Quais materiais preciso para punção venosa?"* ou *"Busque o POP.ENF.002"*). O agente deve traduzir a intenção em uma busca estruturada no banco de dados SQL por código, título, setor ou palavras-chave. |
| **RF02** | **Resposta Estruturada com Citação Oficial** | Ao localizar um POP aplicável, o assistente deve responder utilizando exclusivamente os dados oficiais do banco, apresentando: (1) Código, Título, Setor e Versão do POP; (2) Lista de Materiais Necessários; (3) Passo a Passo / Execução; e (4) Pontos Críticos / Biossegurança. |
| **RF03** | **Recusa Segura e Registro de Lacuna de Protocolo** | Caso o procedimento buscado não possua POP cadastrado ou ativo no banco de dados, o sistema deve recusar a geração de instruções médicas/operacionais por conta própria e registrar automaticamente a demanda na tabela `lacunas_protocolos` para notificar a gestão hospitalar sobre protocolos faltantes. |
| **RF04** | **Auditoria e Métricas de Consultas** | O sistema deve registrar todas as interações em uma tabela de histórico (`logs_consultas`) e disponibilizar um endpoint analítico para a gestão visualizar os POPs mais consultados e as principais lacunas identificadas no hospital. |
| **RF05** | **Catálogo Direto de POPs (CRUD/Listagem)** | O sistema deve expor endpoints REST diretos para listagem, busca por código e cadastro de novos POPs homologados no banco de dados. |

---

## 3. Regras de Negócio (RNs)

* **RN01 — Fonte Única de Verdade (Single Source of Truth):** Nenhuma etapa técnica ou lista de materiais pode ser apresentada ao usuário se não vier do retorno da ferramenta de consulta ao banco SQL de POPs.
* **RN02 — Status de Homologação:** Apenas POPs com status `ATIVO` (vigentes) devem ser utilizados para orientar procedimentos no chat.
* **RN03 — Rastreabilidade de Lacunas:** Toda consulta cuja busca SQL retorne vazio deve gerar ou incrementar um registro de lacuna com o termo pesquisado e a pergunta original do profissional.

---

## 4. Requisitos Não-Funcionais (RNFs — ISO/IEC 25010)

* **RNF01 — Confiabilidade e Fidelidade à Fonte (Groundedness / Anti-Alucinação):** O sistema deve garantir 100% de vinculação institucional nas respostas clínicas/operacionais, exigindo citação explícita do `codigo_pop` e `versao` em todas as orientações positivas.
* **RNF02 — Auditabilidade e Rastreabilidade:** Todas as requisições conversacionais devem gerar log persistente contendo data/hora, pergunta original, POPs acionados, flag de lacuna (`foi_encontrado`) e tempo de resposta em milissegundos.
* **RNF03 — Segurança e Privacidade (Conformidade LGPD):** O sistema não deve coletar, exigir ou armazenar dados pessoais ou clínicos de pacientes (PII/PHI), operando exclusivamente sobre protocolos institucionais.
* **RNF04 — Desempenho (Tempo de Resposta):** Endpoints REST de consulta direta ao banco devem responder em até `500ms` (p95), e consultas mediadas pelo agente de IA devem concluir em até `5s` em condições normais de rede.
* **RNF05 — Testabilidade e Desacoplamento:** A lógica de busca SQL, registro de auditoria e regras de negócio deve ser desacoplada do cliente de LLM externo, permitindo execução determinística e offline de testes automatizados.
* **RNF06 — Portabilidade e Responsividade Multi-Dispositivo:** A interface web deve ser plenamente responsiva (*mobile-first*), adaptando layout, tipografia, alvos de toque (mínimo `44px`) e navegação para operação fluida em **Desktop** (computadores do posto de enfermagem), **Tablet** (ronda em enfermarias) e **Smartphone** (consulta rápida à beira-leito).
