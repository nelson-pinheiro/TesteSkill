"""T05 Vencimentos e continuidade (abas A–D) e T06 Prorrogações e substituições (lista A–B e detalhe 1–6)."""
import calendar
from shell import *
from data import CONTRATOS, C
from s_inicio import ctr_cell

PROC = {
    "027/2024": ("PRC-2026-009", "Prorrogação · etapa 3 Instrução documental", "Juntar nova pesquisa de preços (PR06) até 12/11/2026"),
    "038/2024": ("—", "Sem procedimento (escopo — art. 111)", "Avaliar mora ou extinção até 25/11/2026"),
    "012/2025": ("PRC-2026-014", "Prorrogação · etapa 4 Análise jurídica", "Parecer jurídico até 16/11/2026"),
    "052/2025": ("ENC-2026-002", "Encerramento · em andamento", "Termo de recebimento definitivo até 30/11/2026"),
    "025/2023": ("PRC-2025-022", "Substituição · concluído", "Planejar transição para 061/2026"),
    "047/2024": ("PRC-2026-017", "Prorrogação · etapa 2 Manifestação da contratada", "Cobrar resposta da contratada até 18/11/2026"),
    "031/2023": ("PRC-2026-011", "Substituição · etapa 3 Instrução documental", "Concluir termo de referência até 30/11/2026"),
    "033/2025": ("PRC-2026-019", "Substituição · etapa 1 Análise inicial", "Levantar início estimado (prazo 31/10/2026 vencido)"),
}


def proc_of(c):
    return PROC.get(c["n"], ("—", "Sem procedimento", "Registrar decisão prevista" if c["dec"] == "Não informada" else f"Abrir procedimento até {c['c15_data']}"))


@screen("Vencimentos.dc.html", "T05.A Vencimentos — Lista por faixas", "r05", "T05.A")
def t05a():
    faixas = ["Ultrapassado", "0–30 dias", "31–60 dias", "61–90 dias", "91–180 dias", "Acima de 180 dias"]
    blocos = []
    for fx in faixas:
        cs = sorted([c for c in CONTRATOS if c["faixa"] == fx], key=lambda c: c["dias"])
        rows = []
        for c in cs:
            pid, sit, prox = proc_of(c)
            di = cat(div(c["c15_data"]), prazo_nat("Parâmetro interno")) if c["c15_data"] else qual("Não informado") if c["dec"] == "Não informada" else small("não aplicável")
            dias = str(c["dias"]) if c["dias"] >= 0 else span(f"{c['dias']} — data final ultrapassada" if c["tipo"] != "Escopo" else f"{c['dias']} — prorrogação automática (art. 111)", style="color:#FFB3B8;font-weight:600;")
            rows.append([ctr_cell(c["n"], c["ctda"], c["sei"] if c["n"] == "021/2025" else None), c["fim"], dias, di, c["c15_sit"],
                         c["dec"] if c["dec"] != "Não informada" else qual("Não informado"), c["gestor"],
                         cat(a(pid, "T06-D1-Resumo.dc.html") if pid.startswith("PRC") else span(pid), div(sit, style=f"font-size:12px;color:{MUTED};")),
                         str(c["pend"]), prox, risco(c["risco"]),
                         col(a("Registrar ou alterar decisão", "T0302-Prazos.dc.html"),
                             a("Abrir procedimento" if pid.startswith("PRC") else "Criar procedimento", "T06-D1-Resumo.dc.html" if pid.startswith("PRC") else "Prorrogacoes.dc.html"),
                             a("Criar providência", "T11B-Todas.dc.html"), gap=4, style="font-size:12px;min-width:130px;")])
        blocos.append(section(f"{fx} · {len(cs)} contrato(s)",
                              table(["Contrato", "Término formalizado", ("Dias restantes", "r"), "Data interna (C15)", "Situação da C15", "Decisão prevista", "Responsável",
                                     "Procedimento e etapa", ("Pend.", "r"), "Próximo passo", "Risco (C18)", "Ações"], rows, minw=1500, dense=True) if rows else p("Nenhum contrato nesta faixa."),
                              h=3))
    return page("T05 Vencimentos e continuidade", "venc", ["Vencimentos", "A Lista por faixas"],
                [filterbar(fsel("Unidade", "Todas as autorizadas", "GERAD", "GERTIC"), fsel("Decisão prevista", "Todas", "Prorrogar", "Substituir", "Encerrar"),
                           fsel("Responsável", "Todos", "P. Nunes", "A. Lima"), fsel("Risco", "Todos", "Existente", "Alto", "Moderado", "Indeterminado")),
                 listbar(14, 3), alert("info", "Faixas sem sobreposição", "Ultrapassado; 0–30; 31–60; 61–90; 91–180; acima de 180 dias. A tramitação não muda a data formal; "
                                       "a decisão registrada pelo operador é validada pelo coordenador."), *blocos],
                tabs_=tabs(T05_TABS, "A Lista por faixas"), sub="Todos os vencimentos e o que garante a continuidade (Diretriz, item 3).",
                acts=[btn("Exportar calendário (RPT03)", href="Relatorios.dc.html", small_=True)])


