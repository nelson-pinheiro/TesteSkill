"""T14 Administração: T14.01 a T14.07 (seção 12.5) e subvisões T14.04.01 a T14.04.07 (seção 5.6)."""
from shell import *


def adm(code, nome, tablist, tab, body, sub, tecnico=False, acts=None):
    kw = dict(perfil="Administrador técnico", unidade="GERTIC", nome="E. Tavares", ini="ET") if tecnico else {}
    aviso = alert("info", "Tela do administrador técnico", "Exibida no perfil correspondente. A função técnica não concede validação de atos nem acesso irrestrito a documentos de negócio (CP04).") if tecnico else None
    return page(f"{code} {nome}", "admin", ["Administração", f"{code} {nome}", tab] if tab else ["Administração", f"{code} {nome}"],
                [aviso, *body], tabs_=tabs(tablist, tab) if tablist else None, sub=sub, acts=acts, h1=f"{code} {nome}", **kw)


# ---------------------------------------------------------------- T14.01
@screen("T1401-Usuarios.dc.html", "T14.01 Usuários", "r09", "T14.01")
def t1401u():
    us = [["msilva", "M. Silva", "m.silva@[domínio institucional]", estado("Validado", "green"), "M. Silva", "GERAD — Coordenador (01/01/2026 –) · DIRAF — Consulta (– 31/12/2026)"],
          ["rcosta", "R. Costa", "r.costa@[domínio institucional]", estado("Validado", "green"), "R. Costa", "GERAD — Operador contratual (01/01/2026 –)"],
          ["lmartins", "L. Martins", "l.martins@[domínio institucional]", estado("Validado", "green"), "L. Martins", "DIRAF — Operador financeiro (01/01/2026 –)"],
          ["jprado", "J. Prado", "j.prado@[domínio institucional]", estado("Validado", "green"), "J. Prado", "GERAD — Gestor ou fiscal designado (01/05/2026 –)"],
          ["hrocha", "H. Rocha", "h.rocha@[domínio institucional]", badge("Inativo", "gray"), "H. Rocha", "Vínculo revogado em 30/04/2026 (motivo: remoção)"]]
    vinc = section("Vínculo selecionado — R. Costa", form_grid(
        field("Unidade", kind="select", options=["GERAD"]), field("Perfil", kind="select", options=["Operador contratual"]), field("Vigente de", "01/01/2026", kind="date"),
        field("Vigente até", "", kind="date", placeholder="Indeterminado"), field("Autorizador", "M. Silva (coordenadora)", ro=True), field("Motivo", "Lotação na GERAD", req=True)),
        actions(btn("Salvar vínculo", kind="primary"), btn("Revogar vínculo", kind="danger")),
        small("Revogar impede novos acessos, downloads e entregas (CP02). Vínculos da mesma pessoa, unidade e perfil não se sobrepõem."), h=3)
    return adm("T14.01", "Usuários, perfis e unidades", T1401_TABS, "Usuários",
               [listbar(5, 0), table(["Login institucional", "Nome", "E-mail", "Ativo", "Pessoa vinculada", "Vínculos unidade–perfil"], us, dense=True), vinc,
                alert("info", "Negação por padrão", "Sem vínculo vigente, nada da carteira é exibido (T00). Uma pessoa pode acumular perfis mediante autorização registrada.")],
               "Usuário, vínculos unidade–perfil com vigência, autorizador e motivo.", tecnico=True, acts=[btn("Novo usuário", kind="primary", ico="plus"), btn("Novo vínculo")])


MATRIZ = [("Visualizar carteira e fichas", "S", "S", "S", "D", "S", "—"), ("Cadastrar ou editar rascunho contratual", "S", "S", "—", "—", "—", "—"),
          ("Validar cadastro, vigência e alterações", "S", "—", "—", "—", "—", "—"), ("Formalizar alteração (T04.01)", "S", "—", "—", "—", "—", "—"),
          ("Registrar empenhos, liquidações e pagamentos", "—", "—", "S", "—", "—", "—"), ("Validar movimentos financeiros", "S", "—", "S (por outro usuário)", "—", "—", "—"),
          ("Criar e atualizar providências", "S", "S", "S", "D", "—", "—"), ("Criar ou alterar cenário simulado", "S", "S", "S", "—", "—", "—"),
          ("Registrar solicitação de reforço", "S", "—", "S", "—", "—", "—"), ("Registrar ciência de notificação própria", "S", "S", "S", "D", "S", "S"),
          ("Confirmar ou alterar prioridade", "S", "—", "—", "—", "—", "—"), ("Registrar pendência que afete pagamento", "S", "S", "S", "D", "—", "—"),
          ("Exportar relatórios", "S", "S", "S", "D", "S", "—"), ("Consultar trilha de auditoria", "S", "—", "—", "—", "S", "Técnica"),
          ("Configurar notificações e parâmetros internos", "S", "—", "—", "—", "—", "Técnica"), ("Gerir usuários e vínculos", "—", "—", "—", "—", "—", "S"),
          ("Importar e aprovar lotes; decidir divergências", "S (aprovar e decidir)", "S (preparar)", "S (preparar, financeiro)", "—", "—", "—"),
          ("Registrar atos de designação, designações e afastamentos", "S", "S", "—", "—", "—", "—"), ("Emitir relatório de conformidade (RPT15)", "S", "—", "—", "—", "S", "—"),
          ("Visualizar identificadores pessoais sem máscara", "S", "—", "—", "—", "—", "—")]


