---
name: chat-pops
description: Sistema visual de fichário cirúrgico em acetato leitoso e divisórias rígidas por comissão para consulta auditável de POPs hospitalares no HU-UFC.
colors:
  board-teal: "#0D6B63"
  ink-verified: "#0B5852"
  board-grass: "#2F6B3B"
  board-ultramarine: "#1E4B94"
  board-oxide: "#A84311"
  vermilion-alert: "#B92525"
  vermilion-soft: "#FDF2F2"
  vermilion-ink: "#6E1414"
  status-active-bg: "#DCF2E4"
  status-active-ink: "#14532D"
  milk-acetate: "rgba(246, 244, 236, 0.95)"
  leaf-solid: "#F6F4EC"
  leaf-inset: "#FBF9F4"
  leaf-recessed: "#EAE6D9"
  board-stack-backing: "#DFDBC9"
  rule-hairline: "#C7C2B4"
  field-stroke: "#9E998A"
  ink-primary: "#181B1A"
  ink-secondary: "#3A423F"
  ink-muted: "#505A56"
  paper-white: "#FFFFFF"
typography:
  display:
    fontFamily: "'Archivo', system-ui, -apple-system, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.18
    letterSpacing: "-0.02em"
    fontVariation: '"wdth" 86'
  headline:
    fontFamily: "'Archivo', system-ui, -apple-system, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
    fontVariation: '"wdth" 86'
  title:
    fontFamily: "'Archivo', system-ui, -apple-system, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 700
    lineHeight: 1.28
    fontVariation: '"wdth" 86'
  body:
    fontFamily: "'Archivo', system-ui, -apple-system, sans-serif"
    fontSize: "0.90625rem"
    fontWeight: 500
    lineHeight: 1.44
  body-reading:
    fontFamily: "'Spectral', Georgia, serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.44
  label:
    fontFamily: "'Archivo', system-ui, -apple-system, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 700
    letterSpacing: "0.06em"
    fontVariation: '"wdth" 86'
  mono:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: "0.75rem"
    fontWeight: 600
    fontFeature: '"tnum" 1'
rounded:
  sm: "4px"
  md: "8px"
  lg: "10px"
spacing:
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "18px"
  xl: "26px"
components:
  button-primary:
    backgroundColor: "{colors.board-teal}"
    textColor: "{colors.paper-white}"
    rounded: "{rounded.sm}"
    padding: "0 15px"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.ink-primary}"
  button-secondary:
    backgroundColor: "{colors.leaf-inset}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "0 15px"
    height: "44px"
  button-secondary-hover:
    backgroundColor: "{colors.ink-primary}"
    textColor: "{colors.paper-white}"
  button-outline-sm:
    backgroundColor: "{colors.leaf-inset}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "44px"
  button-ghost-xs:
    textColor: "{colors.ink-secondary}"
    rounded: "{rounded.sm}"
    padding: "0 10px"
    height: "44px"
  input-field:
    backgroundColor: "{colors.leaf-inset}"
    textColor: "{colors.ink-primary}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "9px 12px"
    height: "44px"
  code-stamp:
    backgroundColor: "{colors.ink-primary}"
    textColor: "{colors.paper-white}"
    typography: "{typography.mono}"
    rounded: "{rounded.sm}"
    padding: "5px 10px"
  status-stamp-active:
    backgroundColor: "{colors.status-active-bg}"
    textColor: "{colors.status-active-ink}"
    typography: "{typography.mono}"
    rounded: "{rounded.sm}"
    padding: "5px 9px"
  pop-card:
    backgroundColor: "{colors.leaf-inset}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "16px"
  fore-tab:
    backgroundColor: "{colors.board-teal}"
    textColor: "{colors.paper-white}"
    typography: "{typography.label}"
    padding: "12px 10px"
    width: "52px"
  punch-item:
    backgroundColor: "{colors.leaf-inset}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "6px 11px"
    height: "44px"
  vermilion-slip:
    backgroundColor: "{colors.vermilion-alert}"
    textColor: "{colors.paper-white}"
    rounded: "{rounded.md}"
    padding: "11px 15px"
---

# Design System: chat-pops

## Overview

**Creative North Star: "O Fichário Cirúrgico de Acetato Leitoso"**

