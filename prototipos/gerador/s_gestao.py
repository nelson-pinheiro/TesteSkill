"""T11 Central de providências (A–D e editor lateral), T12 Central de notificações (A–C) e T13 Relatórios (A, B e T13.01)."""
from shell import *
from s_inicio import ACAO, ctr_cell

EXTRA = [("Alta", None, "Piso pelo risco Alto do contrato; designação sem os suplentes exigidos (C20)", "012/2025", "Alfa Serviços Prediais Ltda", "Designar suplentes e colher Termo de Ciência", "M. Silva", "30/11/2026", 20, "Alto"),
         ("Média", None, "Designação incompleta há 40 dias (até 60 — C20)", "021/2025", "Eta Transportes Ltda", "Designar fiscal titular", "T. Vieira", "20/11/2026", 10, "Indeterminado"),
         ("Média", None, "Pagamento com impedimento (regularidade fiscal); documento próximo de 2 meses", "019/2025", "Delta Copeiragem Ltda", "Obter certidão federal atualizada", "L. Martins", "16/11/2026", 6, "Sem risco identificado"),
         ("Alta", None, "Piso pelo risco Alto do contrato; movimento não classificado torna E indeterminado (C05)", "031/2023", "Beta Tecnologia S.A.", "Saneamento: classificar movimento da nota 2026NE00031", "L. Martins", "13/11/2026", 3, "Alto"),
         ("Planejamento", None, "Obrigação complementar de retroativo pendente (C12)", "060/2024", "Sigma Climatização Ltda", "Pagar obrigação complementar do retroativo (R$ 1.100,00)", "L. Martins", "30/11/2026", 20, "Sem risco identificado"),
         ("Planejamento", None, "Data interna de início (C15) em 14/02/2027 — a iniciar", "044/2023", "Épsilon Elevadores Ltda", "Instruir prorrogação", "P. Nunes", "14/02/2027", 96, "Sem risco identificado")]
CATS = {"027/2024": "Prorrogação", "033/2025": "Contratação substitutiva", "031/2023": "Contratação substitutiva", "041/2026": "Designação", "044/2023": "Reforço de empenho",
        "019/2025": "Reajuste e demais alterações", "038/2024": "Encerramento", "021/2025": "Saneamento de dados", "015/2022": "Pagamento com impedimento", "060/2024": "Pagamento com impedimento",
        "047/2024": "Prorrogação", "012/2025": "Prorrogação"}
SIT = {"027/2024": "Em andamento", "012/2025": "Em andamento", "047/2024": "Aguardando terceiro", "033/2025": "Aberta", "031/2023": "Em andamento", "044/2023": "Aberta",
       "041/2026": "Em andamento", "038/2024": "Aberta", "019/2025": "Aberta", "021/2025": "Aberta", "015/2022": "Aberta", "060/2024": "Aberta"}


def prov_rows(items, sel=None):
    rows = []
    for pr, sug, motivo, n, ctda, prov, resp, prazo, dias, rk in items:
        cat_ = "Atualização de garantia" if "endosso" in prov else ("Designação" if "esign" in prov else ("Saneamento de dados" if "aneamento" in prov else CATS.get(n, "Prorrogação")))
        sit = "Aguardando terceiro" if "endosso" in prov else SIT.get(n, "Aberta")
        dcell = span(f"{-dias} de atraso", style="color:#FFB3B8;font-weight:600;") if dias < 0 else str(dias)
        selc = badge("Em edição →", "blue") if sel and prov == sel else None
        rows.append([ctr_cell(n, ctda), cat_, cat(a(prov, "T11B-Todas.dc.html", style=f"color:{TEXT};text-decoration:underline;"), " ", selc), resp, prazo, dcell,
                     cat(div(row(small("Sugerida"), prio(sug or pr), gap=4)), div(row(small("Confirmada"), prio(pr), gap=4)) if sug else None,
                         div(motivo, style=f"font-size:11px;color:{MUTED};margin-top:2px;")),
                     estado(sit), "SEI-040014/000512/2026" if n == "012/2025" else "—"])
    return rows