@screen("T1401-Perfis.dc.html", "T14.01 Perfis e permissões", "r09", "T14.01")
def t1401p():
    def cell(v):
        if v == "—":
            return span("—", style=f"color:{FAINT};")
        return badge(v, "green" if v.startswith("S") else ("blue" if v == "D" else "purple"))
    rows = [[acao] + [cell(v) for v in vs] for acao, *vs in MATRIZ]
    return adm("T14.01", "Usuários, perfis e unidades", T1401_TABS, "Perfis e permissões",
               [row(small("Legenda:"), badge("S", "green"), small("no escopo da unidade"), badge("D", "blue"), small("apenas nos contratos em que é designado"),
                    span("—", style=f"color:{FAINT};"), small("não permitido"), badge("Técnica", "purple"), small("função técnica"), gap=6),
                table(["Ação", "Coordenador", "Op. contratual", "Op. financeiro", "Gestor/fiscal", "Consulta/controle interno", "Adm. técnico"], rows, minw=1100, dense=True),
                small("Matriz gravada no banco (seg.perfil_permissao) e alterável aqui, sem mudança de código. Seis perfis e vinte permissões (seção 10.2).")],
               "Matriz perfil × ação da seção 10.2.", tecnico=True, acts=[btn("Editar matriz", ico="edit")])


@screen("T1401-Unidades.dc.html", "T14.01 Unidades", "r09", "T14.01")
def t1401n():
    rows = [["RIOPREV", "Rioprevidência", "—", "01/01/2020 –"], ["DIRAF", "Diretoria Administrativo-Financeira", "RIOPREV", "01/01/2020 –"],
            ["GERAD", "Gerência Administrativa", "DIRAF", "01/01/2020 –"], ["GERTIC", "Gerência de Tecnologia", "DIRAF", "01/01/2020 –"],
            ["CHEGAB", "Chefia de Gabinete", "RIOPREV", "01/01/2020 –"], ["DIRSE", "Diretoria de Seguridade", "RIOPREV", "01/01/2020 –"],
            ["GERPAT", "Gerência de Patrimônio (extinta)", "DIRAF", "01/01/2020 – 31/12/2024"]]
    return adm("T14.01", "Usuários, perfis e unidades", T1401_TABS, "Unidades",
               [listbar(7, 0), table(["Sigla", "Nome", "Unidade superior", "Vigência"], rows, dense=True), small("Siglas e estrutura fictícias. Inativar não elimina histórico.")],
               "Unidades com vigência e unidade superior.", tecnico=True, acts=[btn("Nova unidade", kind="primary", ico="plus")])


# ---------------------------------------------------------------- T14.02
@screen("T1402-Categorias.dc.html", "T14.02 Categorias e grupos", "r09", "T14.02")
def t1402c():
    return adm("T14.02", "Cadastros auxiliares e parâmetros", T1402_TABS, "Categorias e grupos", [
        grid(section("Categorias e grupos", table(["Categoria", "Grupos", "Situação"], [["Serviços prediais", "Manutenção · Limpeza · Segurança contra incêndio", "Ativa"],
                                                                                        ["Tecnologia da informação", "Sustentação · Licenças · Telecomunicações", "Ativa"],
                                                                                        ["Comunicação", "Monitoramento de mídia", "Ativa"], ["Suprimentos", "Expediente", "Ativa"],
                                                                                        ["Eventos", "Eventos institucionais", "Inativa (histórico preservado)"]], dense=True), h=3),
             section("Categorias de providência", table(["Código", "Nome"], [["prorrogacao", "Prorrogação"], ["substituicao", "Contratação substitutiva"], ["reforco_empenho", "Reforço de empenho"],
                                                                             ["reajuste_alteracao", "Reajuste e demais alterações"], ["garantia", "Atualização de garantia"], ["documento_pendente", "Documento pendente"],
                                                                             ["pagamento_impedido", "Pagamento com impedimento"], ["encerramento", "Providência de encerramento"],
                                                                             ["atestacao_anual", "Atestação anual de créditos e vantagem (art. 106)"], ["designacao", "Designação de gestor, fiscal ou suplente"],
                                                                             ["saneamento_dados", "Saneamento de dados"]], dense=True), h=3), min_=420),
        grid(section("Modalidades", table(["Modalidade", "Prazo PNCP"], [["Pregão eletrônico", "20 dias úteis"], ["Concorrência", "20 dias úteis"], ["Dispensa", "10 dias úteis"], ["Inexigibilidade", "10 dias úteis"]], dense=True), h=3),
             section("Tipos de documento", table(["Tipo", "Restrição padrão"], [["Contrato", "Pública"], ["Termo aditivo", "Pública"], ["Apólice", "Restrita"], ["Relatório de fiscalização", "Interna"]], dense=True), h=3), min_=420),
        small("Inativar não elimina histórico."),
    ], "Categorias, grupos, modalidades, tipos de documento e categorias de providência.", acts=[btn("Novo item", kind="primary", ico="plus")])


