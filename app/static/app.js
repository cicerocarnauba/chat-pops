(() => {
  const state = {
    pops: [],
    currentPop: null,
    checkedByPop: JSON.parse(sessionStorage.getItem('chatPopsTray') || '{}'),
    geminiKey: sessionStorage.getItem('chatPopsGeminiKey') || '',
  };

  const ICON_ARROW_RIGHT = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.75" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

  const els = {
    tabs: document.querySelectorAll('.fore-tab'),
    views: {
      consulta: document.getElementById('view-consulta'),
      catalogo: document.getElementById('view-catalogo'),
      importar: document.getElementById('view-importar'),
      lacunas: document.getElementById('view-lacunas'),
    },
    mobileSectionLabel: document.getElementById('mobile-section-label'),
    mobileModePill: document.getElementById('mobile-mode-pill'),
    btnToggleKey: document.getElementById('btn-toggle-key'),
    keyDrawer: document.getElementById('painel-api-key'),
    inputKey: document.getElementById('input-gemini-key'),
    btnSaveKey: document.getElementById('btn-save-key'),
    keyStatusNote: document.getElementById('key-status-note'),
    chatFeed: document.getElementById('chat-feed'),
    quickPopList: document.getElementById('quick-pop-list'),
    formChat: document.getElementById('form-chat'),
    inputPergunta: document.getElementById('input-pergunta'),
    btnEnviarChat: document.getElementById('btn-enviar-chat'),
    btnEnviarLabel: document.getElementById('btn-enviar-label'),
    protocolSheet: document.getElementById('protocol-sheet'),

    specCodigo: document.getElementById('spec-codigo'),
    specStatus: document.getElementById('spec-status'),
    specTitulo: document.getElementById('spec-titulo'),
    specSub: document.getElementById('spec-sub'),
    specObjetivo: document.getElementById('spec-objetivo'),
    specBilateral: document.getElementById('spec-bilateral'),
    specMateriais: document.getElementById('spec-materiais'),
    specPassos: document.getElementById('spec-passos'),
    specAlertasBox: document.getElementById('spec-alertas-box'),
    specAlertas: document.getElementById('spec-alertas'),
    trayProgress: document.getElementById('tray-progress'),
    btnResetTray: document.getElementById('btn-reset-tray'),

    gapSheet: document.getElementById('gap-refusal-sheet'),
    gapText: document.getElementById('gap-refusal-text'),
    gapTerm: document.getElementById('gap-term-value'),
    gapCount: document.getElementById('gap-count-value'),
    btnCreateFromGap: document.getElementById('btn-create-from-gap'),
    btnViewGapsFromRefusal: document.getElementById('btn-view-gaps-from-refusal'),

    filtroTermo: document.getElementById('filtro-termo'),
    filtroSetor: document.getElementById('filtro-setor'),
    filtroInativos: document.getElementById('filtro-inativos'),
    catalogGrid: document.getElementById('catalog-grid'),
    btnIrNovoPop: document.getElementById('btn-ir-novo-pop'),

    inputArquivoPop: document.getElementById('input-arquivo-pop'),
    formNovoPop: document.getElementById('form-novo-pop'),
    formFeedback: document.getElementById('form-pop-feedback'),
    btnPreencherExemplo: document.getElementById('btn-preencher-exemplo'),
    btnSalvarPop: document.getElementById('btn-salvar-pop'),
    btnSalvarPopLabel: document.getElementById('btn-salvar-pop-label'),

    kpiCobertura: document.getElementById('kpi-cobertura'),
    kpiConsultas: document.getElementById('kpi-consultas'),
    kpiAtivos: document.getElementById('kpi-ativos'),
    kpiLatencia: document.getElementById('kpi-latencia'),
    tabelaLacunas: document.getElementById('tabela-lacunas'),
    tabelaMaisBuscados: document.getElementById('tabela-mais-buscados'),
    tabelaLogs: document.getElementById('tabela-logs'),
    btnAtualizarAnalytics: document.getElementById('btn-atualizar-analytics'),
    tabCountPops: document.getElementById('tab-count-pops'),
    tabCountGaps: document.getElementById('tab-count-gaps'),
  };

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str ?? '';
    return div.innerHTML;
  }

  function scrollProtocolOnMobile() {
    if (window.innerWidth < 768 && els.protocolSheet) {
      els.protocolSheet.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function activateSection(sectionName) {
    els.tabs.forEach((btn) => {
      const active = btn.dataset.target === sectionName;
      btn.classList.toggle('is-active', active);
      if (active) {
        document.documentElement.style.setProperty('--board-color', btn.dataset.board);
        document.documentElement.dataset.section = sectionName;
        els.mobileSectionLabel.textContent = btn.dataset.label || sectionName;
      }
    });

    Object.entries(els.views).forEach(([key, sectionEl]) => {
      const match = key === sectionName;
      sectionEl.hidden = !match;
      sectionEl.classList.toggle('is-active', match);
    });

    if (sectionName === 'catalogo') {
      carregarCatalogo();
    } else if (sectionName === 'lacunas') {
      carregarAnalytics();
    }
  }

  function syncKeyNote() {
    if (state.geminiKey) {
      els.keyStatusNote.textContent = 'Modo atual: Google Gemini API + Function Calling SQL ativo.';
      els.mobileModePill.textContent = 'IA + SQL';
    } else {
      els.keyStatusNote.textContent = 'Modo atual: SQL Determinístico Offline (RNF05).';
      els.mobileModePill.textContent = 'SQL Ativo';
    }
  }

  function saveTrayState() {
    sessionStorage.setItem('chatPopsTray', JSON.stringify(state.checkedByPop));
  }

  function renderProtocolSheet(pop, latencyMs = null) {
    state.currentPop = pop;
    els.gapSheet.hidden = true;
    els.specObjetivo.hidden = false;
    els.specBilateral.hidden = false;
    els.specAlertasBox.hidden = false;

    els.specCodigo.textContent = pop.codigo;
    els.specStatus.textContent = pop.status;
    els.specStatus.className = `status-stamp ${pop.status === 'ATIVO' ? 'is-active' : 'is-review'}`;
    els.specTitulo.textContent = pop.titulo;
    const latLabel = latencyMs !== null ? ` · Consulta SQL em ${latencyMs}ms` : '';
    els.specSub.textContent = `${pop.setor} · Versão ${pop.versao}${latLabel}`;
    els.specObjetivo.textContent = pop.objetivo;

    const checkedSet = new Set(state.checkedByPop[pop.codigo] || []);
    els.specMateriais.innerHTML = '';
    pop.materiais_lista.forEach((item, idx) => {
      const li = document.createElement('li');
      const isPunched = checkedSet.has(idx);
      li.className = `punch-item${isPunched ? ' is-punched' : ''}`;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.setAttribute('aria-pressed', String(isPunched));
      btn.innerHTML = `<span class="die-cut-circle" aria-hidden="true"></span><span>${escapeHtml(item)}</span>`;
      btn.addEventListener('click', () => {
        const current = new Set(state.checkedByPop[pop.codigo] || []);
        if (current.has(idx)) {
          current.delete(idx);
        } else {
          current.add(idx);
        }
        state.checkedByPop[pop.codigo] = Array.from(current);
        saveTrayState();
        renderProtocolSheet(pop, latencyMs);
      });
      li.appendChild(btn);
      els.specMateriais.appendChild(li);
    });

    els.trayProgress.textContent = `${checkedSet.size}/${pop.materiais_lista.length} marcados`;

    els.specPassos.innerHTML = pop.passos_lista
      .map((passo, idx) => {
        const num = String(idx + 1).padStart(2, '0');
        return `<li><span class="step-idx">${num}.</span><span>${escapeHtml(passo)}</span></li>`;
      })
      .join('');

    els.specAlertas.innerHTML = pop.alertas_lista
      .map((alerta) => `<li>${escapeHtml(alerta)}</li>`)
      .join('');

    renderQuickIndex();
  }

  function renderGapRefusal(chatRes) {
    state.currentPop = null;
    els.specCodigo.textContent = 'SEM POP ATIVO';
    els.specStatus.textContent = 'LACUNA RF03';
    els.specStatus.className = 'status-stamp is-review';
    els.specTitulo.textContent = 'Orientação Clínica Bloqueada por Segurança';
    els.specSub.textContent = `Auditoria gravada em ${chatRes.latencia_ms}ms · Fila da CCIH atualizada`;

    els.specObjetivo.hidden = true;
    els.specBilateral.hidden = true;
    els.specAlertasBox.hidden = true;
    els.gapSheet.hidden = false;

    els.gapText.textContent = chatRes.resposta.replace(/\*\*/g, '').replace(/`/g, '');
    els.gapTerm.textContent = chatRes.lacuna_registrada || 'procedimento não homologado';
    els.gapCount.textContent = `${chatRes.total_buscas_lacuna || 1} solicitações`;

    renderQuickIndex();
  }

  function appendChatTurn(pergunta, chatRes) {
    const userEl = document.createElement('article');
    userEl.className = 'chat-turn turn-user';
    userEl.innerHTML = `<p>“${escapeHtml(pergunta)}”</p>`;

    const botEl = document.createElement('article');
    botEl.className = 'chat-turn turn-assistant';
    const tag = chatRes.foi_encontrado && chatRes.pop_citado
      ? `SQL VERIFICADO · ${escapeHtml(chatRes.pop_citado.codigo)}`
      : 'RECUSA SEGURA · LACUNA CCIH';
    const cleanText = chatRes.resposta.replace(/\*\*/g, '').replace(/`/g, '');
    const lgpdHtml = chatRes.aviso_lgpd
      ? `<p class="helper-note">${escapeHtml(chatRes.aviso_lgpd)}</p>`
      : '';

    botEl.innerHTML = `
      <div class="turn-meta">
        <span class="mono-tag">${tag}</span>
        <span class="mono-muted">${chatRes.latencia_ms}ms</span>
      </div>
      <p>${escapeHtml(cleanText)}</p>
      ${lgpdHtml}
    `;

    els.chatFeed.appendChild(userEl);
    els.chatFeed.appendChild(botEl);
    els.chatFeed.scrollTop = els.chatFeed.scrollHeight;
  }

  function renderQuickIndex() {
    const ativos = state.pops.filter((p) => p.status === 'ATIVO');
    els.quickPopList.innerHTML = '';
    ativos.slice(0, 5).forEach((pop) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      const selected = state.currentPop && state.currentPop.codigo === pop.codigo;
      btn.className = `quick-item${selected ? ' is-selected' : ''}`;
      btn.innerHTML = `<span class="quick-item-text">${escapeHtml(pop.codigo)} · ${escapeHtml(pop.titulo)}</span>${ICON_ARROW_RIGHT}`;
      btn.addEventListener('click', () => {
        renderProtocolSheet(pop);
        scrollProtocolOnMobile();
      });
      els.quickPopList.appendChild(btn);
    });
  }

  async function carregarPopsIniciais() {
    const res = await fetch('/api/v1/pops?incluir_inativos=true');
    if (!res.ok) return;
    state.pops = await res.json();
    const ativos = state.pops.filter((p) => p.status === 'ATIVO');
    els.tabCountPops.textContent = String(ativos.length);
    if (!state.currentPop && ativos.length > 0) {
      const inicial = ativos.find((p) => p.codigo === 'POP.ENF.001') || ativos[0];
      renderProtocolSheet(inicial, 18);
    } else {
      renderQuickIndex();
    }
  }

  async function carregarCatalogo() {
    const params = new URLSearchParams();
    if (els.filtroTermo.value.trim()) params.set('termo', els.filtroTermo.value.trim());
    if (els.filtroSetor.value) params.set('setor', els.filtroSetor.value);
    params.set('incluir_inativos', String(els.filtroInativos.checked));

    const res = await fetch(`/api/v1/pops?${params.toString()}`);
    if (!res.ok) return;
    const lista = await res.json();

    if (lista.length === 0) {
      els.catalogGrid.innerHTML = `
        <article class="pop-card">
          <h3>Nenhum protocolo corresponde ao filtro</h3>
          <p>Ajuste os termos de pesquisa ou cadastre uma nova folha homologada na divisória de importação.</p>
        </article>
      `;
      return;
    }

    els.catalogGrid.innerHTML = '';
    lista.forEach((pop) => {
      const card = document.createElement('article');
      const isAtivo = pop.status === 'ATIVO';
      card.className = `pop-card${isAtivo ? '' : ' is-inactive'}`;
      card.innerHTML = `
        <div class="pop-card-top">
          <span class="code-stamp">${escapeHtml(pop.codigo)}</span>
          <span class="status-stamp ${isAtivo ? 'is-active' : 'is-review'}">${escapeHtml(pop.status)}</span>
        </div>
        <h3>${escapeHtml(pop.titulo)}</h3>
        <p>${escapeHtml(pop.objetivo)}</p>
        <div class="pop-card-foot">
          <span>${escapeHtml(pop.setor)} · ${escapeHtml(pop.versao)}</span>
          ${isAtivo ? `<button type="button" class="btn-outline-sm"><span>Abrir Folha</span>${ICON_ARROW_RIGHT}</button>` : '<span>Bloqueado no Chat (RN02)</span>'}
        </div>
      `;
      const openBtn = card.querySelector('button');
      if (openBtn) {
        openBtn.addEventListener('click', () => {
          activateSection('consulta');
          renderProtocolSheet(pop);
          scrollProtocolOnMobile();
        });
      }
      els.catalogGrid.appendChild(card);
    });
  }

  async function carregarAnalytics() {
    const res = await fetch('/api/v1/analytics/resumo');
    if (!res.ok) return;
    const data = await res.json();

    els.kpiCobertura.textContent = `${data.taxa_cobertura_percentual}%`;
    els.kpiConsultas.textContent = String(data.total_consultas);
    els.kpiAtivos.textContent = `${data.total_pops_ativos} / ${data.total_pops_revisao}`;
    els.kpiLatencia.textContent = `${data.latencia_media_ms}ms`;
    els.tabCountGaps.textContent = String(data.total_lacunas_distintas);

    els.tabelaLacunas.innerHTML = data.lacunas_prioritarias.length
      ? data.lacunas_prioritarias
          .map(
            (lac) => `
          <tr>
            <td>
              <strong>${escapeHtml(lac.termo_buscado)}</strong>
              <div class="mono-muted">${escapeHtml(lac.pergunta_exemplo)}</div>
            </td>
            <td><strong>${lac.quantidade_buscas}x</strong></td>
            <td><button type="button" class="btn-outline-sm" data-gap-title="${escapeHtml(lac.termo_buscado)}"><span>Criar POP</span>${ICON_ARROW_RIGHT}</button></td>
          </tr>
        `
          )
          .join('')
      : '<tr><td colspan="3">Nenhuma lacuna pendente registrada.</td></tr>';

    els.tabelaLacunas.querySelectorAll('[data-gap-title]').forEach((btn) => {
      btn.addEventListener('click', () => {
        preencherRascunhoDeLacuna(btn.dataset.gapTitle || '');
      });
    });

    els.tabelaMaisBuscados.innerHTML = data.pops_mais_buscados.length
      ? data.pops_mais_buscados
          .map(
            (item) => `
          <tr>
            <td>
              <strong>${escapeHtml(item.codigo)}</strong>
              <div>${escapeHtml(item.titulo)}</div>
            </td>
            <td>${escapeHtml(item.setor)}</td>
            <td><strong>${item.total_consultas}x</strong></td>
          </tr>
        `
          )
          .join('')
      : '<tr><td colspan="3">Sem acessos contabilizados.</td></tr>';

    els.tabelaLogs.innerHTML = data.ultimos_logs.length
      ? data.ultimos_logs
          .map(
            (log) => `
          <tr>
            <td>${escapeHtml(log.pergunta)}</td>
            <td><span class="mono-tag">${log.foi_encontrado ? escapeHtml(log.codigo_pop_retornado || 'ATIVO') : 'LACUNA RF03'}</span></td>
            <td>${log.latencia_ms}ms</td>
          </tr>
        `
          )
          .join('')
      : '<tr><td colspan="3">Sem consultas registradas nesta sessão.</td></tr>';
  }

  function preencherRascunhoDeLacuna(termo) {
    const cleanTerm = termo.replace(/\[demo\]/gi, '').trim();
    activateSection('importar');
    const proximoNum = String(state.pops.length + 1).padStart(3, '0');
    document.getElementById('pop-codigo').value = `POP.ENF.${proximoNum}`;
    document.getElementById('pop-titulo').value = cleanTerm
      .split(' ')
      .filter(Boolean)
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ');
    document.getElementById('pop-chaves').value = cleanTerm;
    document.getElementById('pop-titulo').focus();
  }

  function mostrarFeedbackForm(msg, ok) {
    els.formFeedback.hidden = false;
    els.formFeedback.textContent = msg;
    els.formFeedback.className = `feedback-banner ${ok ? 'is-ok' : 'is-err'}`;
  }

  els.tabs.forEach((btn) => {
    btn.addEventListener('click', () => activateSection(btn.dataset.target));
  });

  els.btnToggleKey.addEventListener('click', () => {
    const expanded = els.btnToggleKey.getAttribute('aria-expanded') === 'true';
    els.btnToggleKey.setAttribute('aria-expanded', String(!expanded));
    els.keyDrawer.hidden = expanded;
  });

  els.inputKey.value = state.geminiKey;
  syncKeyNote();

  els.btnSaveKey.addEventListener('click', () => {
    state.geminiKey = els.inputKey.value.trim();
    sessionStorage.setItem('chatPopsGeminiKey', state.geminiKey);
    syncKeyNote();
    els.keyDrawer.hidden = true;
    els.btnToggleKey.setAttribute('aria-expanded', 'false');
  });

  els.btnResetTray.addEventListener('click', () => {
    if (!state.currentPop) return;
    delete state.checkedByPop[state.currentPop.codigo];
    saveTrayState();
    renderProtocolSheet(state.currentPop);
  });

  els.formChat.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const pergunta = els.inputPergunta.value.trim();
    if (!pergunta) return;

    els.btnEnviarChat.disabled = true;
    els.btnEnviarChat.setAttribute('aria-busy', 'true');
    els.btnEnviarLabel.textContent = 'Consultando…';
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (state.geminiKey) {
        headers['X-Gemini-Api-Key'] = state.geminiKey;
      }
      const res = await fetch('/api/v1/chat', {
        method: 'POST',
        headers,
        body: JSON.stringify({ pergunta }),
      });
      if (!res.ok) throw new Error('Falha ao consultar a base de protocolos.');
      const data = await res.json();

      appendChatTurn(pergunta, data);
      els.inputPergunta.value = '';

      if (data.foi_encontrado && data.pop_citado) {
        renderProtocolSheet(data.pop_citado, data.latencia_ms);
      } else {
        renderGapRefusal(data);
        carregarAnalytics();
      }
      scrollProtocolOnMobile();
    } catch (err) {
      appendChatTurn(pergunta, {
        foi_encontrado: false,
        latencia_ms: 0,
        resposta: 'Erro de comunicação com o servidor local. Verifique a conexão e tente novamente.',
      });
    } finally {
      els.btnEnviarChat.disabled = false;
      els.btnEnviarChat.removeAttribute('aria-busy');
      els.btnEnviarLabel.textContent = 'Abrir Folha';
    }
  });

  els.btnCreateFromGap.addEventListener('click', () => {
    preencherRascunhoDeLacuna(els.gapTerm.textContent || '');
  });

  els.btnViewGapsFromRefusal.addEventListener('click', () => {
    activateSection('lacunas');
  });

  els.btnIrNovoPop.addEventListener('click', () => activateSection('importar'));
  els.filtroTermo.addEventListener('input', carregarCatalogo);
  els.filtroSetor.addEventListener('change', carregarCatalogo);
  els.filtroInativos.addEventListener('change', carregarCatalogo);
  els.btnAtualizarAnalytics.addEventListener('click', carregarAnalytics);

  els.inputArquivoPop.addEventListener('change', async () => {
    const file = els.inputArquivoPop.files?.[0];
    if (!file) return;
    const fd = new FormData();
    fd.append('arquivo', file);
    try {
      const res = await fetch('/api/v1/pops/extrair-arquivo', { method: 'POST', body: fd });
      if (!res.ok) throw new Error('Não foi possível extrair os campos do arquivo.');
      const draft = await res.json();
      document.getElementById('pop-codigo').value = draft.codigo || '';
      document.getElementById('pop-setor').value = draft.setor || 'Divisão de Enfermagem';
      document.getElementById('pop-versao').value = draft.versao || 'v1.0 - 2026';
      document.getElementById('pop-status').value = draft.status || 'ATIVO';
      document.getElementById('pop-titulo').value = draft.titulo || '';
      document.getElementById('pop-chaves').value = draft.palavras_chave || '';
      document.getElementById('pop-objetivo').value = draft.objetivo || '';
      document.getElementById('pop-materiais').value = draft.materiais || '';
      document.getElementById('pop-passos').value = draft.passos_execucao || '';
      document.getElementById('pop-alertas').value = draft.alertas_seguranca || '';
      mostrarFeedbackForm(`Arquivo "${file.name}" importado para revisão antes de gravar no SQL.`, true);
    } catch (err) {
      mostrarFeedbackForm(err.message || 'Erro ao ler arquivo.', false);
    }
  });

  els.btnPreencherExemplo.addEventListener('click', () => {
    const proximo = String(state.pops.length + 1).padStart(3, '0');
    document.getElementById('pop-codigo').value = `POP.CCIH.${proximo}`;
    document.getElementById('pop-setor').value = 'CCIH';
    document.getElementById('pop-versao').value = 'v1.0 - 2026 [DEMO]';
    document.getElementById('pop-status').value = 'ATIVO';
    document.getElementById('pop-titulo').value = 'Coleta de Hemocultura Pareada Periférica';
    document.getElementById('pop-chaves').value = 'hemocultura, pareada, sepse, febre, frasco aerobio, bacteremia';
    document.getElementById('pop-objetivo').value = 'Padronizar a coleta asséptica de duas amostras sanguíneas independentes para diagnóstico microbiológico de corrente sanguínea sem contaminação de microbiota cutânea.';
    document.getElementById('pop-materiais').value = 'Luvas estéreis e máscara\nClorexidina alcoólica 0,5% e álcool 70%\n2 pares de frascos de hemocultura identificados\nSeringas estéreis de 20 mL e dispositivo scalp estéril';
    document.getElementById('pop-passos').value = '1. Conferir pedido médico e desinfetar o septo de borracha dos frascos com álcool 70%, aguardando secar.\n2. Higienizar as mãos, realizar antissepsia rigorosa com clorexidina alcoólica 0,5% em sítios anatômicos distintos e aguardar 30s.\n3. Coletar 8 a 10 mL por frasco adulto em duas punções periféricas independentes antes da primeira dose de antimicrobiano.';
    document.getElementById('pop-alertas').value = 'Nunca refrigerar os frascos após a coleta; encaminhar ao laboratório de microbiologia em temperatura ambiente em até 2 horas.\nProibido coletar hemocultura diretamente de cateter periférico já instalado há horas.';
    mostrarFeedbackForm('Rascunho demonstrativo carregado. Clique em Homologar e Gravar no SQL.', true);
  });

  els.formNovoPop.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const payload = {
      codigo: document.getElementById('pop-codigo').value.trim(),
      setor: document.getElementById('pop-setor').value.trim(),
      versao: document.getElementById('pop-versao').value.trim(),
      status: document.getElementById('pop-status').value,
      titulo: document.getElementById('pop-titulo').value.trim(),
      palavras_chave: document.getElementById('pop-chaves').value.trim(),
      objetivo: document.getElementById('pop-objetivo').value.trim(),
      materiais: document.getElementById('pop-materiais').value.trim(),
      passos_execucao: document.getElementById('pop-passos').value.trim(),
      alertas_seguranca: document.getElementById('pop-alertas').value.trim(),
    };

    els.btnSalvarPop.disabled = true;
    els.btnSalvarPop.setAttribute('aria-busy', 'true');
    els.btnSalvarPopLabel.textContent = 'Gravando…';
    try {
      const res = await fetch('/api/v1/pops', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const body = await res.json();
      if (!res.ok) {
        throw new Error(body.detail || 'Verifique os campos obrigatórios (mínimo de caracteres) e tente novamente.');
      }
      await carregarPopsIniciais();
      els.formNovoPop.reset();
      mostrarFeedbackForm(`Protocolo ${body.codigo} gravado com sucesso na base SQL oficial!`, true);
      if (body.status === 'ATIVO') {
        renderProtocolSheet(body);
      }
    } catch (err) {
      mostrarFeedbackForm(err.message || 'Falha ao cadastrar protocolo.', false);
    } finally {
      els.btnSalvarPop.disabled = false;
      els.btnSalvarPop.removeAttribute('aria-busy');
      els.btnSalvarPopLabel.textContent = 'Homologar e Gravar no SQL';
    }
  });

  carregarPopsIniciais();
  carregarAnalytics();
})();