O `chat-pops` traduz o fichário físico de Procedimentos Operacionais Padrão (POPs) do posto de enfermagem para um instrumento digital seco, rastreável e imediato. Uma folha única contínua de acetato leitoso fosco (`rgba(246, 244, 236, 0.95)`) repousa sobre uma pilha escalonada de pranchas divisórias rígidas coloridas por comissão ou função operacional na borda direita. A cor saturada pertence exclusivamente à prancha ativa no fundo do palco, aos furos de encadernação vazados que revelam essa prancha e ao botão de ação primária acoplado à seção.

A densidade prioriza prontidão sob pressão de plantão hospitalar: fios de impressão de `1px` e `1.5px`, carimbos normativos em código monoespaçado tabular, conferência tátil de bandeja por círculos perfurados e leitura serena de etapas clínicas sem blocos corridos. O sistema recusa explicitamente a estética de chat SaaS corporativo cinza ou azul genérico, bolhas de conversa flutuantes com sombras difusas, gradientes decorativos e caixas de métricas aninhadas em cascata.

**Key Characteristics:**
- Folha contínua de acetato leitoso fosco com micro-retícula de `12px` assentada sobre prancha divisória saturada dinâmica.
- Trilho esquerdo de encadernação com furos vazados de `18px` e pilha direita de 4 divisórias verticais escalonadas contínuas.
- Separação tipográfica funcional entre títulos condensados (`Archivo` a `86%` de largura), leitura clínica serifada (`Spectral`) e rastreabilidade tabular (`JetBrains Mono`).
- Vermelhão institucional (`#B92525`) isolado em quarentena semântica para alertas críticos de biossegurança da CCIH e recusas seguras.
- Transições mecânicas secas de `90ms steps(2)` combinadas a um único assentamento inicial de `260ms` da folha no carregamento.

## Colors

A paleta opõe superfícies quentes de papel técnico e tinta mineral escura a quatro pranchas divisórias institucionais de alta saturação e um único vermelhão normativo de segurança clínica.

### Primary
- **Verde-Petróleo Enfermagem** (`#0D6B63`): Cor padrão da prancha divisória ativa na visão de consulta assistencial, fundo perimetral do palco, preenchimento visível através dos furos perfurados, seleção de texto e ação primária da seção.
- **Verde-Tinta Auditado** (`#0B5852`): Variante escurecida para contraste tipográfico sobre papel claro em links sublinhados, selos de verificação SQL e numeração de etapas clínicas.

### Secondary
- **Verde-Folha Catálogo** (`#2F6B3B`): Prancha divisória dedicada ao catálogo oficial de protocolos homologados; assume a variável global da prancha ativa quando selecionada.
- **Azul-Ultramar Normativo** (`#1E4B94`): Prancha divisória da oficina de cadastro e importação de novas folhas normativas EBSERH/HU.
- **Óxido-Terracota CCIH** (`#A84311`): Prancha divisória do livro gerencial de cobertura, auditoria de consultas e fila prioritária de lacunas da CCIH.
- **Verde-Água de Homologação** (`#DCF2E4`) e **Tinta Floresta de Homologação** (`#14532D`): Par semântico exclusivo para o carimbo `ATIVO` e faixas de sucesso após gravação no banco relacional.

### Tertiary
- **Vermelhão de Biossegurança** (`#B92525`): Fundo de alto impacto reservado à tarja obrigatória de pontos críticos da CCIH e ao cabeçalho de recusa segura quando não há POP vigente.
- **Fundo Rosado de Alerta** (`#FDF2F2`) e **Tinta Carmim Escura** (`#6E1414`): Par de superfície e texto para faixas de erro de validação ou falha de extração de arquivo.

### Neutral
- **Acetato Leitoso Fosco** (`rgba(246, 244, 236, 0.95)`) e **Papel Leitoso Sólido** (`#F6F4EC`): Superfície mestra translúcida da folha do fichário no desktop e seu equivalente opaco para a barra horizontal de divisórias no smartphone.
- **Papel Marfim de Controle** (`#FBF9F4`): Superfície interna clara para campos de formulário, cartões do catálogo, itens de bandeja não marcados, respostas do assistente e botões secundários.
- **Cartolina Rebaixada** (`#EAE6D9`): Camada recessiva aplicada ao trilho esquerdo de furos, perguntas enviadas pelo profissional, itens de bandeja já perfurados e trilha da barra de rolagem.
- **Cartão Suporte do Fichário** (`#DFDBC9`): Base estrutural rígida posicionada atrás da pilha de abas na margem direita.
- **Fio Pautado de Manual** (`#C7C2B4`) e **Traço Pedra de Formulário** (`#9E998A`): Fios divisórios estruturais de `1px` entre colunas/seções e bordas de repouso de campos editáveis e botões contornados.
- **Tinta Preta de Impressão** (`#181B1A`): Texto primário, fios mestres de cabeçalho (`1.5px`), carimbos de código oficial, contorno de foco visível e estado hover sólido.
- **Grafite Mineral Secundário** (`#3A423F`) e **Cinza-Ardósia Técnico** (`#505A56`): Subtítulos, objetivos assistenciais, rótulos de campo, legendas verticais de lombada e metadados de latência.
- **Branco Puro de Contraste** (`#FFFFFF`): Texto reverso sobre pranchas saturadas, carimbos escuros e tarja vermelhão, além do fundo de inputs quando em foco ativo.