@screen("T1402-Etapas.dc.html", "T14.02 Etapas e listas de verificação", "r09", "T14.02")
def t1402e():
    et = [[str(i + 1), n_] for i, n_ in enumerate(["Análise inicial", "Manifestação da contratada", "Instrução documental", "Análise jurídica", "Autorização", "Assinatura", "Publicação"])]
    pr = [["PR01", "Previsão de prorrogação no edital e no contrato, e vigência", "Decreto RJ nº 48.817/2023, art. 22, § 1º, I"], ["PR02", "Manifestação justificada de interesse", "art. 22, § 1º, II"],
          ["PR03", "Consulta à contratada", "art. 22, § 1º, III"], ["PR04", "Resposta da contratada", "art. 22, § 1º, IV"], ["PR05", "Objeto e escopo inalterados", "art. 22, § 1º, V"],
          ["PR06", "Pesquisa de preços (vantajosidade)", "art. 22, § 1º, VI"], ["PR07", "Disponibilidade orçamentária", "art. 22, § 1º, VII"], ["PR08", "Habilitação vigente e regularidade", "art. 22, § 1º, VIII"],
          ["PR09", "Recomendação do gestor (120 dias)", "art. 22, XVII"], ["PR10", "Checklist PGE/RJ e manifestação conclusiva", "art. 22, XIX"],
          ["PR11", "Regularidade fiscal e consultas CEIS/CNEP", "Lei nº 14.133/2021, art. 91, § 4º"], ["PR12", "Sem pedido de reequilíbrio pendente", "Lei nº 14.133/2021, art. 131, parágrafo único"]]
    return adm("T14.02", "Cadastros auxiliares e parâmetros", T1402_TABS, "Etapas e listas de verificação", [
        grid(section("Etapas do procedimento de prorrogação (ordem ordinal — C18)", table(["Ordem", "Etapa"], et, dense=True), small("Etapas acrescidas recebem posição ordinal explícita."), h=3),
             section("Lista de verificação da prorrogação", table(["Item", "Descrição", "Fundamento"], pr, dense=True), h=3), min_=420),
    ], "Etapas por tipo de procedimento, com ordem, e itens de lista de verificação com fundamento.", acts=[btn("Nova etapa", ico="plus"), btn("Novo item", ico="plus")])


@screen("T1402-Parametros.dc.html", "T14.02 Parâmetros internos", "r09", "T14.02")
def t1402p():
    rows = [["C15_ANTECEDENCIA_PRORROGAR", "Geral", "120 dias", "120 dias (art. 22, XVII)", "10/11/2026 –", "Valor inicial igual ao piso regulamentar"],
            ["C15_ANTECEDENCIA_SUBSTITUIR", "Geral", "240 dias", "120 dias", "10/11/2026 –", "Prazo interno para concluir nova contratação"],
            ["C15_ANTECEDENCIA_ENCERRAR", "Geral", "60 dias", "—", "10/11/2026 –", "Providências de encerramento"],
            ["C15_ANTECEDENCIA_ANALISAR", "Geral", "240 dias", "120 dias", "10/11/2026 –", "Hipótese mais demorada até a decisão definitiva"],
            ["N01_ANTECEDENCIAS", "Geral", "180/120/90/60/30 dias", "—", "01/01/2026 –", "Alertas de vencimento"],
            ["N13_ANTECEDENCIA", "Geral", "45 dias da emissão", "Marco legal de 2 meses (art. 137, § 2º, IV)", "01/01/2026 –", "Antes do marco legal"],
            ["C18_LIMIAR_DIAS", "Geral", "90 dias", "—", "01/01/2026 –", "Risco Alto sem etapa ≥ autorização"],
            ["C10_DATA_PADRAO", "Geral", "1º dia da competência", "—", "01/01/2026 –", "Exigência de prévio empenho (Lei nº 4.320/1964, art. 60)"]]
    return adm("T14.02", "Cadastros auxiliares e parâmetros", T1402_TABS, "Parâmetros internos", [
        row(prazo_nat("Parâmetro interno"), small("Parâmetros internos não são prazos legais (seção 4.2)."), gap=8),
        table(["Código", "Escopo", "Valor", "Piso regulamentar", "Vigência", "Justificativa"], rows, minw=1000, dense=True),
        section("Novo valor de parâmetro — escopo contrato 012/2025", form_grid(
            field("Parâmetro", kind="select", options=["C15_ANTECEDENCIA_PRORROGAR"]), field("Escopo", kind="select", options=["Contrato — 012/2025", "Geral", "Categoria"]),
            field("Valor", "60 dias", error="Recusado: abaixo do piso regulamentar de 120 dias (Decreto RJ nº 48.817/2023, art. 22, XVII) — CV07."),
            field("Vigente de", "10/11/2026", kind="date"), field("Justificativa", "Tentativa de reduzir a antecedência", req=True)),
            small("Alteração de parâmetro recalcula avisos futuros."), tone="danger", h=3),
    ], "Parâmetros com escopo (geral, categoria, contrato), vigência, justificativa e piso regulamentar.", acts=[btn("Novo valor", kind="primary", ico="plus")])


@screen("T1402-Regras.dc.html", "T14.02 Regras jurídicas", "r09", "T14.02")
def t1402r():
    rows = [["D48817-22-XVII", "Antecedência da recomendação de prorrogação ou nova licitação", "Decreto RJ nº 48.817/2023, art. 22, XVII", prazo_nat("Legal regulamentar"), "v1", "10/11/2026"],
            ["D48817-22-XIX", "Antecedência do envio à assessoria jurídica", "Decreto RJ nº 48.817/2023, art. 22, XIX", prazo_nat("Legal regulamentar"), "v1", "10/11/2026"],
            ["D48817-7-11", "Prazo máximo sem designação", "Decreto RJ nº 48.817/2023, art. 7º, §§ 10 e 11", prazo_nat("Legal regulamentar"), "v1", "10/11/2026"],
            ["L14133-94", "Divulgação no PNCP como condição de eficácia", "Lei nº 14.133/2021, art. 94", prazo_nat("Legal"), "v1", "10/11/2026"],
            ["L14133-137-2-IV", "Atraso de pagamento superior a 2 meses", "Lei nº 14.133/2021, art. 137, § 2º, IV", prazo_nat("Legal"), "v1", "10/11/2026"]]
    return adm("T14.02", "Cadastros auxiliares e parâmetros", T1402_TABS, "Regras jurídicas",
               [table(["Código", "Tema", "Fundamento", "Natureza", "Versão", "Verificada em"], rows, minw=1000, dense=True),
                small("Quadro normativo com versão e data de verificação; itens a validar pela assessoria jurídica constam da seção 4.4.")],
               "Quadro normativo com versão e data de verificação.", acts=[btn("Nova regra", ico="plus")])


