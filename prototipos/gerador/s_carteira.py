"""T02 Carteira de contratos (abas A–D) e T03 Ficha única do contrato (abas T03.01–T03.11 e consulta histórica)."""
from shell import *
from data import CONTRATOS, ENCERRADOS, C
from s_inicio import ctr_cell


def filtros_carteira():
    busca = div(field("Busca (número normalizado, objeto, contratada, CNPJ ou processo SEI)", "021/2025", placeholder="Ex.: 12/2025, Alfa, 12.345.678/0001-95"),
                alert("info", "Número repetido: “021/2025” corresponde a 2 contratos autorizados",
                      "Desambiguados por processo e contratada: SEI-040014/000315/2025 · Zeta Serviços de Limpeza Ltda (DIRSE) e "
                      "SEI-040014/000877/2025 · Eta Transportes Ltda (CHEGAB). Ambos destacados na lista."),
                style="display:flex;flex-direction:column;gap:10px;")
    return col(busca, filterbar(fsel("Unidade", "Todas as autorizadas", "GERAD", "GERTIC", "DIRAF", "DIRSE", "CHEGAB"),
                                fsel("Categoria", "Todas", "Serviços prediais", "Tecnologia da informação"), fsel("Grupo", "Todos", "Manutenção", "Vigilância"),
                                fsel("Tipo", "Todos", "Serviço contínuo", "Fornecimento", "Escopo"),
                                fsel("Situação de vigência", "Todas", "Em vigor", "Data final ultrapassada", "Prorrogada automaticamente (art. 111)"),
                                fsel("Faixa de término", "Todas", "Ultrapassado", "0–30 dias", "31–60 dias", "61–90 dias", "91–180 dias", "Acima de 180 dias"),
                                fsel("Decisão prevista", "Todas", "Prorrogar", "Substituir", "Encerrar", "Analisar", "Não informada"),
                                fsel("Gestor", "Todos", "P. Nunes", "A. Lima", "T. Vieira"),
                                fsel("Qualidade do dado", "Todas", "Validado", "Importado – não validado", "Não informado"),
                                fsel("Risco", "Todos", "Existente", "Alto", "Moderado", "Indeterminado", "Sem risco identificado")), gap=12)


def carteira_rows(lista, extra=None):
    rows = []
    for c in lista:
        dup = c["n"] == "021/2025"
        num = cat(tag("input", type="checkbox", aria_label=f"Selecionar {c['n']}", style=f"width:18px;height:18px;accent-color:{ACC};margin:0 6px 0 0;vertical-align:middle;"),
                  a(c["n"], "Ficha.dc.html", style=f"color:{ACC};font-weight:600;"),
                  div(c["sei"], style=f"font-size:11px;color:{FAINT};") if dup else None,
                  badge("Número repetido", "blue") if dup else None)
        mensal = c["mensal"] if c["mensal"] != "Não aplicável" else span("não aplicável", style=f"color:{MUTED};font-style:italic;")
        sit = c["sit"] if c["sit"] == "Em vigor" else span(c["sit"], style="color:#FFC489;font-weight:600;")
        dias = str(c["dias"]) if c["dias"] >= 0 else span(str(c["dias"]), style="color:#FFB3B8;font-weight:600;")
        r = [num, c["obj"], c["ctda"], c["un"], c["tipo"], sit, c["fim"], dias, cat(div(c["valor"]), small("vigência corrente")), mensal,
             c["dec"] if c["dec"] != "Não informada" else qual("Não informado"), risco(c["risco"]), str(c["pend"]), qual(c["qual"])]
        rows.append(r)
    return rows


COLS_A = ["Número", "Objeto resumido", "Contratada", "Unidade", "Tipo", "Situação", "Término formalizado", ("Dias", "r"),
          ("Valor atualizado (escopo)", "r"), ("Valor mensal", "r"), "Decisão prevista", "Risco", ("Pend.", "r"), "Qualidade"]


def carteira_acts():
    return [btn("Novo contrato (digitar)", href="T04-P1-Identificacao.dc.html", kind="primary", ico="plus"),
            btn("Importar (L02 ou L01)", href="Importacao.dc.html", ico="upload"),
            btn("Buscar na fonte (PNCP)", href="T1407-Conectores.dc.html", ico="plug")]


def lote():
    return row(small("Seleção múltipla — ações em lote permitidas:"), btn("Atribuir responsável", small_=True), btn("Exportar seleção", small_=True), gap=8)


@screen("Carteira.dc.html", "T02.A Carteira — Vigentes", "r02", "T02.A")
def t02a():
    vig = [c for c in CONTRATOS]
    return page("T02 Carteira de contratos", "carteira", ["Carteira", "A Vigentes"],
                [filtros_carteira(), listbar(len(vig), 3, extra=small("(027/2024 e 038/2024 aparecem com a situação por extenso)")), lote(),
                 table(COLS_A, carteira_rows(vig), minw=1640, dense=True),
                 pager("1–14 de 14 · 50 linhas por página · ordenação: término formalizado crescente"),
                 small("Valor mensal só em preço mensal fixo formalizado; nos demais, “não aplicável” (tabela 6.4). A exportação respeita unidade, perfil, filtros e posição.")],
                tabs_=tabs(T02_TABS, "A Vigentes"), acts=carteira_acts(),
                sub="Localizar contratos e conhecer sua situação. Fonte: ctr.vw_carteira.")


@screen("T02B-Encerrados.dc.html", "T02.B Carteira — Encerrados e extintos", "r02", "T02.B")
def t02b():
    rows = []
    for e in ENCERRADOS:
        passivo = e["lap"] != "0,00"
        rows.append([a(e["n"], "Ficha.dc.html", style=f"color:{ACC};font-weight:600;"), e["obj"], e["ctda"], e["un"], e["tipo"], e["sit"], e["fim"],
                     cat(div(e["valor"]), small("global acumulado")), e["mensal"] if e["mensal"] != "Não aplicável" else span("não aplicável", style=f"color:{MUTED};font-style:italic;"),
                     risco(e["risco"]), e["fech"],
                     strong(e["lap"], style="color:#FFC489;font-weight:700;") if passivo else "0,00",
                     span("Encerrado com passivo — continua consultável", style="color:#FFC489;font-weight:600;") if passivo else "—"])
    return page("T02 Carteira — encerrados e extintos", "carteira", [("Carteira", "Carteira.dc.html"), "B Encerrados e extintos"],
                [filtros_carteira(), listbar(3, 0),
                 table(["Número", "Objeto resumido", "Contratada", "Unidade", "Tipo", "Situação", "Término", ("Valor atualizado", "r"), ("Valor mensal", "r"),
                        "Risco", "Situação de fechamento", ("Saldo liquidado a pagar", "r"), "Destaque"], rows, minw=1500, dense=True),
                 alert("info", "Vigência, execução e fechamento são dimensões independentes",
                       "015/2022 está encerrado na vigência e aberto em pendências financeiras (R$ 2.000,00 liquidados a pagar — RPT07)."),
                 pager("1–3 de 3")],
                tabs_=tabs(T02_TABS, "B Encerrados e extintos"), acts=carteira_acts(), sub="As mesmas colunas, com a situação de fechamento e o saldo liquidado a pagar.")