EVENTOS = {
    (2026, 11): {5: [("Vigência", "027/2024 término")], 15: [("Garantia", "Aviso N08 — 012/2025")], 28: [("Vigência", "012/2025 término")]},
    (2026, 12): {1: [("Marco", "031/2023 M120")], 15: [("Vigência", "052/2025 término")], 23: [("Marco", "047/2024 M30")],
                 30: [("Garantia", "012/2025 apólice")], 31: [("Vigência", "025/2023 término"), ("Marco", "021/2025 M120")]},
}
TOM = {"Vigência": "blue", "Garantia": "purple", "Marco": "orange", "Data-base": "teal"}


def mes_grid(ano, mes):
    cal = calendar.Calendar(firstweekday=6)
    cells = [div(dn, style=f"font-size:12px;color:{MUTED};font-weight:600;padding:4px;") for dn in ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]]
    for dte in cal.itermonthdates(ano, mes):
        ev = EVENTOS.get((ano, mes), {}).get(dte.day, []) if dte.month == mes else []
        cells.append(div(div(str(dte.day), style=f"font-size:12px;color:{TEXT if dte.month == mes else FAINT};font-weight:{700 if (dte.month == mes and dte.day == 10 and mes == 11) else 500};"),
                         *[badge(t_[1], TOM[t_[0]]) for t_ in ev],
                         style=f"min-height:76px;padding:6px;background:{SURF if dte.month == mes else BG};border:1px solid {ACC if (mes == 11 and dte.month == 11 and dte.day == 10) else LINE3};border-radius:4px;display:flex;flex-direction:column;gap:4px;min-width:0;overflow:hidden;"))
    return div(div(*cells, style="display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;min-width:760px;"), style="overflow-x:auto;", aria_hidden="true")


@screen("T05B-Calendario.dc.html", "T05.B Vencimentos — Calendário", "r05", "T05.B")
def t05b():
    lista = [["05/11/2026", badge("Vigência", "blue"), ctr_cell("027/2024", "Gama Vigilância Ltda"), "Término formalizado (ultrapassado)"],
             ["15/11/2026", badge("Garantia", "purple"), ctr_cell("012/2025", "Alfa Serviços Prediais Ltda", href="T0307-Garantias.dc.html"), "Aviso N08 — 45 dias antes da validade"],
             ["28/11/2026", badge("Vigência", "blue"), ctr_cell("012/2025", "Alfa Serviços Prediais Ltda"), "Término formalizado"],
             ["01/12/2026", badge("Marco", "orange"), ctr_cell("031/2023", "Beta Tecnologia S.A.", href="T05D-Marcos.dc.html"), "M120 — recomendação do gestor"],
             ["15/12/2026", badge("Vigência", "blue"), ctr_cell("052/2025", "Ômicron Suprimentos Ltda"), "Término formalizado (encerramento planejado)"],
             ["23/12/2026", badge("Marco", "orange"), ctr_cell("047/2024", "Nu Telecom S.A.", href="T05D-Marcos.dc.html"), "M30 — envio à assessoria jurídica"],
             ["30/12/2026", badge("Garantia", "purple"), ctr_cell("012/2025", "Alfa Serviços Prediais Ltda", href="T0307-Garantias.dc.html"), "Validade do seguro-garantia"],
             ["31/12/2026", badge("Vigência", "blue"), ctr_cell("025/2023", "Xi Reprografia Ltda"), "Término (sucessora 061/2026 inicia em 01/01/2027)"],
             ["31/12/2026", badge("Marco", "orange"), ctr_cell("021/2025", "Zeta Serviços de Limpeza Ltda", href="T05D-Marcos.dc.html"), "M120 — recomendação do gestor"],
             ["01/01/2027", badge("Data-base", "teal"), ctr_cell("019/2025", "Delta Copeiragem Ltda", href="T10B-DatasBase.dc.html"), "Data-base de mão de obra (CCT 2027)"]]
    return page("T05 Vencimentos — calendário", "venc", [("Vencimentos", "Vencimentos.dc.html"), "B Calendário"],
                [row(fsel("Tipo de evento", "Todos", "Vigência", "Garantia", "Data-base", "Marco"), fsel("Visão", "Mês", "Semana"),
                     btn("Mês anterior", small_=True), btn("Próximo mês", small_=True), gap=12, align="flex-end"),
                 section("Novembro de 2026", mes_grid(2026, 11), h=3), section("Dezembro de 2026", mes_grid(2026, 12), h=3),
                 section("Lista equivalente", table(["Data", "Tipo", "Contrato", "Evento"], lista, dense=True), small("Clique no contrato para abrir o registro."))],
                tabs_=tabs(T05_TABS, "B Calendário"), sub="Vencimentos de vigência, garantias, datas-base e marcos por mês ou semana, com lista equivalente.")