@screen("T1402-Calendario.dc.html", "T14.02 Calendário e índices", "r09", "T14.02")
def t1402k():
    return adm("T14.02", "Cadastros auxiliares e parâmetros", T1402_TABS, "Calendário e índices", [
        grid(section("Feriados e pontos facultativos (L08)", table(["Data", "Descrição", "Abrangência"], [["15/11/2026", "Proclamação da República", "Nacional"], ["20/11/2026", "Dia da Consciência Negra", "Nacional"],
                                                                                                         ["25/12/2026", "Natal", "Nacional"], ["20/01/2027", "São Sebastião", "Municipal (Rio de Janeiro)"]], dense=True),
                     btn("Importar feriados (L08)", href="Importacao.dc.html", small_=True), small("Base da contagem em dias úteis do prazo de divulgação no PNCP (C01)."), h=3),
             section("Séries de índices (L07)", table(["Índice", "Competência", ("Valor", "r"), "Origem"], [["IPCA", "09/2026", "0,44%", origem("Integrado", "Conector de índices", "11/10/2026 03:00")],
                                                                                                         ["IPCA", "08/2026", "0,23%", origem("Importado", "Lote L07", "12/09/2026 10:00")],
                                                                                                         ["IST", "09/2026", "0,31%", origem("Digitado", "L. Martins", "15/10/2026 09:30")]], dense=True),
                     small("Séries por digitação, importação (L07) ou integração, sempre conferíveis."), h=3), min_=420),
    ], "Feriados e séries de índices.")


# ---------------------------------------------------------------- T14.03
EVENTOS = [("N01", "Aproximação do término da vigência", "180/120/90/60/30 dias", "—", "Coordenador após 15 dias"), ("N02", "Prazo para iniciar prorrogação ou substituição", "Na data interna (C15)", "Semanal", "Coordenador"),
           ("N03", "Prorrogação ou substituição sem avanço", "15 dias sem movimentação", "Semanal", "Coordenador"), ("N04", "Aproximação da data-base", "90 dias", "—", "—"),
           ("N05", "Pedido pendente", "Prazo próximo ou 30 dias sem movimentação", "Semanal", "Coordenador"), ("N06", "Insuficiência projetada de empenho", "R > 0 ou cobertura < 2 meses", "—", "Coordenador"),
           ("N07", "Solicitação de reforço pendente", "15 dias antes da data necessária", "Diária", "—"), ("N08", "Vencimento de garantia", "45 dias e no vencimento", "—", "—"),
           ("N09", "Necessidade de atualizar garantia", "Após alteração formalizada", "—", "—"), ("N10", "Providência próxima do prazo ou atrasada", "5 dias, no prazo e diária", "Diária", "Coordenador após 5 dias"),
           ("N11", "Formalização de aditivo ou apostila", "Após registro validado", "—", "—"), ("N12", "Risco de descontinuidade", "Lacuna > 0 ou risco Existente", "Semanal", "Coordenador"),
           ("N13", "Documento fiscal próximo de 2 meses", "45 dias da emissão", "—", "Coordenador"), ("N14", "Designação ausente ou afastamento sem suplente", "45 e 61 dias; início do afastamento", "Semanal", "Coordenador"),
           ("N15", "Marco regulamentar próximo ou descumprido", "30 e 15 dias; no descumprimento", "—", "Coordenador"), ("N16", "Prazo de recebimento", "5 dias e no esgotamento", "—", "—"),
           ("RESUMO", "Resumo periódico das pendências", "Semanal", "—", "—")]


@screen("T1403-Regras.dc.html", "T14.03 Regras por evento", "r09", "T14.03")
def t1403r():
    rows = [[strong(c_), n, cat(div(ant), prazo_nat("Parâmetro interno")), rep, esc_, "Geral"] for c_, n, ant, rep, esc_ in EVENTOS]
    prev = section("Prévia do aviso — N01 (30 dias)", kv([("Assunto", "[Contratos] 012/2025 — término da vigência em 28/11/2026"),
                                                          ("Conteúdo mínimo do e-mail", "Contrato, evento e prazo; link que exige autenticação"),
                                                          ("Destinatários", "Gestor, coordenador e responsável pela providência")]), h=3)
    return adm("T14.03", "Configuração de notificações", T1403_TABS, "Regras por evento",
               [table(["Evento", "Nome", "Antecedência (parâmetro interno)", "Repetição", "Escalonamento", "Escopo"], rows, minw=1100, dense=True), prev,
                small("Antecedências, repetição e escalonamento configuráveis por escopo (geral, unidade, contrato). Os marcos de 60, 120 e 30 dias são regulamentares, não parâmetros internos.")],
               "Eventos N01 a N16 e resumo, com antecedências, repetição, escalonamento e prévia do aviso.", acts=[btn("Editar regra", ico="edit")])