COLS = ["Contrato", "Categoria", "Descrição", "Responsável", "Prazo", ("Dias", "r"), "Prioridade sugerida e confirmada (motivo)", "Situação", "Processo"]


@screen("Providencias.dc.html", "T11.A Providências — Minhas", "r08", "T11.A")
def t11a():
    minhas = [it for it in ACAO + EXTRA if it[6] == "M. Silva"]
    return page("T11 Central de providências", "provid", ["Providências", "A Minhas"],
                [listbar(len(minhas), 0), table(COLS, prov_rows(sorted(minhas, key=lambda x_: x_[8]))[::1], minw=1300, dense=True),
                 actions(btn("Atualizar situação"), btn("Registrar andamento"), btn("Concluir com evidência", kind="primary")),
                 small("Ordenadas por prazo. Providências também nascem de regras (C15, C19, C20), de notificações e da importação das observações do legado, sempre com conferência.")],
                tabs_=tabs(T11_TABS, "A Minhas"), acts=[btn("Nova providência", href="T11B-Todas.dc.html", kind="primary", ico="plus")],
                sub="O que precisa ser feito, por quem e até quando (Diretriz, item 9). Usuária: M. Silva.")


def editor():
    return tag("aside",
               row(tag("h2", "Editor lateral", style=f"margin:0;font-size:16px;color:{TEXT};"), estado("Aberta"), justify="space-between"),
               field("Contrato", "038/2024 — Kapa Construções Ltda", ro=True), field("Procedimento", "—", ro=True),
               field("Categoria", kind="select", options=["Providência de encerramento", "Prorrogação", "Designação"]),
               field("Descrição", "Avaliar mora ou extinção (objeto não concluído — prorrogação automática, art. 111)", kind="textarea", rows=2),
               field("Responsável", kind="select", options=["P. Nunes", "M. Silva", "J. Prado"]),
               field("Prazo", "25/11/2026", kind="date", note="Reagendar exige motivo e preserva o prazo anterior."),
               div(span("Prioridade", style=f"font-size:13px;font-weight:600;color:{TEXT};"),
                   row(small("Sugerida (C17)"), prio("Média"), small("risco Moderado — escopo em prorrogação automática"), gap=6),
                   row(small("Confirmada"), prio("Alta"), small("M. Silva · 09/11/2026 — “mora da contratada já notificada; risco ao acervo durante a obra”"), gap=6),
                   style="display:flex;flex-direction:column;gap:6px;"),
               field("Situação", kind="select", options=["Aberta", "Aguardando terceiro", "Em andamento", "Concluída", "Cancelada"], note="Aguardar terceiro não suspende o prazo."),
               field("Processo", "SEI-040014/000519/2024"), field("Dependência", "Parecer técnico da fiscalização"),
               field("Evidência (documento ou referência)", "", placeholder="Obrigatória para concluir", error="Conclusão bloqueada: informe a data e a evidência (CR04)."),
               details("Histórico", tag("ul", tag("li", "31/10/2026 — criada pela regra C18 (escopo em prorrogação automática) · sistema"),
                                        tag("li", "09/11/2026 — prioridade confirmada Alta (sugerida Média) · M. Silva"),
                                        style=f"margin:0;padding-left:18px;font-size:12px;color:{TEXT2};line-height:1.6;")),
               actions(btn("Salvar", kind="primary", small_=True), btn("Concluir", small_=True), btn("Cancelar (exige motivo)", small_=True), btn("Reagendar (exige motivo)", small_=True)),
               aria_label="Editor lateral da providência",
               style=f"flex:1 1 340px;max-width:420px;min-width:0;display:flex;flex-direction:column;gap:12px;padding:18px;background:{SURF};border:1px solid {LINE2};border-radius:8px;box-sizing:border-box;align-self:flex-start;")