### Named Rules
**The Active Divider Board Rule.** Apenas uma cor de prancha institucional ocupa o palco por vez: ao trocar de divisória, o fundo do documento, os furos vazados, o item ativo do índice e os botões primários assumem instantaneamente a cor da comissão ativa (`#0D6B63`, `#2F6B3B`, `#1E4B94` ou `#A84311`), mantendo a folha interna rigorosamente neutra.

**The Vermilion Quarantine Rule.** O vermelhão (`#B92525`) nunca é usado em ações destrutivas comuns, contadores decorativos ou abas de navegação; sua presença sinaliza exclusivamente risco biológico crítico da CCIH ou bloqueio normativo por ausência de protocolo vigente.

## Typography

**Display Font:** `Archivo` com eixo variável de largura condensada (`"wdth" 86`, fallback `system-ui, -apple-system, sans-serif`)
**Body Font:** `Archivo` para controles operacionais e `Spectral` (`Georgia, serif`) para leitura clínica de objetivos e etapas
**Label/Mono Font:** `JetBrains Mono` (`ui-monospace, monospace`) com algarismos tabulares (`tabular-nums`)

**Character:** O trio tipográfico separa comando, leitura e auditoria como em um impresso técnico hospitalar: `Archivo` condensada imprime autoridade compacta em cabeçalhos e abas verticais, `Spectral` desacelera o olho na execução sequencial à beira-leito, e `JetBrains Mono` crava códigos normativos, versões e tempos de resposta SQL sem oscilação horizontal.

### Hierarchy
- **Display** (`700`, `1.5rem`, line-height `1.18`, letter-spacing `-0.02em`, `"wdth" 86`): Título do protocolo aberto na folha normativa e cabeçalho principal das folhas internas de catálogo, importação e controle da CCIH.
- **Headline** (`700`, `1.375rem`, line-height `1.2`, letter-spacing `-0.02em`, `"wdth" 86`): Identificação institucional no topo da coluna esquerda de consulta.
- **Title** (`700`, `1.0625rem` em cartões/tabelas e `1rem` em barras de seção, line-height `1.28`, `"wdth" 86`): Títulos de cartões de protocolo, tabelas pautadas de auditoria, comprovantes de lacuna e subseções bilaterais.
- **Body** (`500` em `Archivo` a `0.90625rem`, line-height `1.44`; `400` em `Spectral` a `0.9375rem`–`0.96875rem`, line-height `1.44`–`1.48`): `Archivo` governa turnos de diálogo, campos e checklist (`0.875rem`), enquanto `Spectral` governa o objetivo clínico (máximo `74ch`) e a lista numerada de passos de execução (máximo `68ch`).
- **Label** (`700`, `0.75rem`, letter-spacing `0.06em`, caixa alta com `"wdth" 86` nas divisórias; `600`, `0.8125rem` em rótulos de campo): Rótulos verticais das abas de borda e cabeçalhos diretos de formulários e tabelas.
- **Mono** (`600`, `0.75rem`–`0.8125rem`, `tabular-nums`; `1.1875rem` em indicadores da barra de telemetria): Carimbos de código (`POP.ENF.001`), status normativo, progresso da bandeja (`0/6 marcados`), índices de etapas (`01.`) e latência SQL em milissegundos.

### Named Rules
**The Condensed Spine & Serif Step Rule.** A condensação `"wdth" 86` aplica-se exclusivamente a títulos (`h1`–`h3`) e abas divisórias (e `"wdth" 90` em botões), nunca ao corpo corrido; inversamente, `Spectral` é restrita ao objetivo e aos passos homologados do POP, jamais aparecendo em botões, tabelas ou mensagens de sistema.

**The Tabular Audit Rule.** Todo código de protocolo, versão, contador de conferência, frequência de lacuna e medição de latência deve ser renderizado em `JetBrains Mono` com `font-variant-numeric: tabular-nums`.

