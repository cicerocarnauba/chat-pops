# Fase 2: Arquitetura, Modelagem de Dados (SQL) & Contratos da API — `chat-pops`

**Projeto:** `chat-pops` (Copiloto de Procedimentos Operacionais Padrão Hospitalares)  
**Status:** Arquitetura aprovada (implementação pausada aguardando POPs/documentos reais dos supervisores do PET Saúde Digital).

---

## 1. Visão Geral da Arquitetura

O `chat-pops` adota uma arquitetura em camadas com **desacoplamento entre regras de negócio, persistência SQL e provedor de LLM**, garantindo fidelidade institucional (anti-alucinação) por meio de **Tool Use / Function Calling** sobre o banco de dados relacional.

### Fluxo Principal (`POST /api/v1/chat`)
1. **Recebimento da Consulta:** O profissional envia a pergunta em linguagem natural (e opcionalmente o setor).
2. **Orquestração do Agente (LLM + Tools):** O serviço aciona o modelo Gemini com *System Instructions* restritivas (temperatura baixa, proibição de gerar condutas fora do banco) e expõe duas ferramentas Python determinísticas:
   - `buscar_pops_sql(termo_busca)`: Executa consulta SQL (`SELECT`) filtrando exclusivamente registros com `status = 'ATIVO'` por código, título, palavras-chave ou setor.
   - `registrar_lacuna_sql(termo_buscado, pergunta_original)`: Executada automaticamente quando nenhum POP ativo corresponde à demanda, criando ou incrementando o registro de lacuna.
3. **Formatação Rastreada:**
   - **Caso positivo:** O agente responde usando exclusivamente os campos retornados (`codigo`, `titulo`, `setor`, `versao`, `materiais`, `passos_execucao`, `alertas_seguranca`), com citação obrigatória do código e versão.
   - **Caso negativo (lacuna):** O agente recusa gerar instruções clínicas/operacionais e informa que a demanda foi registrada para a comissão responsável.
4. **Auditoria (Observabilidade):** Toda requisição é registrada em `logs_consultas` com a pergunta original, `codigo_pop_retornado`, flag `foi_encontrado` e `latencia_ms`.
5. **Fallback Determinístico:** Para testabilidade offline (RNF05) e execução sem chave de API externa, o serviço suporta um modo fallback que executa a busca SQL direta e formata a resposta estruturada deterministicamente.

### Decisões Tecnológicas & Stack
- **Backend & API:** Python 3 + FastAPI (documentação OpenAPI/Swagger automática).
- **Persistência:** Banco relacional SQL (SQLite em desenvolvimento local/testes, compatível com PostgreSQL).
- **Motor de IA:** Google Gemini API (`google-genai` SDK v3.6+ com `v1beta`) utilizando *Function Calling* + conexão BYOK opcional em Ajustes.
- **Interface Web Responsiva (RNF06):** Frontend leve (HTML5, CSS3 responsivo com breakpoints para **Mobile `< 768px`**, **Tablet `768px–1024px`** e **Desktop `> 1024px`** + JS puro) servido pelo FastAPI:
  - **Desktop / Tablet:** Layout em 2 colunas (navegação lateral fixa entre *Chat de Consulta*, *Catálogo de POPs* e *Painel de Gestão/Lacunas* + área principal ampla para leitura confortável de protocolos).
  - **Smartphone:** Navegação adaptada em barra inferior (*bottom tab bar*) com leitura vertical otimizada, checklists de materiais fáceis de marcar e campo de consulta fixo na base.
- **Testes:** `pytest` com isolamento da camada de IA via *mocks/stubs*.

---

## 2. Modelagem de Dados Relacional (SQL)

### Tabela 1: `pops` (Catálogo Oficial de Protocolos)
| Coluna | Tipo SQL | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Identificador interno |
| `codigo` | `VARCHAR(30)` | `UNIQUE NOT NULL` | Código institucional (ex.: `POP.ENF.001`, `POP.CCIH.004`) |
| `titulo` | `VARCHAR(200)` | `NOT NULL` | Nome oficial do procedimento |
| `setor` | `VARCHAR(100)` | `NOT NULL` | Setor responsável (ex.: `Divisão de Enfermagem`, `CCIH`) |
| `versao` | `VARCHAR(20)` | `NOT NULL` | Versão e ano de homologação (ex.: `v3.2 - 2026`) |
| `objetivo` | `TEXT` | `NOT NULL` | Finalidade assistencial/operacional |
| `materiais` | `TEXT` | `NOT NULL` | Lista de materiais para montagem de bandeja |
| `passos_execucao` | `TEXT` | `NOT NULL` | Passo a passo numerado oficial |
| `alertas_seguranca` | `TEXT` | `NOT NULL` | EPIs, contraindicações e pontos críticos de biossegurança |
| `palavras_chave` | `VARCHAR(255)` | `NOT NULL` | Termos de busca normalizados |
| `status` | `VARCHAR(20)` | `NOT NULL DEFAULT 'ATIVO'` | `ATIVO` ou `EM_REVISAO` (RN02) |

### Tabela 2: `lacunas_protocolos` (Mapeamento de POPs Inexistentes — RF03 / RN03)
| Coluna | Tipo SQL | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Identificador interno |
| `termo_buscado` | `VARCHAR(150)` | `UNIQUE NOT NULL` | Termo normalizado do procedimento não encontrado |
| `pergunta_exemplo` | `TEXT` | `NOT NULL` | Última pergunta real feita pelo profissional |
| `quantidade_buscas` | `INTEGER` | `NOT NULL DEFAULT 1` | Frequência da demanda pela equipe |
| `ultima_ocorrencia` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Data/hora da última tentativa |

### Tabela 3: `logs_consultas` (Auditoria e Observabilidade — RF04 / RNF02)
| Coluna | Tipo SQL | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Identificador do log |
| `pergunta` | `TEXT` | `NOT NULL` | Pergunta original enviada ao chat |
| `codigo_pop_retornado` | `VARCHAR(30)` | `NULL` | Código do POP citado (ou `NULL` em caso de lacuna) |
| `foi_encontrado` | `BOOLEAN` | `NOT NULL` | `1` (Sucesso) ou `0` (Lacuna) |
| `latencia_ms` | `INTEGER` | `NOT NULL` | Tempo total de processamento em milissegundos |
| `criado_em` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Data/hora da consulta |

---

## 3. Contratos da API REST (FastAPI)

| Método | Endpoint | Propósito |
| :--- | :--- | :--- |
| `POST` | `/api/v1/chat` | Recebe `pergunta` e `setor_usuario` (opcional), executa o agente com busca SQL, grava auditoria/lacuna e retorna resposta estruturada + metadados do POP citado. |
| `GET` | `/api/v1/pops` | Lista POPs ativos com filtros opcionais por `termo` e `setor`. |
| `GET` | `/api/v1/pops/{codigo}` | Consulta direta de um POP específico pelo código oficial. |
| `POST` | `/api/v1/pops` | Cadastra um novo POP homologado na base. |
| `GET` | `/api/v1/analytics/resumo` | Retorna indicadores gerenciais: total de consultas, taxa de cobertura (%), ranking dos POPs mais buscados e ranking de lacunas prioritárias. |