@screen("T1403-Destinatarios.dc.html", "T14.03 Destinatários e canais", "r09", "T14.03")
def t1403d():
    rows = [["N01, N02, N12", "Gestor · coordenador · responsável pela providência", cat(badge("Interna", "blue"), " ", badge("E-mail", "teal")), "Geral"],
            ["N06, N07", "Operador financeiro · coordenador", cat(badge("Interna", "blue"), " ", badge("E-mail", "teal")), "Unidade DIRAF"],
            ["N13, N16", "Gestor · fiscais · operador financeiro", cat(badge("Interna", "blue"), " ", badge("E-mail", "teal")), "Geral"],
            ["N14", "Coordenador · autoridade que autorizou a contratação", badge("Interna", "blue"), "Geral"],
            ["RESUMO", "Cada usuário com pendências", badge("E-mail", "teal"), "Geral"]]
    return adm("T14.03", "Configuração de notificações", T1403_TABS, "Destinatários e canais",
               [table(["Eventos", "Destinatários por responsabilidade", "Canais", "Escopo"], rows, dense=True),
                alert("info", "Canais", "Notificação interna sempre; e-mail quando o serviço estiver configurado, com conteúdo mínimo. Permissões reavaliadas antes de gerar e antes de enviar.")],
               "Destinatários por responsabilidade e canais.")


@screen("T1403-Monitor.dc.html", "T14.03 Monitor do agendador", "r09", "T14.03")
def t1403m():
    return adm("T14.03", "Configuração de notificações", T1403_TABS, "Monitor", [
        grid(stat("Último ciclo do agendador", "10/11/2026 07:00", "concluído em 42 s · sem usuários conectados (CN04)", "green"), stat("Fila", "3 entregas", "e-mail pendente"),
             stat("Falhas nas últimas 24 h", "1", "serviço de e-mail indisponível", "orange"), stat("Avisos gerados no ciclo", "9", "ocorrências deduplicadas"), min_=220),
        table(["Entrega", "Canal", "Tentativas", "Próxima tentativa", "Situação", ""], [["N01 · 012/2025 · P. Nunes", "E-mail", "3", "09:40", badge("Falha", "red"), a("Reenviar", "T1403-Monitor.dc.html")],
                                                                                    ["N15 · 027/2024 · M. Silva", "E-mail", "1", "07:10", badge("Pendente", "yellow"), ""]], dense=True),
        alert("warn", "Falha persistente", "Aparece ao administrador técnico e não impede a notificação interna. Fila parada gera alerta (CO05)."),
    ], "Último ciclo do agendador, fila, falhas e reenvio.", tecnico=True)


# ---------------------------------------------------------------- T14.04
def imp(tab, body, sub, acts=None):
    return adm("T14.04", "Importação e conciliação", T1404_TABS, tab,
               [row(badge("Lote 2026-11-03 · L01", "purple"), small("planilha_acompanhamento_2026.xlsx · hash 9f3c…a21e · responsável R. Costa"), gap=8), *body],
               sub, acts=acts)


@screen("Importacao.dc.html", "T14.04.01 Lotes", "r09b", "T14.04.01")
def t140401():
    rows = [["2026-11-03 · L01", "planilha_acompanhamento_2026.xlsx", "9f3c…a21e", "R. Costa", "03/11/2026", estado("Em conferência", "blue"), "1.284", "1.201 aceitas · 46 conciliadas · 23 rejeitadas · 14 adiadas",
             col(a("Continuar", "T140402-Mapeamento.dc.html"), a("Abrir recibo", "T140407-Recibo.dc.html"), gap=4, style="font-size:12px;")],
            ["2026-10-20 · L04", "relatorio_empenhos_2026-10.csv", "41ab…77d0", "L. Martins", "20/10/2026", estado("Concluída", "green"), "212", "208 aceitas · 4 divergências",
             a("Abrir recibo", "T140407-Recibo.dc.html")],
            ["2026-11-04 · L01", "planilha_acompanhamento_2026.xlsx", "9f3c…a21e", "R. Costa", "04/11/2026", badge("Recusado — já recebido", "red"), "—", "Mesmo arquivo e leiaute (CEN03)", "—"]]
    novo = section("Novo lote", form_grid(field("Leiaute", kind="select", options=["L01 Planilhas legadas (cinco abas)", "L02 Contratos", "L03 Designações", "L04 Notas de empenho e movimentos",
                                                                                   "L05 Liquidações e pagamentos", "L06 Documentos fiscais (XML ou planilha)", "L07 Séries de índices",
                                                                                   "L08 Feriados", "L09 Itens de preço e cronograma"]),
                                          field("Arquivo", "", placeholder="Selecionar arquivo (UTF-8, datas ISO, decimais como texto)")),
                   actions(btn("Simular carga (não grava a carteira)", kind="primary"), btn("Cancelar")), h=3)
    return imp("T14.04.01 Lotes", [listbar(3, 0), table(["Lote", "Arquivo", "Hash", "Responsável", "Data", "Situação", ("Candidatas", "r"), "Contagens por disposição", "Ações"], rows, minw=1300, dense=True),
                                   novo, small("No celular, exibe-se o resumo do lote e uma linha por vez; a carga em massa é feita no computador.")],
               "Simulação antes da carga; disposição única por linha; recibo. Aplicável a qualquer leiaute da seção 16.",
               acts=[btn("Novo lote", kind="primary", ico="upload")])