@screen("T05C-Continuidade.dc.html", "T05.C Vencimentos — Continuidade", "r05", "T05.C")
def t05c():
    rows = [[ctr_cell("031/2023", "Beta Tecnologia S.A."), "31/03/2027", a("SEI-040014/000931/2026", "T06-D5-Substituicao.dc.html"), "3 Instrução documental", "15/04/2027", "—",
             small("Pregão em 01/2027; homologação em 03/2027; 15 dias para assinatura"), cat(strong("Lacuna de 14 dias", style="color:#FFC489;font-weight:700;"), small(" C02")), risco("Alto"),
             col(a("Rever início estimado", "T06-D5-Substituicao.dc.html"), a("Abrir procedimento", "T06-D5-Substituicao.dc.html"), gap=4, style="font-size:12px;")],
            [ctr_cell("033/2025", "Mu Comunicação Ltda"), "18/02/2027", "SEI-040014/000977/2026", "1 Análise inicial", qual("Não informado"), "—",
             small("Sem cronograma da nova contratação"), cat(badge("Indeterminado", "gray", dashed=True), small(" nunca zero")), risco("Moderado"),
             col(a("Informar início estimado", "T06-D5-Substituicao.dc.html"), a("Providência de levantamento (gerada)", "T11B-Todas.dc.html"), gap=4, style="font-size:12px;")],
            [ctr_cell("025/2023", "Xi Reprografia Ltda"), "31/12/2026", "SEI-040014/000502/2026", "Concluído", "01/01/2027", "01/01/2027 (contrato 061/2026)",
             small("Sucessora formalizada"), cat(strong("Lacuna 0"), small(" (31/12 → 01/01)")), cat(risco("Moderado"), small(" C18 ordem 8 — sucessora ainda não vigente; dias ≤ antecedência")),
             col(a("Abrir sucessora", "Ficha.dc.html"), gap=4, style="font-size:12px;")]]
    return page("T05 Vencimentos — continuidade", "venc", [("Vencimentos", "Vencimentos.dc.html"), "C Continuidade"],
                [listbar(3, 1),
                 table(["Contrato (decisão substituir)", "Término atual", "Processo substitutivo", "Etapa", "Início estimado", "Início formalizado", "Premissas",
                        "Lacuna ou sobreposição (C02)", "Risco", "Ações"], rows, minw=1400, dense=True),
                 section("Memória da C02 — 031/2023", kv([("Fórmula", "máx(0, início da substituta − término atual − 1), datas inclusivas"),
                                                          ("Cálculo", "15/04/2027 − 31/03/2027 − 1 = 14 dias descobertos (CV05)"),
                                                          ("Sobreposição", "Início igual ou anterior ao término: lacuna 0 e dias de sobreposição informados à parte")], min_=320), h=3),
                 alert("info", "Início desconhecido", "Mostra “indeterminado” e gera providência de levantamento; o aviso N12 é de avaliação, sem inventar lacuna (CN12).")],
                tabs_=tabs(T05_TABS, "C Continuidade"), sub="Para cada contrato com decisão “substituir”: processo substitutivo, início estimado e formalizado e lacuna (C02).")