## Layout

Em telas amplas de posto de enfermagem (`> 1160px`), o palco do fichário ocupa exatamente `100vh` (`min-height: 820px`) com recuo perimetral assimétrico (`18px 14px 18px 20px`) que expõe a moldura da prancha ativa. A grade mestra (`minmax(0, 1fr) 64px`) acopla a folha leitosa à pilha direita de divisórias (`64px`). Dentro da folha, uma segunda grade (`54px minmax(0, 1fr)`) isola o trilho esquerdo de furos (`54px`, padding `48px 12px 24px`) do conteúdo ativo.

A visão principal de consulta divide a mesma folha em duas colunas contínuas (`420px minmax(0, 1fr)`) separadas apenas por um fio vertical de `1px`: à esquerda (`padding: 18px 20px`), cabeçalho institucional, histórico rolável, índice rápido dos 5 primeiros protocolos ativos e barra de busca ancorada na base; à direita (`padding: 18px 26px`), cabeçalho normativo do POP, objetivo, grade bilateral rolável (`minmax(250px, 0.92fr) minmax(290px, 1.16fr)`, `gap: 22px`) confrontando Bandeja Conferida e Passos de Execução, e tarja vermelhão fixa acima da dobra (`flex-shrink: 0`). As demais divisórias utilizam folha única com rolagem interna (`padding: 22px 30px`, `gap: 18px`), grade responsiva no catálogo (`repeat(auto-fill, minmax(320px, 1fr))`, `gap: 14px`), barra pautada de 4 métricas (`repeat(4, 1fr)`) e livro dividido (`1.15fr 0.95fr`, `gap: 28px`).

O ritmo espacial segue incrementos curtos e funcionais (`6px`, `8px`, `12px`, `18px`, `26px`) e impõe altura mínima de `44px` em todos os alvos clicáveis ou digitáveis. Em tablets (`max-width: 1160px`), o palco libera a trava de `100vh` (`height: auto; min-height: 100vh`), empilha a consulta e a malha bilateral em coluna única (`1fr`) e converte grades de 4 colunas em pares (`1fr 1fr`), mantendo o trilho de furos e as abas laterais. Em smartphones (`max-width: 767px`), o fichário assume fluxo vertical de borda a borda (`padding: 0`): exibe cabeçalho compacto da seção ativa no topo, converte as 4 divisórias em faixa horizontal imediata (`min-height: 56px`), oculta o trilho de furos e títulos redundantes, reduz o preenchimento interno para `16px` e executa rolagem suave automática até a folha do protocolo ao abrir um item.

## Elevation & Depth

O sistema adota profundidade física contida em duas únicas cotas reais — a folha de acetato sobre a prancha rígida e os furos vazados através do papel — enquanto toda a organização interna ocorre por camadas tonais planas (`#FBF9F4` e `#EAE6D9` sobre `#F6F4EC`) e fios secos de impressão (`1px` e `1.5px`). Cartões, tabelas, turnos de conversa e botões nunca projetam sombra própria.

### Shadow Vocabulary
- **Elevação da Folha de Acetato** (`box-shadow: 0 12px 28px -8px rgba(18, 24, 23, 0.30), 0 3px 7px rgba(18, 24, 23, 0.16)`): Aplicada exclusivamente ao contêiner principal da folha leitosa, combinada com `backdrop-filter: blur(3px)` e textura pontilhada sutil (`radial-gradient(rgba(24, 27, 26, 0.03) 1px, transparent 0)` a cada `12px`). No carregamento inicial (respeitando `prefers-reduced-motion: no-preference`), assenta uma única vez em `260ms cubic-bezier(0.16, 1, 0.3, 1)`.
- **Recorte Vazado de Perfuração** (`box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.42)`): Sombra interna aplicada apenas aos furos de encadernação de `18px` no trilho esquerdo e aos círculos de `17px` dos itens de bandeja quando marcados, simulando espessura física sobre a prancha colorida visível ao fundo.

### Named Rules
**The Tactile Die-Cut Depth Rule.** Nenhum componente interno à folha pode usar `box-shadow` externo: a hierarquia dentro do protocolo vem de contrastes planos de papel (`#FBF9F4` vs. `#EAE6D9`) e espessura de fio (`1px` vs. `1.5px`), reservando sombras internas aos círculos perfurados que revelam a prancha ativa.