@screen("T140402-Mapeamento.dc.html", "T14.04.02 Prévia e mapeamento", "r09b", "T14.04.02")
def t140402():
    rows = [["Contratos", "A", "Nº CONTRATO", "ctr.contrato.numero", "Texto", "012/2025", "Normaliza número", "v3", "—"],
            ["Contratos", "D", "CNPJ", "ctr.contratada.cnpj", "Identificador", "12.345.678/0001-95", "Confere dígitos (alfanumérico aceito)", "v3", "—"],
            ["Contratos", "H", "VALOR GLOBAL", "ctr.versao_contratual.valor_global", "Decimal (texto)", "1.020.000,00", "Lido como texto decimal", "v3", "—"],
            ["Contratos", "K", "TÉRMINO", "ctr.versao_contratual.vigencia_fim", "Data", "28/11/2026", "dd/mm/aaaa → ISO", "v3", span("12 células com data inválida", style="color:#FFB3B8;")],
            ["Comissões", "(sem título)", "—", "pes.pessoa_dado_restrito.id_funcional", "Identificador restrito", "******56", "Mascarado por padrão", "v3", "—"]]
    return imp("02 Prévia e mapeamento", [table(["Aba", "Coluna", "Cabeçalho", "Destino", "Tipo", "Exemplo", "Regra", "Versão do mapa", "Erro"], rows, minw=1300, dense=True),
                                          actions(btn("Alterar mapa (gera nova versão)"), btn("Simular sem gravar a carteira", kind="primary"))],
               "Aba, coluna, cabeçalho, destino, tipo, exemplo, regra, versão e erro.")