@screen("T05D-Marcos.dc.html", "T05.D Vencimentos — Marcos regulamentares", "r05", "T05.D")
def t05d():
    rows = []
    for c in sorted(CONTRATOS, key=lambda c: c["fim"][6:] + c["fim"][3:5] + c["fim"][:2]):
        rows.append([ctr_cell(c["n"], c["ctda"]), c["fim"], c["dec"],
                     c["m120"] if c["s120"] != "Não aplicável" else "—", c["r120"] or "—", marco(c["s120"]),
                     c["m30"] if c["s30"] != "Não aplicável" else "—", c["r30"] or "—", marco(c["s30"]),
                     col(a("Registrar recomendação", "T06-D4-Marcos.dc.html") if c["s120"] in ("A cumprir", "Descumprido") else None,
                         a("Registrar envio jurídico", "T06-D4-Marcos.dc.html") if c["s30"] in ("A cumprir", "Descumprido") else None,
                         a("Abrir procedimento", "T06-D1-Resumo.dc.html"), gap=4, style="font-size:12px;")])
    return page("T05 Vencimentos — marcos regulamentares", "venc", [("Vencimentos", "Vencimentos.dc.html"), "D Marcos regulamentares"],
                [row(prazo_nat("Legal regulamentar"), small("M120: Decreto RJ nº 48.817/2023, art. 22, XVII · M30: art. 22, XIX · regra C19"), gap=8),
                 alert("info", "Exemplo de aceite (CV07)", "Término 28/11/2026 → M120 = 31/07/2026 e M30 = 29/10/2026. Sem registros, ambos “descumprido” em 10/11/2026; "
                       "com recomendação em 31/07/2026 e envio em 05/11/2026, M120 “cumprido” e M30 “cumprido com atraso”."),
                 listbar(len(rows), 0),
                 table(["Contrato", "Término", "Decisão", "M120 limite", "Registro", "Situação M120", "M30 limite", "Registro", "Situação M30", "Ações"], rows, minw=1300, dense=True),
                 small("“Não aplicável”: decisão encerrar, contrato por escopo ou contrato encerrado; M30 só quando a decisão prevista é prorrogar. "
                       "São marcos regulamentares, não parâmetros internos, e não mudam com a data interna da C15.")],
                tabs_=tabs(T05_TABS, "D Marcos regulamentares"), sub="Por contrato: data-limite M120 e M30, data do registro e situação (C19).")


# ======================================================================= T06
PROCS_A = [
    ("PRC-2026-014", "012/2025", "Alfa Serviços Prediais Ltda", "Prorrogação", "SEI-040014/000512/2026", "15/07/2026", "31/10/2026 → 20/11/2026", "P. Nunes", "ASSJUR",
     "4 Análise jurídica", "05/11/2026 · remessa à ASSJUR", "5", "PR08, PR11", "Parecer jurídico até 16/11/2026", ("Cumprido", "Cumprido com atraso")),
    ("PRC-2026-009", "027/2024", "Gama Vigilância Ltda", "Prorrogação", "SEI-040014/000388/2026", "20/06/2026", "08/07/2026 → 30/10/2026", "P. Nunes", "GERAD",
     "3 Instrução documental", "14/10/2026 · devolução da ASSJUR (pesquisa de preços insuficiente)", "27", "PR06, PR08", "Juntar nova pesquisa até 12/11/2026", ("Cumprido", "Descumprido")),
    ("PRC-2026-017", "047/2024", "Nu Telecom S.A.", "Prorrogação", "SEI-040014/000844/2026", "02/10/2026", "22/10/2026", "A. Lima", "Contratada (externo)",
     "2 Manifestação da contratada", "06/10/2026 · remessa à contratada", "35", "PR04", "Cobrar resposta até 18/11/2026", ("Descumprido", "A cumprir")),
    ("PRC-2026-011", "031/2023", "Beta Tecnologia S.A.", "Substituição", "SEI-040014/000931/2026", "05/08/2026", "30/09/2026 → 15/12/2026", "A. Lima", "GERTIC",
     "3 Instrução documental", "28/10/2026 · recebimento da pesquisa de preços", "13", "—", "Concluir termo de referência até 30/11/2026", ("A cumprir", "Não aplicável")),
    ("PRC-2026-019", "033/2025", "Mu Comunicação Ltda", "Substituição", "SEI-040014/000977/2026", "28/10/2026", "31/10/2026", "T. Vieira", "CHEGAB",
     "1 Análise inicial", "28/10/2026 · abertura", "13", "Início estimado não informado", "Levantar cronograma (prazo 31/10/2026 vencido)", ("Descumprido", "Não aplicável")),
]