RASCUNHOS = [
    ("063/2026", "Upsilon Brigada Ltda", "Brigada de incêndio e primeiros socorros", "Rascunho", "Passo 6 (Prazos) em preenchimento; passos 7 e revisão pendentes",
     "R. Costa", "09/11/2026", "T04-P6-Prazos.dc.html"),
    ("058/2026", "Tau Arquivística Ltda", "Guarda e gestão de arquivo", "Importado – não validado", "Lote L01 de 03/11/2026: CNPJ divergente entre as abas Contratos e Comissões",
     "R. Costa", "03/11/2026", "T140405-Validacao.dc.html"),
    ("049/2025", "Phi Consultoria Ltda", "Consultoria atuarial", "Devolvido", "Devolvido por M. Silva em 06/11/2026: “instrumento assinado não anexado” · saneamento até 13/11/2026",
     "R. Costa", "06/11/2026", "T04-Revisao.dc.html"),
]


@screen("T02C-Rascunhos.dc.html", "T02.C Carteira — Rascunhos e não validados", "r02", "T02.C")
def t02c():
    rows = []
    for n, ct, ob, sit, mot, resp, desde, href in RASCUNHOS:
        st_ = qual(sit) if sit.startswith("Importado") else estado(sit)
        rows.append([a(n, href, style=f"color:{ACC};font-weight:600;"), ct, ob, st_, mot, resp, desde,
                     col(a("Continuar cadastro", href), a("Submeter à validação", "T04-Revisao.dc.html"),
                         a("Validar ou devolver (coordenador)", "T04-Revisao.dc.html"), gap=4, style="font-size:12px;")])
    return page("T02 Carteira — rascunhos e não validados", "carteira", [("Carteira", "Carteira.dc.html"), "C Rascunhos e não validados"],
                [listbar(3, 3),
                 table(["Contrato", "Contratada", "Objeto", "Situação", "Motivo da pendência", "Responsável pela pendência", "Desde", "Ações"], rows, dense=True),
                 alert("info", "Rascunho não alimenta totais (MIG08)", "Contratos em rascunho, importados não validados ou devolvidos não entram em indicadores nem relatórios oficiais. "
                       "A validação é feita por pessoa diferente de quem lançou (segregação — CP03).")],
                tabs_=tabs(T02_TABS, "C Rascunhos e não validados"), acts=carteira_acts(), sub="Contratos em rascunho, importados não validados ou devolvidos, com motivo e responsável.")


@screen("T02D-Todos.dc.html", "T02.D Carteira — Todos", "r02", "T02.D")
def t02d():
    rows = [[a(c["n"], "Ficha.dc.html", style=f"color:{ACC};font-weight:600;"), c["ctda"], c["un"], badge("Vigente", "blue"), c["sit"], c["fim"], c["valor"], risco(c["risco"]), qual(c["qual"])]
            for c in CONTRATOS]
    rows += [[a(e["n"], "T02B-Encerrados.dc.html", style=f"color:{ACC};font-weight:600;"), e["ctda"], e["un"], badge("Encerrado ou extinto", "gray"), e["sit"], e["fim"], e["valor"],
              risco(e["risco"]), qual(e["qual"])] for e in ENCERRADOS]
    rows += [[a(r[0], r[7], style=f"color:{ACC};font-weight:600;"), r[1], "GERAD", badge("Rascunho ou não validado", "purple"), r[3], "—", "—", risco("Indeterminado"),
              qual("Importado – não validado") if r[3].startswith("Importado") else qual("Não informado")] for r in RASCUNHOS]
    return page("T02 Carteira — todos", "carteira", [("Carteira", "Carteira.dc.html"), "D Todos"],
                [filtros_carteira(), listbar(len(rows), 6),
                 table(["Número", "Contratada", "Unidade", "Situação (aba de origem)", "Situação detalhada", "Término", ("Valor atualizado", "r"), "Risco", "Qualidade"], rows, minw=1200, dense=True),
                 pager(f"1–{len(rows)} de {len(rows)}")],
                tabs_=tabs(T02_TABS, "D Todos"), acts=carteira_acts(), sub="União das abas, com coluna de situação.")


# =================================================================== T03 Ficha
def ficha_header(hist=False):
    c = C("012/2025")
    if hist:
        items = [("Situação de vigência", "Em vigor"), ("Término formalizado", "28/11/2026"), ("Dias restantes em 15/03/2026", "258"),
                 ("Valor atualizado (vigência corrente)", "R$ 1.020.000,00"), ("Valor mensal vigente", "R$ 85.000,00"),
                 ("Designação", desig("Completa")), ("Qualidade", qual("Validado"))]
    else:
        items = [("Situação de vigência", "Em vigor"), ("Qualidade do dado", qual("Validado")), ("Término formalizado", "28/11/2026"),
                 ("Dias restantes (C01)", "18"), ("Valor atualizado (vigência corrente)", "R$ 1.074.400,00"),
                 ("Cobertura de empenho", "Sem insuficiência no horizonte (até 28/11/2026)"), ("Risco (C18)", risco("Alto")),
                 ("Designação (C20)", desig("Completa — 4 apontamentos"))]
    return div(
        row(col(row(span("012/2025", style=f"font-size:22px;font-weight:700;color:{TEXT};"), badge("Serviço contínuo · mensal fixo", "gray"), gap=10),
                span(c["obj"], style=f"font-size:15px;color:{TEXT2};"),
                small(f"{c['ctda']} · CNPJ {c['cnpj']} · Unidade {c['un']} · Processo principal {c['sei']}"), gap=4),
            div(field("Situação em uma data", "15/03/2026" if hist else "", kind="date", placeholder="dd/mm/aaaa",
                      note="Reconstrói vigência, preço, valor e designações aplicáveis; somente leitura."),
                btn("Consultar", href="T03-Historico.dc.html", small_=True), style="display:flex;align-items:flex-end;gap:8px;max-width:420px;"),
            justify="space-between", align="flex-start"),
        kv(items, min_=170),
        style=f"display:flex;flex-direction:column;gap:16px;padding:18px 20px;background:{SURF};border:1px solid {LINE};border-radius:8px;")