@screen("T140403-Conciliacao.dc.html", "T14.04.03 Conciliação de contratos", "r09b", "T14.04.03")
def t140403():
    lista = table(["Linha original", "Candidatos no sistema", "Número", "Processo", "Natureza", "Contraparte", "Decisão"],
                  [["Contratos · linha 87", "063/2026 (rascunho digitado)", "63/2026", "SEI-040014/000955/2026", "Termo de contrato", "Upsilon Brigada Ltda", badge("Vinculada", "green")],
                   ["Contratos · linha 41", "021/2025 Zeta · 021/2025 Eta", "21/2025", "SEI-040014/000877/2025", "Carta-contrato", "Eta Transportes Ltda", badge("Pendente", "yellow")],
                   ["Contratos · linha 112", "—", "58/2026", "—", "Termo de contrato", "Tau Arquivística Ltda", badge("Criada distinta", "blue")]], minw=1000, dense=True)
    painel = section("Evidências — linha 41", kv([("Processo na planilha", "SEI-040014/000877/2025"), ("Contraparte", "Eta Transportes Ltda (CNPJ confere)"),
                                                  ("Candidato mais provável", "021/2025 Eta (mesmo processo e contraparte)")], min_=260),
                     field("Decisão", kind="radio", options=["*Vincular a 021/2025 Eta", "Criar distinto", "Rejeitar", "Adiar"]), field("Justificativa", "Processo e contraparte coincidem", req=True, kind="textarea", rows=2),
                     actions(btn("Registrar decisão", kind="primary")), h=3)
    return imp("03 Conciliação de contratos", [div(div(lista, style="flex:999 1 560px;min-width:0;"), div(painel, style="flex:1 1 320px;min-width:0;max-width:420px;"),
                                                   style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start;")],
               "Linha original, candidatos, número, processo, natureza, contraparte e evidências — tabela com painel lateral de evidências.")


@screen("T140404-Designacao.dc.html", "T14.04.04 Divergências de designação", "r09b", "T14.04.04")
def t140404():
    rows = [["012/2025", "Fiscal administrativo", "F. Dias", "******56", "Acompanhamento: 29/11/2025 –", "Comissões: 01/12/2025 –", "PORT GERAD nº 112/2025",
             col(a("Escolher com evidência", "T140404-Designacao.dc.html"), a("Informar valor comprovado", "T140404-Designacao.dc.html"), a("Manter pendente", "T140404-Designacao.dc.html"), gap=4, style="font-size:12px;")],
            ["021/2025 Eta", "Fiscal técnico", "Q. Duarte", "******19", "Acompanhamento: titular", "Comissões: suplente", "—",
             col(a("Escolher com evidência", "T140404-Designacao.dc.html"), a("Manter pendente", "T140404-Designacao.dc.html"), gap=4, style="font-size:12px;")]]
    return imp("04 Divergências de designação", [table(["Contrato", "Papel", "Pessoa", "Identificador restrito", "Valor na aba Acompanhamento", "Valor na aba Comissões", "Ato", "Decisão"], rows, minw=1200, dense=True),
                                                 small("Identificador mascarado; a escolha exige evidência (ato ou Termo de Ciência). Conflitos do legado constam em bloco próprio no RPT12.")],
               "Valores das duas abas, papel, pessoa, identificador restrito, período e ato.")


@screen("T140405-Validacao.dc.html", "T14.04.05 Validação por domínio", "r09b", "T14.04.05")
def t140405():
    rows = [["Contratos", "058/2026 · CNPJ", "58.901.234/0001-1X", "—", "—", "Vigência corrente", "—", badge("Devolvido", "orange"), "Dígito verificador inválido"],
            ["Valores", "012/2025 · valor global", "=12*85000", "1.020.000,00", "Fórmula da célula H14", "Vigência 2025–2026", "Contrato 012/2025", badge("Aprovado", "green"), "—"],
            ["Prazos", "021/2025 Eta · término", "31/08/27", "31/08/2027", "—", "Vigência corrente", "Carta-contrato", badge("Pendente", "yellow"), cat(badge("Importado – não validado", "purple"))]]
    div_ = section("Divergência com valor validado (16.7)", kv([("Campo", "012/2025 · data de término"), ("Valor do sistema (validado)", "28/11/2026"), ("Valor do arquivo", "28/12/2026")], min_=240),
                   field("Decisão", kind="radio", options=["Aceitar o valor da fonte", "*Manter o valor do sistema", "Corrigir por digitação"]), field("Justificativa", "Conferido no instrumento assinado", req=True),
                   small("Valor validado não muda sem decisão registrada com justificativa e autor."), h=3)
    return imp("05 Validação por domínio", [table(["Domínio", "Registro · campo", "Original", "Normalizado", "Fórmula", "Escopo temporal", "Instrumento", "Estado", "Motivo"], rows, minw=1300, dense=True),
                                            actions(btn("Aprovar", kind="primary", disabled=True, title="Aprovação bloqueada sem evidência"), btn("Devolver com motivo"), btn("Corrigir com motivo")),
                                            small("Aprovação bloqueada sem evidência."), div_],
               "Original, normalizado, fórmula, escopo temporal, instrumento e estado por domínio.")


@screen("T140406-Qualidade.dc.html", "T14.04.06 Qualidade da carteira", "r09b", "T14.04.06")
def t140406():
    rows = [["Data-base de reajuste", badge("Alta", "orange"), "021/2025 Eta", "T. Vieira", "Reajustes pendentes", "L01 · aba Contratos", a("Abrir cadastro", "T04-P7-Composicao.dc.html")],
            ["Processo de gestão e fiscalização", badge("Média", "yellow"), "019/2025", "G. Freitas", "RPT15 · conformidade", "—", a("Criar providência", "T11B-Todas.dc.html")],
            ["Projeção validada", badge("Alta", "orange"), "041/2026", "L. Martins", "Comprometimento financeiro previsto", "—", a("Abrir cadastro", "T07C-Projecao.dc.html")],
            ["Início estimado da substituta", badge("Alta", "orange"), "033/2025", "T. Vieira", "Risco de descontinuidade", "—", a("Criar providência", "T11B-Todas.dc.html")]]
    return imp("06 Qualidade da carteira", [listbar(4, 4), table(["Campo faltante", "Gravidade", "Contrato", "Responsável", "Indicador prejudicado", "Fonte", "Ação"], rows, minw=1000, dense=True)],
               "Campo faltante, gravidade, contrato, responsável, indicador prejudicado e fonte.", acts=[btn("Exportar pendências", ico="download")])


@screen("T140407-Recibo.dc.html", "T14.04.07 Recibo e reconciliação", "r09b", "T14.04.07")
def t140407():
    return imp("07 Recibo e reconciliação", [
        grid(stat("Candidatas", "1.284"), stat("Aceitas", "1.201", "", "green"), stat("Conciliadas", "46"), stat("Rejeitadas", "23", "", "red"), stat("Adiadas", "14", "", "yellow"), min_=160),
        alert("ok", "Totais reconciliados", "1.201 + 46 + 23 + 14 = 1.284 candidatas — entradas e disposições conciliam (RPT13)."),
        table(["Candidata", "Disposição", "Destino", "Motivo", "Homologadores", "Entidades derivadas", "Versão dos cálculos"],
              [["Contratos · linha 87", "Conciliada", a("063/2026", "T04-P1-Identificacao.dc.html"), "Vinculada ao rascunho digitado", "R. Costa · M. Silva", "—", "v0.4"],
               ["Contratos · linha 112", "Aceita", a("058/2026", "T02C-Rascunhos.dc.html"), "Criada como distinta", "R. Costa · M. Silva", "1 contratada", "v0.4"],
               ["Contratos · linha 133", "Rejeitada", "—", "CNPJ com dígito verificador incorreto (CEN06)", "R. Costa", "—", "v0.4"]], minw=1100, dense=True),
        actions(btn("Conferir"), btn("Exportar XLSX", ico="download"), btn("CSV"), btn("PDF")),
    ], "Disposição de cada candidata, destino, motivo, homologadores, entidades derivadas e versão dos cálculos.")


# ---------------------------------------------------------------- T14.05 a T14.07
@screen("T1405-Trilha.dc.html", "T14.05 Trilha de auditoria", "r09b", "T14.05")
def t1405t():
    rows = [["10/11/2026 09:10", "M. Silva", "ctr.contrato", "012/2025", "U", "objeto_resumido: “Manutenção predial” → “Manutenção predial preventiva e corretiva”", "Correção de grafia do objeto"],
            ["10/11/2026 09:12", "R. Costa", "ctr.contrato", "012/2025", "Conflito", "Gravação com versão desatualizada recusada (v6 × v7)", "—"],
            ["05/11/2026 16:20", "P. Nunes", "prc.procedimento_movimentacao", "PRC-2026-014", "I", "Remessa GERAD → ASSJUR", "—"],
            ["04/11/2026 08:02", "—", "seg (acesso)", "—", "Negado", "Usuário de outra unidade tentou abrir 012/2025 (CP01)", "—"]]
    return adm("T14.05", "Auditoria e correções", T1405_TABS, "Trilha", [
        row(fsel("Usuário", "Todos", "M. Silva", "R. Costa"), fsel("Tabela", "Todas", "ctr.contrato", "fin.empenho"), field("Registro", "", placeholder="Ex.: 012/2025"), fsel("Período", "Últimos 30 dias"), gap=12, align="flex-end"),
        table(["Instante", "Usuário", "Tabela", "Registro", "Ação", "Antes → depois", "Motivo"], rows, minw=1200, dense=True),
        small("Somente leitura: a trilha não admite alteração (BD47). Correção financeira por estorno ou evento compensatório."),
    ], "Trilha filtrável por usuário, tabela, registro e período, com antes e depois.")


@screen("T1405-Exportacoes.dc.html", "T14.05 Exportações", "r09b", "T14.05")
def t1405e():
    return adm("T14.05", "Auditoria e correções", T1405_TABS, "Exportações",
               [table(["Instante", "Usuário", "Relatório", "Filtros", "Formato", ("Linhas", "r"), "Identificador"],
                      [["10/11/2026 08:40", "M. Silva", "RPT15", "II, V, VI · GERAD e GERTIC · 2026", "PDF", "6", "EXP-2026-11-10-0007"],
                       ["09/11/2026 17:02", "L. Martins", "RPT05", "2026 · todas", "XLSX", "34", "EXP-2026-11-09-0003"]], dense=True)],
               "Relatórios emitidos (aud.exportacao).")


@screen("T1405-Correcoes.dc.html", "T14.05 Correções", "r09b", "T14.05")
def t1405c():
    return adm("T14.05", "Auditoria e correções", T1405_TABS, "Correções",
               [table(["Instante", "Registro", "Tipo", "Motivo", "Autor"],
                      [["20/04/2026", "Designação F. Dias (012/2025)", "Correção de data de início", "Conferência do ato", "R. Costa"],
                       ["02/10/2026", "Liquidação 2026NL00950", "Estorno (2026NL00951)", "Competência incorreta", "L. Martins"]], dense=True),
                small("Versão anterior preservada com autor e motivo (CH04).")], "Correções e estornos com motivo.")


@screen("T1406-Copias.dc.html", "T14.06 Cópias e recuperação", "r09b", "T14.06")
def t1406():
    return adm("T14.06", "Cópias e recuperação", None, None, [
        grid(stat("Última cópia do banco", "10/11/2026 02:00", "cifrada · retenção 30 dias", "green"), stat("Última cópia dos documentos", "10/11/2026 02:30", "", "green"),
             stat("Último teste de restauração", "15/10/2026", "ambiente isolado · reconciliado (CO01)", "green"), stat("Fila de avisos", "Saudável", "3 entregas pendentes"), min_=220),
        table(["Teste", "Data", "Ambiente", "Resultado"], [["Restauração completa", "15/10/2026", "Isolado", badge("Reconciliado", "green")], ["Restauração de documentos", "15/07/2026", "Isolado", badge("Reconciliado", "green")]], dense=True),
        alert("warn", None, "Restauração em produção apenas por procedimento autorizado. Proposta a homologar: perda máxima de 24 horas e recuperação em até 8 horas (seção 10.4)."),
    ], "Estado das cópias, testes de restauração e saúde da fila de avisos.", tecnico=True)


@screen("T1407-Conectores.dc.html", "T14.07 Integrações — Conectores", "r09b", "T14.07")
def t1407c():
    rows = [["PNCP", "Somente leitura", badge("Ativo", "green"), "09/11/2026 03:00 · 14 consultados", "cofre://contratos/pncp (referência)"],
            ["SEI", "Somente leitura", badge("Ativo", "green"), "10/11/2026 07:00 · 9 processos", "cofre://contratos/sei"],
            ["Sistema financeiro oficial", "Somente leitura", badge("Inativo — formato a confirmar", "gray"), "—", "—"],
            ["Índices (IPCA)", "Somente leitura", badge("Ativo", "green"), "11/10/2026 03:00", "Sem credencial"]]
    return adm("T14.07", "Integrações", T1407_TABS, "Conectores",
               [table(["Fonte", "Modo", "Estado", "Última execução", "Referência da credencial"], rows, dense=True),
                alert("info", "Indisponibilidade da fonte", "Registra a falha, mantém os dados e a data da última atualização; a digitação segue disponível (CO03, CEN01)."),
                small("Credencial no cofre de segredos — a tela mostra apenas a referência.")],
               "Conectores por fonte: modo, estado, última execução e referência da credencial.", tecnico=True)


@screen("T1407-Execucoes.dc.html", "T14.07 Integrações — Execuções", "r09b", "T14.07")
def t1407e():
    return adm("T14.07", "Integrações", T1407_TABS, "Execuções",
               [table(["Execução", "Fonte", "Início", ("Lidos", "r"), ("Propostas", "r"), ("Divergências", "r"), ("Erros", "r"), "Situação"],
                      [["2026-11-10-0700", "SEI", "10/11/2026 07:00", "9", "2", "0", "0", badge("Concluída", "green")],
                       ["2026-11-09-0300", "PNCP", "09/11/2026 03:00", "14", "1", "1", "0", badge("Concluída", "green")],
                       ["2026-11-08-0300", "PNCP", "08/11/2026 03:00", "0", "0", "0", "1", badge("Falha — fonte indisponível", "red")]], dense=True)],
               "Execuções com contagens e erros.", tecnico=True)


@screen("T1407-Divergencias.dc.html", "T14.07 Integrações — Divergências", "r09b", "T14.07")
def t1407d():
    return adm("T14.07", "Integrações", T1407_TABS, "Divergências", [
        table(["Contrato · campo", "Valor do sistema", "Origem do sistema", "Valor da fonte", "Origem da fonte", "Situação"],
              [["052/2025 · valor global", "115.000,00", "Digitado (validado)", "100.000,00", "PNCP · 09/11/2026", badge("Aberta", "yellow")]], dense=True),
        section("Decisão", field("Opção", kind="radio", options=["Aceitar o valor da fonte", "*Manter o valor do sistema", "Corrigir por digitação"]),
                field("Justificativa", "PNCP sem os termos aditivos 1 e 2; valor do sistema conferido nos instrumentos", req=True, kind="textarea", rows=2),
                field("Autor", "M. Silva", ro=True), actions(btn("Registrar decisão", kind="primary")),
                small("Dado validado só muda por decisão registrada (CEN04). Divergências de importação por arquivo são decididas em T14.04.05, com as mesmas opções."), h=3),
    ], "Divergências entre o valor do sistema e o da fonte, com decisão.")