**The Flush Active Tab Rule.** A aba divisória ativa na borda direita remove sua borda direita (`border-right-color: transparent`), zera qualquer sombra (`box-shadow: none`) e expande de `52px` para `58px`, fundindo-se no mesmo plano cromático da prancha de suporte ao fundo.

## Shapes

A geometria combina cantos retos de guilhotina nos encontros mecânicos do fichário com raios curtos nos elementos internos. Controles operacionais, carimbos, campos e cartões usam raio técnico mínimo (`4px`), blocos compostos e a tarja de biossegurança usam curvatura moderada (`8px`), e a folha mestra adota silhueta assimétrica (`10px 0 10px 10px`) cujo canto superior direito vivo (`0px`) encaixa-se sem folga no cartão de suporte das abas (`0 10px 10px 0`).

As abas laterais projetam orelhas arredondadas apenas para fora (`0 8px 8px 0`), sobrepondo suas bordas horizontais em `-1px` para formar uma pilha contínua sem frestas. Círculos plenos (`50%`) são reservados estritamente aos furos do trilho esquerdo (`18px`), aos discos de conferência da bandeja (`17px`) e aos marcadores internos de `5px` da tarja vermelhão — nunca há botões ou campos em formato pílula. Fios estruturais seguem peso duplo: `1px` em `#C7C2B4` para pautas e divisões de coluna, e `1.5px` em `#181B1A` para cabeçalhos normativos de folha, cabeçalhos de tabela e moldura da barra de consulta.

## Components

Os componentes comportam-se como carimbos, pautas e recortes mecânicos de prontuário: resposta instantânea em `90ms steps(2)`, contornos nítidos e zero efeito elástico ou brilho difuso.

### Buttons
- **Shape:** Cantos técnicos curtos (`4px` de raio), altura mínima obrigatória de `44px`, tipografia `Archivo` peso `600` com `"wdth" 90` e espaçamento interno de `7px` entre rótulo e ícone SVG (`stroke-width: 1.75`).
- **Primary:** Fundo dinâmico na cor da prancha ativa (`#0D6B63` por padrão), texto branco (`#FFFFFF`), borda seca de `1px solid #181B1A` e padding horizontal de `15px` (`0.875rem`). Em `:disabled`, reduz opacidade para `0.65` com cursor `wait`.
- **Hover / Focus:** Troca seca em `90ms steps(2)` para fundo preto de impressão (`#181B1A`); foco por teclado exibe contorno externo de `2px solid #181B1A` com `outline-offset: 2px`.
- **Secondary / Outline / Ghost:** Secundário usa fundo marfim (`#FBF9F4`), texto e borda `#181B1A` (`0 15px`), invertendo para fundo `#181B1A` e texto `#FFFFFF` no hover; Contornado Compacto usa borda `#9E998A` (`0 12px`, `0.8125rem`) que escurece para `#181B1A` sobre fundo `#FFFFFF` no hover; Fantasma (`0 10px`, `0.78125rem`) permanece transparente com texto `#3A423F` até exibir borda `#C7C2B4` no hover.

### Chips
- **Style:** Carimbos retangulares compactos (`4px` de raio) em `JetBrains Mono` peso `600` com algarismos tabulares, substituindo pílulas arredondadas genéricas.
- **State:** O Carimbo de Código (`5px 10px`, `0.8125rem`) usa bloco sólido `#181B1A` com texto `#FFFFFF`; o Carimbo de Status (`5px 9px`, `0.75rem`, `border: 1px solid currentColor`) alterna entre homologado `ATIVO` (fundo `#DCF2E4`, texto `#14532D`) e retido `EM_REVISAO` / `LACUNA RF03` (texto riscado com `line-through`).

### Cards / Containers
- **Corner Style:** `4px` nos cartões de catálogo; `8px` nos turnos de conversa e no comprovante de demanda da CCIH; zero caixa individual na barra de telemetria (colunas separadas apenas por fios verticais de `1px` sobre a folha).
- **Background:** Papel marfim (`#FBF9F4`) para cartões ativos, turnos do assistente e comprovantes; cartolina rebaixada (`#EAE6D9`) para turnos do profissional; filtro `grayscale(1)` sobre fundo esmaecido para protocolos suspensos.
- **Shadow Strategy:** Estritamente planos (`box-shadow: none`), seguindo a seção Elevation & Depth.
- **Border:** `1px solid #C7C2B4` em repouso, mudando em `90ms steps(2)` para `1px solid #181B1A` no hover dos cartões de catálogo.
- **Internal Padding:** `16px` nos cartões do catálogo (`gap: 9px`), `18px` no comprovante de lacuna e `10px 13px` nos turnos de conversa.

