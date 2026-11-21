# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

FastAPI (Python 3) servindo interface web responsiva em HTML5, CSS3 e JavaScript puro, com persistência SQLite (compatível com PostgreSQL) e SDK `google-genai` para Function Calling.

## Users

Enfermeiros, técnicos de enfermagem, residentes multiprofissionais e internos em plantão hospitalar (consulta rápida à beira-leito, no posto de enfermagem ou em ronda de enfermaria), além de gestores da Comissão de Controle de Infecção Hospitalar (CCIH) e da Divisão de Enfermagem do Hospital Universitário (contexto HU-UFC / PET Saúde Digital).

## Product Purpose

Permitir consulta rápida, estruturada e auditável de Procedimentos Operacionais Padrão (POPs) hospitalares homologados durante o plantão — entregando materiais de bandeja, passo a passo oficial e pontos críticos de biossegurança em segundos — enquanto mapeia automaticamente lacunas de protocolos demandados pela equipe assistencial para priorização pela gestão.

## Positioning

Copiloto institucional B2E com *Human-in-the-Loop* conectado exclusivamente à base relacional oficial de POPs vigentes (`status = 'ATIVO'`): toda resposta clínica ou operacional cita obrigatoriamente `codigo` e `versao` do documento homologado, e qualquer procedimento ausente gera recusa segura imediata com registro automático na fila `lacunas_protocolos` — zero geração livre de condutas clínicas.

## Operating Context

Uso sob pressão de tempo em postos de enfermagem (desktops compartilhados sob iluminação fluorescente intensa ou reduzida no plantão noturno), corredores/enfermarias (tablets em ronda) e beira-leito (smartphones operados com uma mão antes da montagem de bandeja). Os documentos de origem na realidade hospitalar são POPs institucionais padrão EBSERH/HU identificados por códigos formais (`POP.ENF.001`, `POP.CCIH.004`), estruturados em Objetivo, Materiais Necessários, Execução/Passo a Passo e Alertas de Biossegurança.

## Capabilities and Constraints

- **RF01/RF02 — Consulta Conversacional e Estruturada:** Busca por linguagem natural ou código oficial via Function Calling (`buscar_pops_sql`), retornando exclusivamente campos homologados do banco (`codigo`, `titulo`, `setor`, `versao`, `objetivo`, `materiais`, `passos_execucao`, `alertas_seguranca`).
- **RF03 — Recusa Segura e Mapeamento de Lacunas:** Procedimentos sem POP `ATIVO` acionam `registrar_lacuna_sql`, incrementando a demanda por termo e pergunta original sem inventar instruções.
- **RF04 — Painel Analítico e Auditoria:** Registro em `logs_consultas` (pergunta, POP retornado, flag `foi_encontrado`, `latencia_ms`) e visão gerencial com total de consultas, taxa de cobertura (%), POPs mais acessados e ranking de lacunas.
- **RF05 — Catálogo Direto e Cadastro/Importação:** Listagem filtrável por termo e setor, leitura integral por código e tela dedicada para cadastrar ou importar novos POPs homologados.
- **RNF03 — Conformidade LGPD:** Proibição estrita de coletar, solicitar ou armazenar dados pessoais ou clínicos de pacientes (PII/PHI).
- **RNF04/RNF05 — Desempenho e Fallback Offline:** Consultas diretas em até 500ms (p95), chat em até 5s, e modo fallback determinístico funcional sem chave externa de LLM.

## Brand Commitments

- Identidade institucional hospitalar universitária (`chat-pops` — Copiloto de POPs / contexto HU-UFC & PET Saúde Digital).
- Idioma integralmente em português brasileiro técnico da área de enfermagem e saúde pública.

## Evidence on Hand

- Documentos de engenharia aprovados em `docs/01_ELICITACAO_REQUISITOS.md` e `docs/02_ARQUITETURA_E_DADOS.md`.
- Sem PDFs oficiais dos supervisores anexados nesta etapa inicial: o sistema partirá de um catálogo *seed* demonstrativo explicitamente rotulado com 5 POPs realistas no padrão estrutural EBSERH/HU (Punção Venosa Periférica, Higienização das Mãos, Sondagem Vesical de Demora, Administração Segura de Medicamentos e Curativo Limpo/Asséptico), acompanhado da interface de cadastro/importação para inserção imediata dos protocolos reais. Nenhuma homologação clínica real deve ser fabricada sem rótulo demonstrativo.

## Product Principles

1. **Rastreabilidade acima de fluência:** Toda orientação assistencial exibe código, setor e versão em destaque imediato; sem vínculo no banco ativo, o sistema recusa orientar.
2. **Prontidão de plantão:** A lista de materiais de bandeja, os passos numerados e os alertas de biossegurança devem ser escaneáveis em segundos, sem exigir leitura de blocos corridos.
3. **Lacuna vira inteligência de gestão:** Uma busca sem resposta nunca é um beco sem saída — torna-se evidência quantificada para a CCIH e a Divisão de Enfermagem.
4. **Zero fricção multi-dispositivo:** Mesma clareza operacional no computador do posto, no tablet da ronda e no celular à beira-leito, respeitando privacidade total (zero dados de pacientes).

## Accessibility & Inclusion

- RNF06: Alvos de toque mínimos de `44px`, navegação responsiva entre Desktop (`> 1024px`), Tablet (`768px–1024px`) e Smartphone (`< 768px`), alto contraste legível sob iluminação intensa de posto de enfermagem e zero fadiga visual em plantões longos.