@screen("Prorrogacoes.dc.html", "T06.A Procedimentos — Em andamento", "r05", "T06.A")
def t06a():
    rows = []
    for pid, n, ct, tp, sei, ab, pz, resp, un, et, ult, dsa, pend, prox, (m1, m2) in PROCS_A:
        href = "T06-D5-Substituicao.dc.html" if tp == "Substituição" else "T06-D1-Resumo.dc.html"
        rows.append([cat(a(pid, href, style=f"color:{ACC};font-weight:600;"), div(f"{n} · {ct}", style=f"font-size:12px;color:{TEXT2};")), tp, sei, ab, pz, resp, un, et, ult,
                     span(dsa, style="color:#FFC489;font-weight:600;") if int(dsa) > 15 else dsa, pend, prox,
                     cat(row(small("M120"), marco(m1), gap=4), row(small("M30"), marco(m2), gap=4))])
    return page("T06 Prorrogações e substituições", "prorrog", ["Prorrogações e substituições", "A Em andamento"],
                [filterbar(fsel("Tipo", "Todos", "Prorrogação", "Substituição"), fsel("Etapa", "Todas", "1 Análise inicial", "2 Manifestação da contratada", "3 Instrução documental", "4 Análise jurídica"),
                           fsel("Responsável", "Todos", "P. Nunes", "A. Lima", "T. Vieira"), fsel("Unidade atual", "Todas", "GERAD", "ASSJUR", "Contratada (externo)")),
                 listbar(5, 1, acts=[btn("Exportar RPT04", href="Relatorios.dc.html", small_=True)]),
                 table(["Procedimento / contrato", "Tipo", "Processo SEI", "Abertura", "Prazo interno original → revisado", "Responsável", "Unidade atual", "Etapa",
                        "Última movimentação", ("Dias sem avanço", "r"), "Pendências", "Próxima ação e prazo", "Marcos"], rows, minw=1700, dense=True),
                 small("Prazo interno revisado preserva o original. Unidade atual e última movimentação podem ser atualizadas por consulta ao SEI, sempre com a data da consulta.")],
                tabs_=tabs(T06_TABS, "A Em andamento"), acts=[btn("Novo procedimento", href="T06-D1-Resumo.dc.html", kind="primary", ico="plus")],
                sub="Acompanhar cada procedimento de prorrogação ou substituição até a formalização (Diretriz, item 4).")


@screen("T06B-Concluidos.dc.html", "T06.B Procedimentos — Concluídos e cancelados", "r05", "T06.B")
def t06b():
    rows = [[a("PRC-2026-003", "T06-D1-Resumo.dc.html"), "060/2024 · Sigma Climatização Ltda", "Prorrogação", "02/02/2026", "20/05/2026", estado("Concluída"), "Prorrogado por 12 meses", a("2º Termo aditivo (formalizado em 22/05/2026)", "T0401-Formalizacao.dc.html"), a("Reabrir com motivo", "T06-D1-Resumo.dc.html")],
            [a("PRC-2025-022", "T06-D5-Substituicao.dc.html"), "025/2023 · Xi Reprografia Ltda", "Substituição", "12/11/2025", "30/09/2026", estado("Concluída"), "Sucessora contratada", "Contrato 061/2026 (início 01/01/2027)", a("Reabrir com motivo", "T06-D1-Resumo.dc.html")],
            [a("PRC-2026-006", "T06-D1-Resumo.dc.html"), "017/2024 · Rho Eventos Ltda", "Prorrogação", "10/03/2026", "10/06/2026", estado("Cancelada"), "Motivo: extinção antecipada do contrato", "—", a("Reabrir com motivo", "T06-D1-Resumo.dc.html")]]
    return page("T06 Prorrogações e substituições — concluídos e cancelados", "prorrog", [("Prorrogações e substituições", "Prorrogacoes.dc.html"), "B Concluídos e cancelados"],
                [listbar(3, 0), table(["Procedimento", "Contrato", "Tipo", "Abertura", "Conclusão ou cancelamento", "Situação", "Resultado", "Instrumento", "Ação"], rows, minw=1200, dense=True),
                 alert("info", None, "Concluir o procedimento não formaliza: a prorrogação só altera a vigência pela formalização em T04.01 (CR01).")],
                tabs_=tabs(T06_TABS, "B Concluídos e cancelados"), sub="Os mesmos dados, com data de conclusão, resultado e instrumento.")