### Inputs / Fields
- **Style:** Fundo `#FBF9F4`, borda `1px solid #9E998A`, raio de `4px`, altura mínima de `44px` (`102px` em áreas de texto) e padding `9px 12px` em `Archivo` (`0.90625rem`). A barra de consulta principal agrupa input transparente e botão primário dentro de uma moldura única de `1.5px solid #181B1A` com raio de `8px` e padding de `5px`.
- **Focus:** Muda o fundo para `#FFFFFF` e a borda para `#181B1A`, acompanhado do anel global `:focus-visible` (`2px solid #181B1A`, offset `2px`).
- **Error / Disabled:** Feedback de formulário aparece em faixa dedicada acima dos campos (`12px 16px`, raio `4px`), alternando entre par verde homologado (`#DCF2E4` / `#14532D`) e par vermelhão suave (`#FDF2F2` / `#6E1414`, borda `#B92525`).

### Navigation
- **Divisórias de Borda do Fichário:** No desktop, pilha vertical contínua de 4 abas (`writing-mode: vertical-rl`, `Archivo` `0.75rem`, peso `700`, `"wdth" 86`, `letter-spacing: 0.06em`, `min-height: 132px`, `width: 52px`) com ícone SVG de `18px` e contador entre parênteses em `JetBrains Mono`. Cada aba exibe permanentemente a cor da sua comissão; a aba ativa alarga para `58px` em `90ms steps(2)` e funde-se à prancha de fundo. No smartphone (`< 768px`), converte-se em barra horizontal (`writing-mode: horizontal-tb`, `min-height: 56px`, `0.6875rem`) com fundo `#F6F4EC` para abas inativas e preenchimento colorido sólido apenas na aba ativa.

### Die-Cut Tray Checklist & Vermilion Safety Slip
- **Checklist de Bandeja Perfurado:** Lista de botões de largura total (`min-height: 44px`, fundo `#FBF9F4`, borda `1px solid #C7C2B4`, raio `4px`, padding `6px 11px`) precedidos por um disco de `17px` (`border: 1.5px solid #3A423F`, fundo `#FFFFFF`). Ao marcar (`aria-pressed="true"`), a linha recua para `#EAE6D9` e o disco é "vazado" com a cor da prancha ativa (`--board-color`) e sombra interna `--shadow-hole`.
- **Tarja Vermelhão de Biossegurança (CCIH):** Bloco incompressível (`flex-shrink: 0`) na base da folha normativa com fundo `#B92525`, texto `#FFFFFF`, raio `8px` e padding `11px 15px`, exibindo título com ícone de alerta e grade dupla (`1fr 1fr`, coluna única abaixo de `1160px`) de regras críticas marcadas por pontos circulares claros de `5px`.

## Do's and Don'ts

### Do:
- **Do** manter toda leitura e interação sobre a folha única de acetato leitoso (`rgba(246, 244, 236, 0.95)`), separando zonas internas com fios secos de `1px` (`#C7C2B4`) e `1.5px` (`#181B1A`).
- **Do** vincular a cor da prancha ativa (`--board-color`) simultaneamente ao fundo do palco, aos furos vazados de encadernação, aos discos marcados da bandeja e aos botões primários.
- **Do** exibir código oficial (`POP.ENF.001`), setor e versão em `JetBrains Mono` tabular no topo de toda resposta ou folha assistencial, mantendo a tarja vermelhão (`#B92525`) visível sem rolagem na abertura desktop (`1440×900`).
- **Do** preservar altura mínima de `44px` em todos os botões, itens de índice rápido, checklists de bandeja e campos de formulário, usando chaveamento seco de `90ms steps(2)` para estados interativos.

### Don't:
- **Don't** introduzir bolhas de chat flutuantes, avatares de robô, fundos cinza/azul de SaaS genérico ou sombras externas em cartões, tabelas e botões dentro da folha.
- **Don't** usar o vermelhão de biossegurança (`#B92525`) em abas de navegação, emblemas decorativos ou botões secundários fora de alertas críticos da CCIH e recusas seguras.
- **Don't** aplicar a fonte serifada `Spectral` em controles de interface ou tabelas, nem remover a condensação `"wdth" 86` dos títulos e abas divisórias.
- **Don't** criar cartões de KPI engaiolados com sombras no painel analítico; mantenha indicadores e rankings pautados diretamente sobre a folha como um livro de registro hospitalar.