def evidencias(grupo, docs, origem_txt):
    lis = [tag("li", row(icon("file", 16, MUTED), div(a(t_, "T0309-Documentos.dc.html"), small(sub)), gap=8, align="flex-start")) for t_, sub in docs]
    return tag("aside", tag("h2", "Painel de evidências", style=f"margin:0;font-size:15px;color:{TEXT};"),
               small(f"Grupo selecionado: {grupo}"),
               tag("ul", *lis, style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px;font-size:13px;"),
               div(strong("Origem dos campos", style=f"font-size:13px;color:{TEXT};"), small(origem_txt), style="display:flex;flex-direction:column;gap:4px;"),
               origem("Digitado", "R. Costa", "01/12/2025 10:14"),
               small("Abrir documento respeita a permissão; endereço direto sem permissão é negado."),
               aria_label="Painel de evidências",
               style=f"flex:1 1 280px;max-width:340px;min-width:0;align-self:flex-start;display:flex;flex-direction:column;gap:12px;padding:18px;background:{SURF};border:1px solid {LINE};border-radius:8px;box-sizing:border-box;")


def ficha(tab, ref, body, grupo, docs, origem_txt, edit_href, edit_txt="Editar (abre o passo de T04 e gera rascunho)", hist=False, validacao="Validado em 02/04/2026 por M. Silva"):
    head = row(row(strong(tab.split(" ", 1)[1] if " " in tab else tab, style=f"font-size:18px;color:{TEXT};font-weight:600;"),
                   estado("Validado"), small(validacao), gap=8),
               btn(edit_txt, href=edit_href, ico="edit", small_=True) if edit_href and not hist else
               small("Somente leitura na consulta histórica" if hist else "Aba calculada — sem edição direta"),
               justify="space-between")
    content = div(div(head, *body, style="flex:999 1 560px;min-width:0;display:flex;flex-direction:column;gap:16px;"),
                  evidencias(grupo, docs, origem_txt), style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start;")
    return page(f"{ref} Ficha do contrato 012/2025", "carteira",
                [("Carteira", "Carteira.dc.html"), "012/2025 Alfa Serviços Prediais", tab],
                [ficha_header(hist), tabs(T03_TABS, tab, label="Abas da ficha"), content],
                band=hist_band() if hist else None,
                acts=[btn("Nova providência", href="T11B-Todas.dc.html", small_=True, ico="plus"), btn("Ficha consolidada (RPT02)", href="Relatorios.dc.html", small_=True)],
                h1="Ficha única do contrato", sub="Tudo o que se sabe do contrato, por abas, com fonte e situação de validação de cada grupo.")


DOCS_CT = [("Contrato 012/2025 (assinado em 28/11/2025)", "SEI-040014/000418/2025 · doc. 41029337 · conferido"),
           ("1º Termo aditivo (31/03/2026)", "SEI-040014/000418/2025 · doc. 43551820 · conferido")]


@screen("Ficha.dc.html", "T03.01 Ficha — Identificação, contratada e origem", "r03", "T03.01")
def t0301():
    c = C("012/2025")
    oi = origem("Integrado", "Conector PNCP", "05/12/2025 03:00", "Sincronização PNCP · contrato nº 2025.0012 · execução 2025-12-05-0300")
    od = origem("Digitado", "R. Costa", "01/12/2025 10:14")
    om = origem("Importado", "Lote L01 de 03/11/2026 (R. Costa)", "03/11/2026 14:02", "Lote L01 · planilha de comissões · aba Contratos · célula F14",
                "Planilha legada de acompanhamento (arquivo de 2026)")
    body = [
        section("Identificação", kv([("Número e ano", "012/2025 · 2025", od), ("Forma normalizada (busca)", "12/2025"), ("Natureza do instrumento", "Termo de contrato"),
                                     ("Tipo e modelo de preço", "Serviço contínuo · Mensal fixo"), ("Enquadramento no art. 2º da Lei nº 14.133/2021", "Inciso V — prestação de serviços"),
                                     ("Objeto resumido", c["obj"], od), ("Unidade responsável", "GERAD"), ("Categoria · grupo", "Serviços prediais · Manutenção"),
                                     ("Criticidade do objeto", "Essencial (desempate da C17)"),
                                     ("Situação (três indicações)", cat(div("Vigência: Em vigor"), div("Execução: Em execução"), div("Fechamento: Aberto")))]),
                kv([("Objeto completo (texto do instrumento)", "Prestação de serviços continuados de manutenção predial preventiva e corretiva, com fornecimento de materiais, "
                     "nas sedes do Rioprevidência, conforme o Termo de Referência.")], min_=600), h=3),
        section("Contratada", kv([("Razão social", c["ctda"]), ("CNPJ", cat(div(c["cnpj"]), small("dígitos verificadores conferidos; aceita o formato alfanumérico")), oi)]),
                table(["Nome", "Papel", "E-mail", "Telefone", "Período"],
                      [["R. Albuquerque", "Representante legal", "representante@alfa.exemplo", "(21) 0000-0001", "desde 28/11/2025"],
                       ["D. Farias", "Preposto", "preposto@alfa.exemplo", "(21) 0000-0002", "desde 29/11/2025"]],
                      caption="Representante, preposto e contatos (visíveis conforme o perfil)", dense=True), h=3),
        section("Origem e regime jurídico", kv([("Modalidade", "Pregão eletrônico", oi), ("Procedimento de origem", "Pregão eletrônico nº 014/2025"), ("Ata de registro de preços", "Não aplicável"),
                                                ("Regime jurídico", "Lei nº 14.133/2021"), ("Prazo de divulgação no PNCP", cat(div("20 dias úteis"), prazo_nat("Legal")))]), h=3),
        section("Mão de obra e condicionantes", kv([("Dedicação exclusiva de mão de obra", "Sim", om), ("Predominância de mão de obra", "Sim"), ("Conta vinculada", "Sim"),
                                                    ("Previsão de prorrogação no edital", "Sim"), ("Sistema estruturante de TI", "Não")]),
                small("Habilitam repactuação, fiscal administrativo e conferência trabalhista mensal; condicionam os tetos de vigência e a decisão “prorrogar”."), h=3),
        section("Prazos contratuais (base da C22)", kv([("Liquidação", cat(div("10 dias"), prazo_nat("Contrato"))), ("Pagamento", cat(div("30 dias"), prazo_nat("Contrato"))),
                                                        ("Recebimento provisório", cat(div("15 dias"), prazo_nat("Contrato"))), ("Recebimento definitivo", cat(div("30 dias"), prazo_nat("Contrato")))]),
                small("Lidos da cláusula 7ª do contrato, sem valor padrão."), h=3),
    ]
    return ficha("T03.01 Identificação", "T03.01", body, "Identificação, contratada e origem", DOCS_CT + [("Edital do pregão eletrônico nº 014/2025", "SEI-040014/000301/2025 · conferido")],
                 "Identificação digitada; contratada e modalidade integradas do PNCP; mão de obra importada do legado e validada.", "T04-P1-Identificacao.dc.html")


@screen("T0302-Prazos.dc.html", "T03.02 Ficha — Prazos e continuidade", "r03", "T03.02")
def t0302():
    c = C("012/2025")
    body = [
        section("Vigência formalizada", kv([("Assinatura", "28/11/2025"), ("Publicação do extrato", "02/12/2025 (DOERJ)"), ("Divulgação no PNCP", "05/12/2025 · nº de controle 2025.0012"),
                                            ("Início da vigência", "29/11/2025"), ("Término da vigência", "28/11/2026"), ("Prazo de execução", "12 meses"),
                                            ("Instrumento-fonte das datas", "Contrato 012/2025"), ("Dias restantes (C01)", "18")]),
                row(nat("Formalizado"), badge("Divulgado no PNCP", "green"), small("Só instrumento assinado e validado define estas datas."), gap=8), h=3),
        section("Em tramitação", kv([("Procedimento", a("PRC-2026-014 · Prorrogação", "T06-D1-Resumo.dc.html")), ("Etapa", "4 Análise jurídica (desde 05/11/2026)"),
                                     ("Minuta", "2º Termo aditivo — prorrogação por 12 meses"), ("Término pretendido", "28/11/2027")]),
                alert("warn", "Em tramitação nunca substitui as datas formalizadas", "Os avisos continuam calculados sobre 28/11/2026 até a formalização em T04.01 (CV02)."), h=3),
        section("Decisão e providências", kv([("Decisão prevista", "Prorrogar · registrada em 02/06/2026 · validada por M. Silva"),
                                              ("Data interna de início das providências (C15)", cat(div("31/07/2026"), prazo_nat("Parâmetro interno"))),
                                              ("Situação da C15", "Em andamento (procedimento aberto em 15/07/2026)"), ("Responsável", "P. Nunes")]),
                small("Fixação manual da data interna exige justificativa e respeita o piso de 120 dias (Decreto RJ nº 48.817/2023, art. 22, XVII)."), h=3),
        section("Marcos regulamentares (C19)",
                table(["Marco", "Data-limite", "Registro", "Situação", "Natureza e dispositivo"],
                      [["M120 — recomendação do gestor", "31/07/2026", "31/07/2026 · doc. 46610021", marco("Cumprido"), cat(prazo_nat("Legal regulamentar"), small(" art. 22, XVII"))],
                       ["M30 — envio à assessoria jurídica", "29/10/2026", "05/11/2026 · doc. 47720415", marco("Cumprido com atraso"), cat(prazo_nat("Legal regulamentar"), small(" art. 22, XIX"))]],
                      dense=True), h=3),
        section("Continuidade", kv([("Contratação substituta", "Não aplicável (decisão prorrogar)"), ("Início estimado / formalizado", "—"),
                                    ("Lacuna (C02)", "Não aplicável"), ("Risco (C18)", cat(risco("Alto"), small(" ordem 7: 18 dias, etapa anterior a “autorização”")))]), h=3),
        section("Linha do tempo (somente leitura)",
                table(["Versão ou evento", "Efeitos", "Registro", "Instrumento"],
                      [["V1 — vigência 29/11/2025 a 28/11/2026", "29/11/2025", "01/12/2025", "Contrato 012/2025"],
                       ["V2 — acréscimo de posto (sem alteração de prazo)", "01/04/2026", "02/04/2026", "1º Termo aditivo"],
                       ["Decisão prevista: prorrogar", "02/06/2026", "02/06/2026", "—"],
                       ["Procedimento de prorrogação aberto", "15/07/2026", "15/07/2026", "PRC-2026-014"]], dense=True), h=3),
    ]
    return ficha("T03.02 Prazos", "T03.02", body, "Prazos e continuidade", DOCS_CT + [("Extrato publicado no DOERJ (02/12/2025)", "doc. 41188410 · conferido")],
                 "Datas integradas do PNCP e conferidas com o instrumento assinado.", "T04-P6-Prazos.dc.html")


@screen("T03-Historico.dc.html", "T03 Ficha — Situação em uma data (CH01)", "r03", "T03")
def t03hist():
    body = [
        alert("info", "Situação reconstruída em 15/03/2026", "Vigência, preço, valor e designações aplicáveis na data; nada é sobrescrito na posição corrente."),
        section("Vigência e valor aplicáveis", kv([("Vigência", "29/11/2025 a 28/11/2026"), ("Versão contratual aplicável", "V1 (contrato original)"),
                                                   ("Valor atualizado (vigência corrente)", "R$ 1.020.000,00"), ("Valor mensal vigente", "R$ 85.000,00"),
                                                   ("Itens de preço", "4 itens (sem o posto noturno incluído pelo 1º TA em 01/04/2026)")]), h=3),
        section("Designações aplicáveis",
                table(["Papel", "Pessoa", "Período", "Observação"],
                      [["Gestor titular", "P. Nunes", "29/11/2025 – atual", "—"],
                       ["Fiscal técnico titular", "H. Rocha", "29/11/2025 – 30/04/2026", "Substituído por J. Prado em 01/05/2026 (CH02)"],
                       ["Fiscal administrativo titular", "F. Dias", "29/11/2025 – atual", badge("Registro retroativo: lançado em 20/04/2026", "yellow")]], dense=True), h=3),
        alert("warn", "Registros retroativos evidenciados", "A designação de F. Dias foi registrada em 20/04/2026 com início em 29/11/2025; aparece destacada nesta consulta."),
    ]
    return ficha("T03.02 Prazos", "T03 (consulta histórica)", body, "Prazos, valores e designações em 15/03/2026", DOCS_CT[:1],
                 "Reconstrução a partir das versões contratuais e do histórico de designações.", None, hist=True)


@screen("T0303-Valores.dc.html", "T03.03 Ficha — Valores e composição", "r03", "T03.03")
def t0303():
    itens = [["1", "Posto", "Mão de obra", "Encarregado de manutenção", "posto", "1", "9.800,00", "9.800,00", "117.600,00", "—"],
             ["2", "Posto", "Mão de obra", "Oficial de manutenção", "posto", "4", "8.500,00", "34.000,00", "408.000,00", "—"],
             ["3", "Posto", "Mão de obra", "Auxiliar de manutenção", "posto", "3", "5.500,00", "16.500,00", "198.000,00", "—"],
             ["4", "Posto", "Mão de obra", "Auxiliar noturno (1º TA, desde 01/04/2026)", "posto", "1", "6.800,00", "6.800,00", "54.400,00", "—"],
             ["5", "Item", "Insumo", "Materiais de reposição", "mês", "1", "24.700,00", "24.700,00", "296.400,00", "—"]]
    body = [
        section("Valores formalizados", row(nat("Formalizado"), gap=6),
                kv([("Valor original", "R$ 1.020.000,00"), ("Valor atualizado — vigência corrente", "R$ 1.074.400,00"), ("Valor atualizado — global acumulado", "R$ 1.074.400,00"),
                    ("Valor atualizado — base do art. 125", "R$ 1.020.000,00"), ("Valor mensal vigente", "R$ 91.800,00"), ("Periodicidade", "Mensal")]),
                small("Escopos da C03 não se misturam; o valor resulta da última versão formal válida e coincide com o original mais as variações formais únicas."), h=3),
        section("Itens de preço", table(["Nº", "Tipo", "Componente", "Descrição", "Unidade", ("Qtd.", "r"), ("Preço unitário", "r"), ("Valor mensal", "r"), ("Valor total", "r"), "Etapa prevista"],
                                        itens, foot=["", "", "", "Total", "", "", "", "91.800,00", "1.074.400,00", ""], minw=1000, dense=True),
                alert("ok", "Composição reconciliada com o valor da versão V2", "Total dos itens = R$ 1.074.400,00 = valor da vigência corrente. Divergência impediria a validação."), h=3),
        section("Execução e saldo contratual (C04)", row(nat("Execução registrada"), gap=6),
                kv([("Execução registrada (obrigações validadas, líquidas de glosas)", "R$ 984.866,67"), ("Saldo contratual (vigência corrente)", "R$ 89.533,33"),
                    ("Custo previsto até o término (11/2026, 28 dias)", "R$ 85.680,00")]),
                composicao(("Obrigações 11/2025 a 03/2026", "345.666,67"), ("Obrigações 04/2026 a 10/2026", "642.600,00"), ("Glosas", "−3.400,00"), ("Estornos", "0,00"),
                           formula="C04", cobertura="11 competências validadas"),
                a("Abrir obrigações (T09.A)", "Pagamentos.dc.html"), h=3),
        section("Premissas e cenários", row(nat("Projeção"), nat("Cenário simulado"), gap=6),
                kv([("Projeção operacional vigente", "v3 · cronograma mensal · horizonte até 28/11/2026 · autor L. Martins"),
                    ("Cenário", "Prorrogação por 12 meses com reajuste estimado de 4,8% (não altera valores formalizados)")]),
                a("Abrir valores e planejamento (T07)", "T07A-Formalizado.dc.html"), h=3),
    ]
    return ficha("T03.03 Valores", "T03.03", body, "Valores e composição", DOCS_CT + [("Planilha de composição de custos (V2)", "doc. 43551901 · conferido")],
                 "Valores e itens digitados a partir do instrumento; execução calculada (C04).", "T04-P7-Composicao.dc.html")


@screen("T0304-Empenhos.dc.html", "T03.04 Ficha — Empenhos", "r03", "T03.04")
def t0304():
    body = [
        section("Exercício 2026 · conjunto 3.3.90.37 · fonte 100 · PT 09.122.0002.2031",
                table(["Nota", "Tipo", "Movimentos", ("Valor atualizado", "r"), ("Liquidado", "r"), ("Saldo", "r")],
                      [[a("2026NE00012", "T08B-Notas.dc.html"), "Estimativo", "Inicial 700.000,00 · reforço 2026NE00140 +300.000,00 · anulação 2026NE00188 −20.000,00",
                        "980.000,00", "802.400,00", "177.600,00"]], dense=True),
                grid(*[stat(k, v, s) for k, v, s in [("E — empenho atualizado", "980.000,00", "C05"), ("L — liquidado", "802.400,00", ""),
                                                      ("S — saldo a liquidar", "177.600,00", "C06"), ("O — executado não liquidado", "91.800,00", "C07 · 10/2026"),
                                                      ("D — disponível", "85.800,00", "C08"), ("F — execução futura prevista", "85.680,00", "C13 · até 28/11/2026"),
                                                      ("R — reforço estimado", "0,00", "C09")]], min_=150, gap=10),
                small("Data de insuficiência (C10): sem insuficiência no horizonte (até 28/11/2026) · Meses de cobertura (C16): 1,0"),
                memoria(("E = 700.000,00 + 300.000,00 − 20.000,00", "980.000,00"), ("S = E − L", "177.600,00"), ("D = S − O", "85.800,00"), ("R = máx(0, F − D)", "0,00"),
                        formula="C05–C10 · eventos deduplicados pelo identificador oficial"),
                alert("info", None, "Os totais são os mesmos de T08 na mesma data de posição."), h=3),
        section("Solicitações de reforço", table(["Solicitação", ("Valor", "r"), "Data necessária", "Situação", "Movimento de atendimento"],
                                                 [["REF-2026-007", "300.000,00", "15/05/2026", estado("Atendida", "green"), "2026NE00140 (conciliado)"]], dense=True), h=3),
        section("Restos a pagar (bloco próprio)", table(["Nota", "Exercício", "Tipo", ("Inscrito", "r"), ("Saldo", "r"), "Obrigações vinculadas"],
                                                        [["2025NE00480", "2025", "Processado", "90.666,67", "0,00", "11/2025 e 12/2025"]], dense=True),
                small("O saldo de restos a pagar não compensa o exercício corrente."), h=3),
    ]
    return ficha("T03.04 Empenhos", "T03.04", body, "Empenhos", [("Nota de empenho 2026NE00012", "sistema financeiro oficial · importada (L04) e validada"),
                                                                 ("Reforço 2026NE00140", "importado (L04) e validado")],
                 "Notas e movimentos importados do relatório do sistema financeiro (L04) e validados por L. Martins.", "Empenhos.dc.html",
                 edit_txt="Abrir T08 filtrada no contrato", validacao="Validado em 05/11/2026 por L. Martins (financeiro)")


@screen("T0305-Pagamentos.dc.html", "T03.05 Ficha — Documentos fiscais e pagamentos", "r03", "T03.05")
def t0305():
    body = [
        grid(stat("Executado não liquidado", "91.800,00", "10/2026 — atesto incompleto"), stat("Liquidado a pagar", "0,00", "C11"),
             stat("Pago (2026)", "802.400,00", "baixas brutas"), stat("Com impedimento", "1 documento", "atesto incompleto (C21)", "orange"), min_=200),
        section("Competências, documentos e pagamentos",
                table(["Competência", ("Obrigação (bruto)", "r"), ("Glosa", "r"), "Documento fiscal", "Atesto (C21)", ("Liquidado", "r"), ("Baixa bruta", "r"), "Situação"],
                      [["10/2026", "91.800,00", "0,00", "NFS-e 1187 (03/11/2026)", cat(badge("Insuficiente", "orange"), small(" 1 de 2 fiscais")), "0,00", "0,00", "Impedimento: atesto incompleto"],
                       ["09/2026", "91.800,00", "0,00", "NFS-e 1152 (02/10/2026)", badge("Suficiente", "green"), "91.800,00", "91.800,00", "Pago em 30/10/2026"],
                       ["08/2026", "91.800,00", "0,00", "NFS-e 1120 (02/09/2026)", badge("Suficiente", "green"), "91.800,00", "91.800,00", "Pago em 30/09/2026"],
                       ["07/2026", "91.800,00", "3.400,00", "NFS-e 1093 (04/08/2026)", badge("Suficiente", "green"), "88.400,00", "88.400,00", "Pago em 31/08/2026"]],
                      minw=980, dense=True), h=3),
        alert("info", None, "Contrato encerrado com pendência permanece nesta aba e no RPT07."),
    ]
    return ficha("T03.05 Fiscais e pagamentos", "T03.05", body, "Documentos fiscais e pagamentos",
                 [("NFS-e 1187 — competência 10/2026", "importada por XML (L06) · aguardando 2º atesto")],
                 "Documentos importados por XML (L06); liquidações e pagamentos do sistema financeiro (L05).", "Pagamentos.dc.html",
                 edit_txt="Abrir T09 filtrada no contrato", validacao="Validado em 05/11/2026 por L. Martins")


@screen("T0306-Alteracoes.dc.html", "T03.06 Ficha — Alterações e reajustes", "r03", "T03.06")
def t0306():
    body = [
        section("Formalizadas (somente leitura)", row(nat("Formalizado"), gap=6),
                table(["Classe", "Instrumento", "Processo", "Justificativa", "Assinatura", ("Valor anterior", "r"), ("Variação", "r"), ("Valor resultante", "r"), "Término anterior → novo", "Início dos efeitos"],
                      [["Acréscimo", a("1º Termo aditivo", "T0401-Formalizacao.dc.html"), "SEI-040014/000418/2025", "Inclusão de posto noturno de auxiliar", "31/03/2026",
                        "1.020.000,00", "+54.400,00", "1.074.400,00", "28/11/2026 → 28/11/2026", "01/04/2026"]], minw=1100, dense=True),
                small("Eventos sucessivos não repetem valor já incorporado (CH03)."), h=3),
        section("Propostas e simulações (fora dos valores oficiais)", row(nat("Cenário simulado"), badge("Em análise", "blue"), gap=6),
                table(["Item", "Natureza", "Situação", ""],
                      [["2º Termo aditivo — prorrogação por 12 meses (minuta)", "Proposta", "Em análise — PRC-2026-014, etapa 4", a("Abrir procedimento", "T06-D1-Resumo.dc.html")],
                       ["Prorrogação com reajuste estimado de 4,8%", "Cenário simulado", "Rótulo próprio em tela e exportação", a("Abrir cenário (T07.D)", "T07D-Cenarios.dc.html")]], dense=True), h=3),
        section("Reajuste e repactuação", kv([("Índice e cláusula", "IPCA · cláusula 9ª (insumos)"), ("Data-base (data do orçamento estimado)", "08/2025"),
                                              ("Último reajuste", "Nenhum"), ("Próxima referência prevista — insumos", "08/2026 (pedido não protocolado)"),
                                              ("Repactuação — data-base de mão de obra", "01/01/2026 (CCT 2026)"), ("Próxima referência — mão de obra", "01/01/2027 (CCT 2027)")]),
                small("A próxima referência é derivada e muda com a formalização."), a("Abrir datas-base (T10.B)", "T10B-DatasBase.dc.html"), h=3),
        section("Limites do art. 125", kv([("Acréscimos acumulados", "R$ 54.400,00 · 5,33% de 25%"), ("Supressões acumuladas", "R$ 0,00 · 0,00% de 25%"),
                                           ("Limite restante para acréscimos", "R$ 200.600,00 (19,67%)")]),
                div(div(style=f"width:21%;height:10px;background:{ACC};border-radius:3px;"), style=f"height:10px;background:{RAISED};border-radius:3px;", aria_hidden="true"),
                small("Alerta fundamentado antes da formalização acima do limite."), h=3),
    ]
    return ficha("T03.06 Alterações", "T03.06", body, "Alterações e reajustes", DOCS_CT[1:],
                 "Alterações registradas em T04.01 a partir do instrumento assinado.", "T0401-Formalizacao.dc.html", edit_txt="Formalizar evento (T04.01)")


@screen("T0307-Garantias.dc.html", "T03.07 Ficha — Garantias e seguros", "r03", "T03.07")
def t0307():
    body = [
        section("Garantia contratual", kv([("Aplicável", "Sim"), ("Modalidade", "Seguro-garantia"), ("Instituição e número", "Seguradora Exemplo S.A. · apólice 0775.12.2025.0001234"),
                                           ("Valor e percentual", "R$ 51.000,00 · 5,00% (até 5%, ou até 10% com justificativa — arts. 96 a 99)"),
                                           ("Validade", "29/11/2025 a 30/12/2026"), ("Cobertura de verbas trabalhistas", "Sim (dedicação exclusiva de mão de obra)"),
                                           ("Documento e comprovante de recolhimento", a("Apólice e boleto quitado", "T0309-Documentos.dc.html")),
                                           ("Situação", "Vigente"), ("Necessidade de atualização", "Sim — 1º TA elevou o valor (aviso N09)"),
                                           ("Proposta de liberação · liberação", "— · —")]),
                alert("warn", "Endosso pendente", "Após o 1º termo aditivo, 5% do valor atualizado = R$ 53.720,00; complementação de R$ 2.720,00 solicitada à contratada. "
                      "Aviso N08 programado para 15/11/2026 (45 dias antes da validade — parâmetro interno)."),
                small("Em seguro-garantia, validade inferior à vigência gera alerta (art. 97). “Não aplicável” exige justificativa; vazio é pendência de avaliação, nunca dispensa."), h=3),
        section("Histórico (somente inserção)", table(["Evento", "Data", "Documento", "Registrado por"],
                                                      [["Emissão", "25/11/2025", "Apólice 0775.12.2025.0001234", "R. Costa"],
                                                       ["Endosso solicitado (complementação)", "06/04/2026", "Ofício GERAD nº 041/2026", "J. Prado"]], dense=True), h=3),
    ]
    return ficha("T03.07 Garantias", "T03.07", body, "Garantias e seguros", [("Apólice 0775.12.2025.0001234", "doc. 41029401 · conferido"), ("Ofício de solicitação de endosso", "doc. 43610077 · conferido")],
                 "Dados da apólice digitados a partir do documento.", "T04-P7-Composicao.dc.html")


@screen("T0308-Responsaveis.dc.html", "T03.08 Ficha — Responsáveis e designações", "r03", "T03.08")
def t0308():
    body = [
        section("Quadro atual", table(["Papel", "Titularidade", "Pessoa", "Início", "Ato", "Termo de Ciência"],
                                      [["Gestor", "Titular", "P. Nunes", "29/11/2025", "PORT GERAD nº 112/2025", "27/11/2025"],
                                       ["Fiscal técnico", "Titular", "J. Prado", "01/05/2026", "PORT GERAD nº 058/2026", "30/04/2026"],
                                       ["Fiscal administrativo", "Titular", "F. Dias", "29/11/2025", "PORT GERAD nº 112/2025", span("Ausente", style="color:#FFC489;font-weight:600;")]], dense=True),
                small("Consulta em data passada mostra a designação do período (CH01, CH02)."), h=3),
        section("Conformidade (C20) — indicadores, não bloqueios",
                table(["Apontamento", "Resultado", ""],
                      [["Gestor e fiscal titulares", desig("Completa"), ""],
                       ["Suplentes exigidos × existentes", span("2 exigidos (1 de gestor + 1 para cada 2 fiscais) · 0 existentes", style="color:#FFC489;"), a("Gerar providência (designação)", "T11B-Todas.dc.html")],
                       ["Ato sem publicação e sem dispensa justificada", "Não há", ""],
                       ["Termo de Ciência ausente ou posterior ao ato", span("1 ausente (F. Dias)", style="color:#FFC489;"), a("Gerar providência (designação)", "T11B-Todas.dc.html")],
                       ["Comissão com menos de 3 titulares", "Não se aplica", ""],
                       ["Comissionado exclusivo sem justificativa", span("1 (F. Dias)", style="color:#FFC489;"), a("Gerar providência (designação)", "T11B-Todas.dc.html")],
                       ["Mesma pessoa como gestor e fiscal", "Não há", ""]], dense=True),
                small("Critério de suplentes a validar pela assessoria jurídica (seção 4.4)."), h=3),
        section("Ato de designação", kv([("Número e data", "PORT GERAD nº 112/2025 · 28/11/2025"), ("Autoridade", "Diretoria Administrativo-Financeira"),
                                         ("Publicação no Diário Oficial", "01/12/2025"), ("Comissão · dedicação exclusiva", "Não · Não"),
                                         ("Processo e documento", "SEI-040014/000611/2025 · doc. 41100230"), ("Contratos abrangidos", "012/2025 e 060/2024")]),
                small("Publicação não anterior ao ato; um ato pode abranger vários contratos."), h=3),
        section("Designação selecionada — F. Dias",
                kv([("Nome · cargo · vínculo", "F. Dias · Assessor · ocupante exclusivo de cargo em comissão"),
                    ("ID funcional", cat(span("******56"), btn("Mostrar (registra acesso)", small_=True))),
                    ("Papel · titularidade", "Fiscal administrativo · titular"), ("Início · fim · motivo", "29/11/2025 · — · —"),
                    ("Termo de Ciência (data e documento)", span("Não informado", style="color:#FFC489;")), ("Declaração de ausência de impedimento", "Assinada em 27/11/2025"),
                    ("Justificativa para comissionado exclusivo", span("Não informada", style="color:#FFC489;"))]),
                small("A mesma pessoa não ocupa o mesmo papel em períodos sobrepostos (CD04); encerrar exige motivo. Identificador mascarado por padrão (CP05)."), h=3),
        section("Afastamentos", table(["Pessoa", "Período", "Motivo", "Comunicação", "Suplente que assume", "Ciência do suplente"],
                                      [["J. Prado", "04/01/2027 – 23/01/2027", "Férias", "05/11/2026", span("Sem suplente", style="color:#FFC489;"), "—"]], dense=True),
                small("Afastamento sem suplente em exercício gera o aviso N14 no início do afastamento."), h=3),
        section("Histórico (somente leitura)", table(["Papel", "Pessoa", "Período", "Motivo do encerramento"],
                                                     [["Fiscal técnico titular", "H. Rocha", "29/11/2025 – 30/04/2026", "Remoção para outra unidade"]], dense=True), h=3),
    ]
    return ficha("T03.08 Responsáveis", "T03.08", body, "Responsáveis e designações", [("PORT GERAD nº 112/2025", "DOERJ 01/12/2025 · conferido"), ("PORT GERAD nº 058/2026", "DOERJ 04/05/2026 · conferido")],
                 "Designações importadas da planilha de comissões (L03) e conferidas; afastamento digitado.", "T04-P5-Responsaveis.dc.html")


@screen("T0309-Documentos.dc.html", "T03.09 Ficha — Documentos e processos", "r03", "T03.09")
def t0309():
    body = [
        section("Processos", table(["Número SEI", "Papel", "Tipo e assunto", "Unidade atual", "Conferência"],
                                   [[a("SEI-040014/000418/2025", "T0309-Documentos.dc.html"), "Principal", "Contratação — manutenção predial", "GERAD", "10/11/2026 (conector SEI)"],
                                    [a("SEI-040014/000611/2025", "T0309-Documentos.dc.html"), "Gestão e fiscalização", "Gestão e fiscalização do contrato 012/2025", "GERAD", "10/11/2026"],
                                    [a("SEI-040014/000512/2026", "T06-D6-Documentos.dc.html"), "Relacionado", "Prorrogação — 2º termo aditivo", "ASSJUR", "10/11/2026"]], dense=True),
                small("Um principal e um de gestão e fiscalização por contrato."), h=3),
        section("Documentos", table(["Tipo", "Número", "Data", "Versão", "Arquivo ou link", "Restrição", "Conferência", "Vínculos"],
                                    [["Contrato", "012/2025", "28/11/2025", "1", "doc. 41029337", "Pública", badge("Conferido", "green"), "V1"],
                                     ["Termo aditivo", "1º TA", "31/03/2026", "1", "doc. 43551820", "Pública", badge("Conferido", "green"), "V2"],
                                     ["Apólice de seguro-garantia", "0775.12.2025.0001234", "25/11/2025", "1", "doc. 41029401", "Restrita", badge("Conferido", "green"), "Garantia"],
                                     ["Endosso da apólice", "—", "—", "—", span("Arquivo indisponível", style="color:#FFC489;"), "Restrita", badge("Pendente", "yellow"), "Garantia"],
                                     ["Relatório mensal de fiscalização", "10/2026", "—", "—", span("Arquivo indisponível", style="color:#FFC489;"), "Interna", badge("Pendente", "yellow"), "Obrigação 10/2026"]],
                                    minw=1000, dense=True),
                small("Arquivo indisponível é pendência, nunca documento conferido; versões anteriores preservadas; endereço direto sem permissão é negado."), h=3),
        section("Instrumentos de gestão (art. 19 do Decreto RJ nº 48.817/2023)",
                table(["Instrumento aplicável", "Situação"],
                      [["Termo de referência com o modelo de gestão", badge("Presente", "green")], ["Matriz de riscos", badge("Presente", "green")],
                       ["Plano de fiscalização", badge("Presente", "green")], ["Formulários de acompanhamento (IN AGE nº 54/2025) — 09/2026 e 10/2026", badge("Faltante", "orange")]], dense=True),
                small("Lista configurável em T14.02; faltante gera pendência de documento."), h=3),
    ]
    return ficha("T03.09 Documentos", "T03.09", body, "Documentos e processos", DOCS_CT, "Processos conferidos por consulta ao SEI (conector), com a data da consulta.",
                 "T04-P4-Processos.dc.html")


@screen("T0310-Historico.dc.html", "T03.10 Ficha — Providências e histórico", "r03", "T03.10")
def t0310():
    body = [
        section("Providências pendentes do contrato", table(["Prioridade", "Providência", "Responsável", "Prazo", "Situação"],
                                                            [[prio("Alta"), a("Obter parecer jurídico e autorização da prorrogação", "T11B-Todas.dc.html"), "P. Nunes", "20/11/2026", estado("Em andamento")],
                                                             [prio("Alta"), a("Solicitar endosso do seguro-garantia", "T11B-Todas.dc.html"), "J. Prado", "24/11/2026", estado("Aguardando terceiro")],
                                                             [prio("Média"), a("Designar suplentes e colher Termo de Ciência", "T11B-Todas.dc.html"), "M. Silva", "30/11/2026", estado("Aberta")]], dense=True),
                act=actions(btn("Nova providência", href="T11B-Todas.dc.html", small_=True, ico="plus"), btn("Abrir T11", href="T11B-Todas.dc.html", small_=True)), h=3),
        section("Linha do tempo unificada (somente leitura)",
                table(["Instante (Brasília)", "Tipo", "Evento", "Autor", "Antes → depois"],
                      [["05/11/2026 16:20", badge("Negócio", "blue"), "Remessa do PRC-2026-014 à ASSJUR (marco M30 registrado)", "P. Nunes", "—"],
                       ["03/11/2026 09:12", badge("Negócio", "blue"), "Atesto da NFS-e 1187 por J. Prado (fiscal técnico)", "J. Prado", "—"],
                       ["31/07/2026 15:02", badge("Negócio", "blue"), "Recomendação do gestor à autoridade (M120)", "P. Nunes", "—"],
                       ["20/04/2026 11:40", badge("Auditoria", "purple"), "Correção: início da designação de F. Dias", "R. Costa", "01/12/2025 → 29/11/2025 · motivo: conferência do ato"],
                       ["02/04/2026 10:05", badge("Negócio", "blue"), "Formalização do 1º termo aditivo (versão V2)", "M. Silva", "1.020.000,00 → 1.074.400,00"]], minw=900, dense=True),
                small("Correção cria novo registro; o histórico não é alterado."), a("Abrir trilha completa (T14.05)", "T1405-Trilha.dc.html"), h=3),
    ]
    return ficha("T03.10 Providências e histórico", "T03.10", body, "Providências e histórico", DOCS_CT[:1], "Eventos de negócio e de auditoria (aud.evento).", "T11B-Todas.dc.html",
                 edit_txt="Abrir T11 filtrada no contrato")


@screen("T0311-Conformidade.dc.html", "T03.11 Ficha — Conformidade da gestão e fiscalização", "r03", "T03.11")
def t0311():
    itens = [
        ("Gestor, fiscais e suplentes designados", "Arts. 4º, 5º e 8º, III", "C20", "Completa (titulares); faltam 2 suplentes", "orange", "T0308-Responsaveis.dc.html"),
        ("Ato publicado e Termo de Ciência anterior ao ato", "Art. 7º, caput e § 1º", "C20", "Ato: atende · Termo de Ciência: não atende (1 ausente)", "orange", "T0308-Responsaveis.dc.html"),
        ("Processo de gestão e fiscalização relacionado ao principal", "Art. 22, I e III", "T03.09", "Informado", "green", "T0309-Documentos.dc.html"),
        ("Instrumentos mínimos no processo", "Art. 22, I, e art. 19", "T03.09", "3 presentes · 1 faltante", "orange", "T0309-Documentos.dc.html"),
        ("Publicação do extrato e divulgação no PNCP", "Art. 22, II; Lei nº 14.133/2021, art. 94", "T03.02", "Extrato 02/12/2025 · PNCP 05/12/2025", "green", "T0302-Prazos.dc.html"),
        ("Recomendação com 120 dias e envio jurídico com 30 dias", "Art. 22, XVII e XIX", "C19", "M120 cumprido · M30 cumprido com atraso", "yellow", "T05D-Marcos.dc.html"),
        ("Lista de verificação da prorrogação", "Art. 22, § 1º", "T06", "10 atendidos · 2 pendentes", "orange", "T06-D3-Checklist.dc.html"),
        ("Atesto por dois fiscais", "Art. 22, XXIII e § 2º", "C21", "3 documentos suficientes · 1 insuficiente", "orange", "T09B-DocFiscais.dc.html"),
        ("Conferência trabalhista mensal", "Art. 28, § 3º", "T09.A", "11 competências com registro · 1 sem (10/2026)", "orange", "Pagamentos.dc.html"),
        ("Controle e liberação da garantia", "Art. 22, XI e XII", "T03.07", "Vigente · endosso pendente", "yellow", "T0307-Garantias.dc.html"),
        ("Formulários de acompanhamento", "IN AGE nº 54/2025, art. 4º, § 1º", "T03.09", "Não informado (09/2026 e 10/2026)", "gray", "T0309-Documentos.dc.html"),
        ("Relatório final do gestor", "Art. 23", "T03.09", "Não aplicável (contrato em curso)", "gray", "T0309-Documentos.dc.html"),
    ]
    rows = [[t_, small(f), a(fonte, href), badge(res, tone, dashed=(tone == "gray")), a("Criar providência", "T11B-Todas.dc.html")] for t_, f, fonte, res, tone, href in itens]
    body = [
        alert("info", "O que os registros mostram e o que falta", "“Não informado” não equivale a descumprimento; o sistema não emite juízo de conformidade (CD06). "
              "Fundamentos do Decreto RJ nº 48.817/2023, salvo indicação."),
        section("Itens verificados", table(["Item verificado", "Fundamento", "Fonte no sistema", "Resultado exibido", "Ação"], rows, minw=980, dense=True),
                act=btn("Emitir RPT15 do contrato", href="T1301-Previa.dc.html", small_=True, kind="primary"), h=3),
    ]
    return ficha("T03.11 Conformidade", "T03.11", body, "Conformidade da gestão e fiscalização", [("PORT GERAD nº 112/2025", "conferido"), ("Lista de verificação PR01–PR12", "PRC-2026-014")],
                 "Visões das regras C19, C20 e C21 e tabelas de processos, documentos, garantias e instrumentos.", None, validacao="Calculado na posição 10/11/2026")