def proc_head(sub=False):
    if sub:
        return div(row(strong("PRC-2026-011 · Substituição", style=f"font-size:18px;color:{TEXT};font-weight:700;"), estado("Em andamento"), gap=10),
                   small("Contrato 031/2023 · Beta Tecnologia S.A. · SEI-040014/000931/2026 · responsável A. Lima · etapa 3 Instrução documental"),
                   style=f"padding:16px;background:{SURF};border:1px solid {LINE};border-radius:8px;display:flex;flex-direction:column;gap:6px;")
    return div(row(strong("PRC-2026-014 · Prorrogação", style=f"font-size:18px;color:{TEXT};font-weight:700;"), estado("Em andamento"), gap=10),
               small("Contrato 012/2025 · Alfa Serviços Prediais Ltda · SEI-040014/000512/2026 · responsável P. Nunes · unidade atual ASSJUR · etapa 4 Análise jurídica"),
               style=f"padding:16px;background:{SURF};border:1px solid {LINE};border-radius:8px;display:flex;flex-direction:column;gap:6px;")


def det_page(tab, body, sub=False):
    tl = [t_ if t_[0] != "5 Substituição" or not sub else (t_[0], t_[1]) for t_ in T06_DET]
    return page(f"T06 Detalhe do procedimento — {tab}", "prorrog",
                [("Prorrogações e substituições", "Prorrogacoes.dc.html"), "PRC-2026-011" if sub else "PRC-2026-014", tab],
                [proc_head(sub), tabs(tl, tab, label="Abas do procedimento"), *body], h1="Detalhe do procedimento",
                sub="Aba 5 visível quando o tipo é substituição." if not sub else "Procedimento de substituição — as demais abas do protótipo mostram o PRC-2026-014.")


@screen("T06-D1-Resumo.dc.html", "T06 Detalhe — 1 Resumo", "r05", "T06.1")
def d1():
    return det_page("1 Resumo", [
        section("Resumo", kv([("Tipo", "Prorrogação"), ("Contrato", a("012/2025 · Alfa Serviços Prediais Ltda", "Ficha.dc.html")), ("Processo SEI", "SEI-040014/000512/2026"),
                              ("Data de abertura", "15/07/2026"), ("Responsável", "P. Nunes"), ("Unidade atual", "ASSJUR (consultado no SEI em 10/11/2026 07:00)"),
                              ("Etapa", "4 Análise jurídica"), ("Prazo interno original", cat(div("31/10/2026"), prazo_nat("Parâmetro interno"))),
                              ("Prazo interno revisado", "20/11/2026 · motivo: devolução da DIRAF em 19/10/2026 (classificação orçamentária)"),
                              ("Pendências", "PR08 e PR11 (atualizar antes da assinatura)"), ("Próxima ação e prazo", "Parecer jurídico até 16/11/2026"), ("Situação", "Em andamento")])),
        section("Ações", actions(btn("Editar", ico="edit"), btn("Rever prazo (com motivo)"), btn("Trocar responsável"), btn("Concluir (exige resultado)"),
                                 btn("Cancelar (exige motivo)", kind="danger"), btn("Formalizar (T04.01)", href="T0401-Formalizacao.dc.html", kind="primary")),
                alert("warn", "Concluir não formaliza", "Concluir o procedimento não altera a vigência; o comando “Formalizar” leva a T04.01, onde o instrumento assinado é registrado (CR01)."),
                small("O prazo original é preservado ao rever o prazo.")),
    ])