@screen("T11B-Todas.dc.html", "T11.B Providências — Todas (com editor lateral)", "r08", "T11.B")
def t11b():
    todas = ACAO + EXTRA
    grupos = []
    for pr in ["Crítica", "Alta", "Média", "Planejamento", "A confirmar"]:
        its = sorted([it for it in todas if it[0] == pr], key=lambda x_: x_[8])
        grupos.append(section(cat(prio(pr), f"  {len(its)} providência(s)"),
                              table(COLS, prov_rows(its, sel="Avaliar mora ou extinção (objeto não concluído)"), dense=True), h=3))
    lista = div(listbar(len(todas), 0), *grupos, style="flex:999 1 560px;min-width:0;display:flex;flex-direction:column;gap:16px;")
    return page("T11 Central de providências — todas", "provid", [("Providências", "Providencias.dc.html"), "B Todas"],
                [filterbar(fsel("Categoria", "Todas", "Prorrogação", "Designação", "Reforço de empenho", "Atualização de garantia"), fsel("Responsável", "Todos", "P. Nunes", "L. Martins", "M. Silva"),
                           fsel("Situação", "Abertas", "Aguardando terceiro", "Todas")),
                 div(lista, editor(), style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start;")],
                tabs_=tabs(T11_TABS, "B Todas"), acts=[btn("Nova providência", kind="primary", ico="plus"), btn("Atribuir"), btn("Confirmar ou ajustar prioridade (coordenador)")],
                sub="Agrupadas por prioridade (Crítica, Alta, Média, Planejamento, A confirmar), com sugerida e confirmada e o motivo.")


@screen("T11C-PorResponsavel.dc.html", "T11.C Providências — Por responsável", "r08", "T11.C")
def t11c():
    rows = [["P. Nunes", "Gestor · GERAD", "4", span("1", style="color:#FFB3B8;font-weight:700;"), "0"], ["L. Martins", "Operadora financeira · DIRAF", "5", "0", "2"],
            ["T. Vieira", "Gestor · CHEGAB", "3", span("1", style="color:#FFB3B8;font-weight:700;"), "0"], ["A. Lima", "Gestor · GERTIC", "2", "0", "0"],
            ["M. Silva", "Coordenadora · GERAD", "2", "0", "1"], ["J. Prado", "Fiscal técnico · GERAD", "1", "0", "0"], ["C. Ramos", "Fiscal administrativo · GERAD", "1", "0", "0"]]
    return page("T11 Central de providências — por responsável", "provid", [("Providências", "Providencias.dc.html"), "C Por responsável"],
                [listbar(7, 0, acts=[btn("Exportar RPT10", href="Relatorios.dc.html", small_=True)]),
                 table(["Responsável", "Papel", ("Abertas", "r"), ("Vencidas", "r"), ("A vencer em 7 dias", "r")], rows, foot=["Total", "", "18", "2", "3"], dense=True),
                 actions(btn("Redistribuir selecionadas", kind="primary")), small("Vencidas destacadas por texto e cor. A quantidade de providências não se confunde com a de contratos.")],
                tabs_=tabs(T11_TABS, "C Por responsável"), sub="Carga por responsável: abertas, vencidas e a vencer em 7 dias.")


@screen("T11D-Concluidas.dc.html", "T11.D Providências — Concluídas e canceladas", "r08", "T11.D")
def t11d():
    rows = [[ctr_cell("012/2025", "Alfa Serviços Prediais Ltda"), "Registrar recomendação do gestor (M120)", estado("Concluída"), "31/07/2026", "Evidência: doc. 46610021", a("Reabrir com motivo", "T11B-Todas.dc.html")],
            [ctr_cell("060/2024", "Sigma Climatização Ltda"), "Formalizar reajuste (apostila nº 1)", estado("Concluída"), "05/10/2026", "Evidência: Apostila nº 1", a("Reabrir com motivo", "T11B-Todas.dc.html")],
            [ctr_cell("012/2025", "Alfa Serviços Prediais Ltda"), "Solicitar reforço de empenho (abril)", estado("Concluída"), "15/05/2026", "Evidência: 2026NE00140 conciliado", a("Reabrir com motivo", "T11B-Todas.dc.html")],
            [ctr_cell("017/2024", "Rho Eventos Ltda"), "Instruir prorrogação", estado("Cancelada"), "10/06/2026", "Motivo: extinção antecipada do contrato", a("Reabrir com motivo", "T11B-Todas.dc.html")]]
    return page("T11 Central de providências — concluídas e canceladas", "provid", [("Providências", "Providencias.dc.html"), "D Concluídas e canceladas"],
                [listbar(4, 0), table(["Contrato", "Providência", "Situação", "Data", "Evidência ou motivo", "Ação"], rows, dense=True),
                 small("Reabrir exige motivo; a conclusão anterior é preservada.")],
                tabs_=tabs(T11_TABS, "D Concluídas e canceladas"), sub="Histórico com evidência de conclusão ou motivo do cancelamento.")


# ======================================================================= T12
NOTIF = [("N01", "Aproximação do término", "012/2025", "Alfa Serviços Prediais Ltda", "Término 28/11/2026 — antecedência de 30 dias (parâmetro interno)", "28/11/2026", 18, "Alta", "P. Nunes",
          "Obter parecer jurídico e autorização", "T0302-Prazos.dc.html"),
         ("N15", "Marco regulamentar descumprido", "027/2024", "Gama Vigilância Ltda", "M30 (envio à assessoria jurídica) descumprido em 06/10/2026", "06/10/2026", -35, "Crítica", "P. Nunes",
          "Remeter o procedimento à ASSJUR", "T05D-Marcos.dc.html"),
         ("N14", "Designação ausente", "041/2026", "Lambda Software Ltda", "Sem designação há 101 dias — limite de 60 dias excedido (art. 7º, § 11)", "30/09/2026", -41, "Alta", "M. Silva",
          "Publicar ato de designação", "T0308-Responsaveis.dc.html"),
         ("N06", "Insuficiência projetada de empenho", "044/2023", "Épsilon Elevadores Ltda", "Reforço estimado R = 10.000,00 (C09); insuficiência em 01/12/2026", "01/12/2026", 21, "Alta", "L. Martins",
          "Solicitar reforço", "Empenhos.dc.html"),
         ("N16", "Prazo de recebimento", "060/2024", "Sigma Climatização Ltda", "Recebimento provisório da competência 10/2026 até 15/11/2026 (C22)", "15/11/2026", 5, "Média", "G. Antunes",
          "Registrar termo de recebimento provisório", "Pagamentos.dc.html"),
         ("N03", "Prorrogação sem avanço", "047/2024", "Nu Telecom S.A.", "Procedimento PRC-2026-017 sem movimentação há 35 dias (etapa 2)", "18/11/2026", 8, "Alta", "A. Lima",
          "Cobrar manifestação da contratada", "Prorrogacoes.dc.html"),
         ("N12", "Risco de descontinuidade", "031/2023", "Beta Tecnologia S.A.", "Lacuna de 14 dias entre término (31/03/2027) e início da substituta (15/04/2027)", "31/03/2027", 141, "Alta", "A. Lima",
          "Revisar cronograma da substituta", "T05C-Continuidade.dc.html")]


@screen("Notificacoes.dc.html", "T12.A Notificações — Não lidas", "r08", "T12.A")
def t12a():
    rows = []
    for ev, nome, n, ct, mot, lim, dias, pr, resp, prox, href in NOTIF:
        dtx = span(f"{-dias} dias de atraso", style="color:#FFB3B8;font-weight:600;") if dias < 0 else f"em {dias} dias"
        rows.append([cat(badge(ev, "blue"), div(nome, style=f"font-size:12px;color:{TEXT2};margin-top:2px;")), ctr_cell(n, ct), mot, cat(div(lim), small(dtx)), prio(pr), resp, prox,
                     cat(div("Gerada 10/11/2026 07:00" if ev in ("N16", "N03") else "Gerada 29/10/2026 07:00" if ev == "N01" else "Gerada 09/11/2026 07:00"),
                         small("Dados de 10/11/2026 07:00")),
                     col(btn("Abrir o registro", href=href, small_=True), btn("Registrar ciência", small_=True), btn("Registrar providência", href="T11B-Todas.dc.html", small_=True), gap=6)])
    return page("T12 Central de notificações", "notif", ["Notificações", "A Não lidas"],
                [listbar(7, 0), table(["Evento", "Contrato e contratada", "Motivo", "Data-limite", "Prioridade", "Responsável", "Próxima ação", "Geração e atualização dos dados", "Ações"],
                                      rows, minw=1500, dense=True),
                 alert("info", "Ações independentes", "Leitura, ciência, registro de providência e conclusão da tarefa são ações independentes; ciência nunca encerra a pendência (CN07). "
                       "Prazos de alerta são parâmetros internos, nunca apresentados como exigências legais.")],
                tabs_=tabs(T12_TABS, "A Não lidas"), sub="Notificações com motivo, prazo, prioridade, responsável e links diretos. Horário de Brasília.")


@screen("T12B-Historico.dc.html", "T12.B Notificações — Histórico", "r08", "T12.B")
def t12b():
    rows = [["29/10/2026 07:00", "N01 · 012/2025 · 30 dias", "Gerada", cat(badge("Interna: enviada", "green"), " ", badge("E-mail: falha", "red")),
             "E-mail: 3 tentativas (07:00, 07:10, 07:40); próxima às 09:40 — intervalos crescentes", "—"],
            ["29/09/2026 07:00", "N01 · 012/2025 · 60 dias", "Ciência registrada (30/09/2026)", cat(badge("Interna: enviada", "green"), " ", badge("E-mail: enviada", "green")), "1", "—"],
            ["14/10/2026 07:00", "N15 · 012/2025 · M30 em 15 dias", "Lida", cat(badge("Interna: enviada", "green"), " ", badge("E-mail: enviada", "green")), "1", "—"],
            ["31/07/2026 07:00", "N02 · 012/2025 · data interna (C15)", "Ciência registrada", cat(badge("Interna: enviada", "green"), " ", badge("E-mail: enviada", "green")), "1", "—"],
            ["—", "N01 · 060/2024 · 30 dias (vigência anterior)", "Cancelada", cat(badge("Interna: cancelada antes do envio", "gray"), " ", badge("E-mail: cancelada antes do envio", "gray")), "0",
             "Prorrogação formalizada em 22/05/2026 — avisos emitidos permanecem (CN02)"],
            ["15/11/2026 07:00 (programada)", "N08 · 012/2025 · garantia em 45 dias", "—", badge("Pendente", "yellow"), "0", "—"]]
    return page("T12 Central de notificações — histórico", "notif", [("Notificações", "Notificacoes.dc.html"), "B Histórico"],
                [row(fsel("Evento", "Todos", "N01", "N02", "N08", "N15"), fsel("Contrato", "Todos", "012/2025", "060/2024"), fsel("Período", "Últimos 90 dias", "Exercício 2026"), gap=12, align="flex-end"),
                 listbar(len(rows), 0), table(["Geração", "Notificação", "Estado da notificação", "Estado por canal", "Tentativas", "Cancelamento (motivo)"], rows, minw=1100, dense=True),
                 small("“Enviada” não significa recebida ou lida. Falha de e-mail não perde o aviso interno (CN06). Uma entrega por chave de idempotência: ocorrência + destinatário + canal + janela.")],
                tabs_=tabs(T12_TABS, "B Histórico"), sub="Todas as notificações do usuário, com estado por canal, tentativas e cancelamentos com motivo.")


@screen("T12C-Resumos.dc.html", "T12.C Notificações — Resumos", "r08", "T12.C")
def t12c():
    return page("T12 Central de notificações — resumos", "notif", [("Notificações", "Notificacoes.dc.html"), "C Resumos"],
                [section("Frequência configurada", kv([("Resumo periódico", "Semanal — segundas-feiras, 07:00 (Brasília)"), ("Destinatária", "M. Silva (coordenadora)")]),
                         field("Alterar frequência (preferência)", kind="select", options=["Semanal", "Diária", "Quinzenal", "Desativado"], w="260px"), prazo_nat("Parâmetro interno"), h=3),
                 table(["Resumo", "Recebido em", ("Itens", "r"), "Destaques", ""],
                       [["Semana de 09/11/2026", "09/11/2026 07:00", "14", "1 Crítica · 6 Altas · 2 marcos descumpridos", a("Abrir itens", "Main.dc.html")],
                        ["Semana de 02/11/2026", "02/11/2026 07:00", "12", "1 Crítica · 5 Altas", a("Abrir itens", "Main.dc.html")],
                        ["Semana de 26/10/2026", "26/10/2026 07:00", "11", "4 Altas", a("Abrir itens", "Main.dc.html")]], dense=True),
                 small("Um resumo por destinatário, sem duplicar os avisos individuais (CN20).")],
                tabs_=tabs(T12_TABS, "C Resumos"), sub="Resumos periódicos recebidos e a frequência configurada.")


# ======================================================================= T13
RPTS = [("RPT01", "Relação geral de contratos", "Contrato", "Todos os perfis com exportação"), ("RPT02", "Ficha consolidada individual", "Contrato", "Idem; gestor e fiscal nos designados"),
        ("RPT03", "Calendário de vencimentos", "Contrato", "Idem"), ("RPT04", "Prorrogações e substituições", "Procedimento", "Idem"),
        ("RPT05", "Empenhos e necessidade de reforço", "Nota e contrato", "Idem"), ("RPT06", "Execução financeira por contrato e exercício", "Contrato, exercício e mês", "Idem"),
        ("RPT07", "Documentos fiscais e pagamentos pendentes", "Documento ou obrigação", "Idem"), ("RPT08", "Reajustes e alterações", "Pedido ou alteração", "Idem"),
        ("RPT09", "Previsão orçamentária", "Contrato, mês e versão", "Idem"), ("RPT10", "Providências por responsável", "Tarefa", "Idem"),
        ("RPT11", "Garantias e documentos pendentes", "Garantia ou documento", "Idem"), ("RPT12", "Responsáveis e designações", "Vínculo pessoa–contrato–papel", "Idem; identificadores mascarados sem permissão"),
        ("RPT13", "Qualidade e reconciliação da carga", "Ocorrência por célula", "Coordenador e operadores"), ("RPT14", "Auditoria e notificações", "Evento ou tentativa", "Coordenador, consulta e controle interno; adm. técnico (técnica)"),
        ("RPT15", "Conformidade da gestão e fiscalização", "Contrato", "Coordenador; consulta, auditoria e controle interno")]


@screen("Relatorios.dc.html", "T13.A Relatórios — Catálogo", "r08", "T13.A")
def t13a():
    rows = [[strong(c_), n, g, small(pf), a("Escolher", "T1301-Previa.dc.html" if c_ == "RPT15" else "Relatorios.dc.html")] for c_, n, g, pf in RPTS]
    cfg = section("Configurar RPT15 — Conformidade da gestão e fiscalização", form_grid(
        field("Universo (incisos do art. 2º da Lei nº 14.133/2021)", kind="checkbox", options=["*II — compra", "*V — prestação de serviços", "*VI — obras e serviços de engenharia", "VII — TIC"],
              note="Padrão: II, V e VI; contratos de outros incisos listados à parte."),
        field("Unidades", kind="select", options=["GERAD e GERTIC", "Todas as autorizadas", "GERAD"]), field("Exercício", kind="select", options=["2026", "2025"]),
        field("Data de corte", "10/11/2026", kind="date"), field("Agrupamento", kind="select", options=["Unidade", "Modalidade", "Risco"]),
        field("Ordenação", kind="select", options=["Número do contrato", "Valor decrescente"]),
        field("Colunas", kind="select", options=["Padrão (itens da aba T03.11)", "Personalizadas"]),
        field("Formato", kind="radio", options=["*PDF", "XLSX", "CSV"]),
        field("Eixo temporal", "", ro=True, placeholder="Desabilitado: aplicável apenas ao RPT06", note="Filtro inaplicável fica desabilitado com explicação."),
        field("Critérios de seleção da unidade de controle interno", "Amostra estratificada por valor e dedicação exclusiva de mão de obra", kind="textarea", rows=2,
              note="Gravados com a emissão (IN AGE nº 54/2025).")),
        actions(btn("Pré-visualizar (T13.01)", href="T1301-Previa.dc.html", kind="primary")))
    return page("T13 Relatórios", "relat", ["Relatórios", "A Catálogo"],
                [table(["Código", "Relatório", "Grão", "Perfis autorizados (seção 10.2)", ""], rows, dense=True), cfg],
                tabs_=tabs(T13_TABS, "A Catálogo"), sub="RPT01 a RPT15, com finalidade, grão e perfis autorizados. Escolha relatório, filtros, data de corte, agrupamento, ordenação, colunas e formato.")


@screen("T13B-Emissoes.dc.html", "T13.B Relatórios — Emissões recentes", "r08", "T13.B")
def t13b():
    rows = [["RPT15", "10/11/2026", "Incisos II, V, VI · GERAD e GERTIC · 2026", "PDF", "6", "EXP-2026-11-10-0007", a("Reemitir", "T1301-Previa.dc.html")],
            ["RPT05", "09/11/2026", "Exercício 2026 · todas as unidades", "XLSX", "34", "EXP-2026-11-09-0003", a("Reemitir", "Relatorios.dc.html")],
            ["RPT13", "03/11/2026", "Lote L01 2026-11-03", "CSV", "1.284", "EXP-2026-11-03-0011", a("Reemitir", "T140407-Recibo.dc.html")],
            ["RPT01", "01/11/2026", "Vigentes · GERAD", "PDF", "9", "EXP-2026-11-01-0002", a("Reemitir", "Relatorios.dc.html")]]
    return page("T13 Relatórios — emissões recentes", "relat", [("Relatórios", "Relatorios.dc.html"), "B Emissões recentes"],
                [listbar(4, 0), table(["Código", "Posição", "Filtros", "Formato", ("Linhas", "r"), "Identificador", ""], rows, dense=True),
                 small("Reemitir usa os mesmos parâmetros; cada emissão fica registrada em aud.exportacao.")],
                tabs_=tabs(T13_TABS, "B Emissões recentes"), sub="Relatórios emitidos pelo usuário: código, posição, filtros, formato, linhas e identificador.")


@screen("T1301-Previa.dc.html", "T13.01 Prévia e exportação — RPT15", "r08", "T13.01")
def t1301():
    def r(n, ct, val, mod, de, rk, it):
        return [n, ct, val, mod, de, risco(rk)] + it
    rows = [r("012/2025", "Alfa Serviços Prediais", "1.074.400,00", "Pregão", "Sim", "Alto", ["Completa · faltam 2 suplentes", "Ciência: não atende", "Informado", "M120 cumprido · M30 com atraso", "1 insuficiente", "1 competência sem registro"]),
            r("027/2024", "Gama Vigilância", "2.880.000,00", "Pregão", "Sim", "Existente", ["Completa", "Atende", "Informado", "M30 descumprido", "Suficiente", "Completa"]),
            r("019/2025", "Delta Copeiragem", "744.000,00", "Pregão", "Sim", "Sem risco identificado", ["Completa", "Atende", badge("Não informado", "gray", dashed=True), "A cumprir", "Suficiente", "1 competência sem registro"]),
            r("044/2023", "Épsilon Elevadores", "612.000,00", "Pregão", "Não", "Sem risco identificado", ["Completa", "Atende", "Informado", "A cumprir", "Suficiente", "Não aplicável"]),
            r("038/2024", "Kapa Construções", "480.000,00", "Concorrência", "Não", "Moderado — escopo em prorrogação automática", ["Completa", "Atende", "Informado", "Não aplicável", "Suficiente", "Não aplicável"]),
            r("060/2024", "Sigma Climatização", "125.000,00", "Pregão", "Não", "Sem risco identificado", ["Completa", "Atende", "Informado", "A cumprir", "Suficiente", "Não aplicável"])]
    return page("T13.01 Prévia e exportação", "relat", [("Relatórios", "Relatorios.dc.html"), "RPT15", "Prévia"], [
        div(row(div(div("GOVERNO DO ESTADO DO RIO DE JANEIRO · RIOPREVIDÊNCIA", style=f"font-size:12px;letter-spacing:.06em;color:{FAINT};font-weight:700;"),
                    div("RPT15 — Conformidade da gestão e fiscalização", style=f"font-size:20px;font-weight:700;color:{TEXT};margin-top:4px;")),
                div(small("Posição 10/11/2026 07:00 (Brasília) · emissão EXP-2026-11-10-0007"), small("Fotografia dos dados: snapshot nº 2026-11-10-0700"), style="display:flex;flex-direction:column;align-items:flex-end;"),
                justify="space-between"),
            kv([("Universo", "Incisos II, V e VI do art. 2º da Lei nº 14.133/2021 (padrão) · contratos vigentes na posição"), ("Unidades · exercício", "GERAD e GERTIC · 2026"),
                ("Critérios de seleção informados pela unidade de controle interno", "Amostra estratificada por valor e dedicação exclusiva de mão de obra (gravados com a emissão)")], min_=260),
            style=f"display:flex;flex-direction:column;gap:14px;padding:20px;background:{SURF};border:1px solid {LINE};border-radius:8px;"),
        table(["Contrato", "Contratada", ("Valor", "r"), "Modalidade", "Ded. exclusiva", "Risco", "Designação (C20)", "Ato e ciência", "Processo de gestão", "Marcos (C19)", "Atesto (C21)", "Conferência trabalhista"],
              rows, minw=1600, dense=True),
        grid(stat("Contratos no universo", "6", "de 9 contratos vigentes de GERAD e GERTIC"), stat("Itens “não informado”", "1", "exibido como tal, nunca como descumprimento"),
             stat("Cobertura dos dados", "96%", "69 de 72 itens com registro"), min_=220),
        section("Fora do universo padrão (listados à parte — CE04)", table(["Contrato", "Inciso", "Motivo"], [["031/2023 · Beta Tecnologia", "VII — TIC", "Inciso fora do padrão"],
                                                                                                         ["047/2024 · Nu Telecom", "VII — TIC", "Inciso fora do padrão"],
                                                                                                         ["041/2026 · Lambda Software", "VII — TIC", "Inciso fora do padrão"]], dense=True), h=3),
        section("Critérios de cálculo, fontes e registros incompletos",
                p("Regras C19, C20 e C21 (seção 7.2); itens da aba T03.11; fontes: registros validados em ctr, pes, fin, doc e prc. Registros incompletos: 019/2025 — processo de gestão e fiscalização não informado (CD06). "
                  "Campos de texto iniciados por caracteres de fórmula são neutralizados na exportação."), h=3),
        actions(btn("Exportar PDF", kind="primary", ico="download"), btn("Exportar XLSX", ico="download"), btn("Exportar CSV", ico="download"), btn("Voltar ao catálogo", href="Relatorios.dc.html")),
        alert("ok", "Mesma fotografia na prévia e no arquivo", "O total da prévia coincide com o arquivo e com a lista de origem; número de linhas e somatórios coincidem entre formatos (CE01)."),
    ], h1="T13.01 Prévia e exportação", sub="Cabeçalho institucional, posição, filtros, tabela, totais, critérios, fontes e registros incompletos.")