@screen("T06-D2-Etapas.dc.html", "T06 Detalhe — 2 Etapas e movimentações", "r05", "T06.2")
def d2():
    etapas = ["Análise inicial", "Manifestação da contratada", "Instrução documental", "Análise jurídica", "Autorização", "Assinatura", "Publicação"]
    trail = tag("ol", *[tag("li", span(str(i + 1), style=f"display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;font-size:12px;font-weight:700;"
                                                         f"{'background:' + ACC + ';color:#06111F;' if i == 3 else ('background:' + ACCBG + ';color:' + ACC2 + ';' if i < 3 else 'border:1px solid ' + LINE2 + ';color:' + MUTED + ';')}"),
                                span(e_, style=f"font-size:13px;color:{TEXT if i == 3 else MUTED};font-weight:{600 if i == 3 else 500};"),
                                style="display:flex;align-items:center;gap:8px;") for i, e_ in enumerate(etapas)],
                aria_label="Trilha de etapas", style="list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px 18px;")
    mov = [["15/07/2026 10:02", "Abertura", "—", "GERAD", "P. Nunes", "Despacho de abertura", "1"],
           ["20/07/2026 14:30", "Remessa", "GERAD", "Contratada", "P. Nunes", "Ofício de consulta (PR03)", "2"],
           ["28/07/2026 09:10", "Recebimento", "Contratada", "GERAD", "R. Costa", "Resposta da contratada (PR04)", "2 (recebimento não conclui etapa)"],
           ["29/07/2026 11:00", "Avanço de etapa", "—", "—", "P. Nunes", "—", "2 → 3"],
           ["12/10/2026 15:45", "Remessa", "GERAD", "DIRAF", "P. Nunes", "Pedido de disponibilidade orçamentária (PR07)", "3"],
           ["19/10/2026 10:20", "Devolução", "DIRAF", "GERAD", "L. Martins", "Motivo: classificação orçamentária divergente", "3"],
           ["05/11/2026 16:20", "Remessa", "GERAD", "ASSJUR", "P. Nunes", "Procedimento instruído (M30 registrado)", "3 → 4"]]
    return det_page("2 Etapas e movimentações", [
        section("Trilha das etapas configuráveis", trail, small("Etapas configuráveis em T14.02; retorno a etapa anterior exige motivo.")),
        section("Histórico de movimentações (somente inserção)",
                table(["Instante", "Tipo", "Origem", "Destino", "Autor", "Evidência ou motivo", "Etapa"], mov, minw=1000, dense=True),
                actions(btn("Registrar remessa"), btn("Registrar recebimento"), btn("Registrar devolução (com motivo)"), btn("Avançar etapa", kind="primary"), btn("Retornar etapa (exige motivo)")),
                small("Movimentação registra autor, momento, etapas e unidades (CR01).")),
    ])


@screen("T06-D3-Checklist.dc.html", "T06 Detalhe — 3 Lista de verificação", "r05", "T06.3")
def d3():
    itens = [("PR01", "Previsão de prorrogação no edital e no contrato, e vigência", "Decreto RJ nº 48.817/2023, art. 22, § 1º, I", "Atendido", "Edital, item 4.2 · contrato, cláusula 3ª", "R. Costa"),
             ("PR02", "Manifestação justificada de interesse da Administração", "art. 22, § 1º, II", "Atendido", "doc. 46600102", "P. Nunes"),
             ("PR03", "Consulta à contratada sobre o interesse na prorrogação", "art. 22, § 1º, III", "Atendido", "Ofício GERAD nº 077/2026", "P. Nunes"),
             ("PR04", "Resposta da contratada quanto ao interesse", "art. 22, § 1º, IV", "Atendido", "doc. 46602210", "R. Costa"),
             ("PR05", "Objeto e escopo inalterados pela prorrogação", "art. 22, § 1º, V", "Atendido", "Manifestação do gestor", "P. Nunes"),
             ("PR06", "Pesquisa de preços que demonstre a vantajosidade, quando for o caso", "art. 22, § 1º, VI", "Atendido", "doc. 47010455", "R. Costa"),
             ("PR07", "Demonstração de disponibilidade orçamentária", "art. 22, § 1º, VII", "Atendido", "Declaração DIRAF de 03/11/2026", "L. Martins"),
             ("PR08", "Documentação vigente de habilitação e manifestação conclusiva sobre a regularidade", "art. 22, § 1º, VIII", "Pendente", "Certidão federal vence em 12/11/2026", "—"),
             ("PR09", "Recomendação do gestor à autoridade competente (mínimo de 120 dias corridos)", "art. 22, XVII", "Atendido", "doc. 46610021 (31/07/2026)", "P. Nunes"),
             ("PR10", "Checklist de Prorrogação da PGE/RJ e manifestação conclusiva de gestor e fiscais", "art. 22, XIX", "Atendido", "doc. 47720401", "P. Nunes"),
             ("PR11", "Regularidade fiscal e consultas ao CEIS e ao CNEP antes de prorrogar", "Lei nº 14.133/2021, art. 91, § 4º", "Pendente", "A realizar antes da assinatura", "—"),
             ("PR12", "Inexistência de pedido de reequilíbrio pendente anterior à prorrogação", "Lei nº 14.133/2021, art. 131, parágrafo único", "Atendido", "Consulta a T10 em 05/11/2026", "M. Silva")]
    rows = [[strong(c_), t_, small(f_), estado(s_), doc, ver, a("Marcar", "T06-D3-Checklist.dc.html")] for c_, t_, f_, s_, doc, ver in itens]
    return det_page("3 Lista de verificação", [
        section("Itens PR01 a PR12", table(["Item", "Descrição", "Fundamento", "Situação", "Documento ou referência", "Verificador", ""], rows, minw=1100, dense=True),
                row(badge("10 atendidos", "green"), badge("2 pendentes", "yellow"), badge("0 não aplicáveis", "gray"), gap=6),
                small("Atendido exige documento ou referência; não aplicável exige justificativa. Itens obrigatórios pendentes impedem o avanço para a análise jurídica, salvo justificativa do coordenador.")),
        alert("warn", "Avanço autorizado com justificativa do coordenador", "M. Silva, 05/11/2026: “PR08 e PR11 serão atualizados imediatamente antes da assinatura, pela validade curta das certidões.”"),
    ])


@screen("T06-D4-Marcos.dc.html", "T06 Detalhe — 4 Marcos e prazos", "r05", "T06.4")
def d4():
    return det_page("4 Marcos e prazos", [
        section("Marcos regulamentares (C19)",
                table(["Marco", "Data-limite", "Data do registro", "Documento", "Situação", "Natureza"],
                      [["M120 — recomendação do gestor", "31/07/2026", "31/07/2026", "doc. 46610021", marco("Cumprido"), cat(prazo_nat("Legal regulamentar"), small(" art. 22, XVII"))],
                       ["M30 — envio à assessoria jurídica", "29/10/2026", "05/11/2026", "doc. 47720415", marco("Cumprido com atraso"), cat(prazo_nat("Legal regulamentar"), small(" art. 22, XIX"))]], dense=True),
                actions(btn("Registrar recomendação do gestor"), btn("Registrar envio à assessoria jurídica"))),
        section("Comparação com o prazo interno",
                table(["Referência", "Data", "Natureza"],
                      [["Data interna de início das providências (C15)", "31/07/2026", prazo_nat("Parâmetro interno")],
                       ["Prazo interno do procedimento — original", "31/10/2026", prazo_nat("Parâmetro interno")],
                       ["Prazo interno do procedimento — revisado", "20/11/2026", prazo_nat("Parâmetro interno")],
                       ["M30 — limite regulamentar", "29/10/2026", prazo_nat("Legal regulamentar")]], dense=True),
                small("Os marcos não mudam com a data interna nem com a revisão do prazo interno.")),
    ])


@screen("T06-D5-Substituicao.dc.html", "T06 Detalhe — 5 Substituição", "r05", "T06.5")
def d5():
    return det_page("5 Substituição", [
        section("Contratação substituta", kv([("Processo substitutivo", "SEI-040014/000931/2026"), ("Contrato sucessor", qual("Não informado")),
                                              ("Início estimado", "15/04/2027"), ("Início formalizado", "—"),
                                              ("Premissas", "Pregão em 01/2027; homologação em 03/2027; 15 dias para assinatura"),
                                              ("Lacuna (C02)", cat(strong("14 dias", style="color:#FFC489;font-weight:700;"), small(" · término 31/03/2027")))]),
                actions(btn("Vincular processo"), btn("Vincular contrato sucessor"), btn("Rever estimativa (com premissas)", kind="primary"))),
        alert("info", None, "Início desconhecido mostra “indeterminado” e gera providência de levantamento; nunca é tratado como lacuna zero."),
    ], sub=True)


@screen("T06-D6-Documentos.dc.html", "T06 Detalhe — 6 Documentos", "r05", "T06.6")
def d6():
    return det_page("6 Documentos", [
        section("Documentos do procedimento",
                table(["Tipo", "Número SEI", "Data", "Versão", "Restrição", ""],
                      [["Despacho de abertura", "doc. 46590011", "15/07/2026", "1", "Pública", a("Abrir", "T06-D6-Documentos.dc.html")],
                       ["Recomendação do gestor (M120)", "doc. 46610021", "31/07/2026", "1", "Pública", a("Abrir", "T06-D6-Documentos.dc.html")],
                       ["Pesquisa de preços", "doc. 47010455", "28/10/2026", "2 (v1 preservada)", "Restrita", a("Abrir", "T06-D6-Documentos.dc.html")],
                       ["Checklist PGE/RJ e manifestação conclusiva", "doc. 47720401", "05/11/2026", "1", "Pública", a("Abrir", "T06-D6-Documentos.dc.html")],
                       ["Minuta do 2º termo aditivo", "doc. 47720409", "05/11/2026", "1", "Interna", a("Abrir", "T06-D6-Documentos.dc.html")]], dense=True),
                actions(btn("Anexar arquivo", ico="upload"), btn("Referenciar documento SEI")), small("Versões preservadas; minuta não altera a vigência.")),
    ])
