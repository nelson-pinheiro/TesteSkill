"""T07 Valores e planejamento (A–D), T08 Empenhos e reforços (A–D) e T08.01 Movimentação financeira (5 variantes)."""
from shell import *
from s_inicio import ctr_cell


def seletor_contrato(n="060/2024 — Sigma Climatização Ltda"):
    return row(field("Contrato", kind="select", options=[n, "012/2025 — Alfa Serviços Prediais Ltda", "044/2023 — Épsilon Elevadores Ltda (medição)",
                                                         "052/2025 — Ômicron Suprimentos Ltda (fornecimento)"], w="420px"),
               small("Valores rotulados por natureza; nada se mistura entre abas."), gap=12, align="flex-end")


def t07page(tab, body, sub):
    return page("T07 Valores e planejamento", "valores", ["Valores e planejamento", tab], [seletor_contrato(), *body], tabs_=tabs(T07_TABS, tab),
                sub=sub, acts=[btn("Previsão orçamentária (RPT09)", href="Relatorios.dc.html", small_=True)])


@screen("T07A-Formalizado.dc.html", "T07.A Valores — Formalizado", "r06", "T07.A")
def t07a():
    return t07page("A Formalizado", [
        section("Valor formalizado", row(nat("Formalizado"), small("Somente leitura — origem em T04.01"), gap=8),
                kv([("Valor original", "R$ 120.000,00"), ("Valor atualizado — vigência corrente (01/06/2026 a 31/05/2027)", "R$ 125.000,00"),
                    ("Valor atualizado — global acumulado", "R$ 365.000,00"), ("Valor atualizado — base do art. 125", "R$ 126.000,00 (valor inicial reajustado)"),
                    ("Valor mensal vigente", "R$ 10.500,00 (desde 01/08/2026)"), ("Acréscimos e supressões acumulados", "0,00% e 0,00%")]),
                alert("ok", "Conferência das duas vias da C03", "Última versão formal (V4) = R$ 125.000,00 = versão V3 (R$ 120.000,00) + apostila nº 1 (+R$ 5.000,00). "
                      "Divergência seria exibida como inconsistência; estados sucessivos nunca são somados (CH03).")),
        section("Versões e instrumentos", table(["Versão", "Instrumento", "Efeitos", ("Valor da vigência", "r"), ("Valor mensal", "r")],
                                                [["V1", "Contrato 060/2024", "01/06/2024", "120.000,00", "10.000,00"],
                                                 ["V2", "1º Termo aditivo — prorrogação", "01/06/2025", "120.000,00", "10.000,00"],
                                                 ["V3", "2º Termo aditivo — prorrogação", "01/06/2026", "120.000,00", "10.000,00"],
                                                 ["V4", "Apostila nº 1 — reajuste IPCA 5,00% (assinada 05/10/2026, efeitos retroativos)", "01/08/2026", "125.000,00", "10.500,00"]], dense=True)),
        section("Composição por item", table(["Item", "Descrição", "Componente", ("Valor mensal", "r")],
                                             [["1", "Manutenção preventiva mensal", "Único", "7.350,00"], ["2", "Manutenção corretiva e peças", "Insumo", "3.150,00"]],
                                             foot=["", "Total", "", "10.500,00"], dense=True)),
    ], "Valores e previsões sem misturar naturezas (Diretriz, item 6). Contrato de exemplo: 060/2024.")


@screen("T07B-Execucao.dc.html", "T07.B Valores — Execução registrada", "r06", "T07.B")
def t07b():
    rows = [["06/2026", "10.000,00", "0,00", "10.000,00", "Validada"], ["07/2026", "10.000,00", "0,00", "10.000,00", "Validada"],
            ["08/2026", "10.500,00", "0,00", "10.500,00", "Validada (inclui complementar retroativa de 500,00)"],
            ["09/2026", "10.500,00", "350,00", "10.150,00", "Validada"], ["10/2026", "10.500,00", "0,00", "10.500,00", "Validada (complementar de 500,00)"]]
    return t07page("B Execução registrada", [
        section("Execução por competência", row(nat("Execução registrada"), gap=6),
                table(["Competência", ("Valor bruto", "r"), ("Glosa", "r"), ("Executado", "r"), "Situação"], rows, foot=["Total", "51.500,00", "350,00", "51.150,00", ""], dense=True),
                a("Abrir obrigações (T09.A)", "Pagamentos.dc.html")),
        grid(div(stat("Executado na vigência corrente", "51.150,00", "C04 · obrigações validadas, líquidas de glosas"),
                 composicao(("Obrigações 06/2026 a 10/2026", "51.500,00"), ("Glosas", "−350,00"), ("Estornos", "0,00"), formula="C04", cobertura="5 de 5 competências validadas")),
             div(stat("Saldo contratual", "73.850,00", "limite 125.000,00 − execução"), composicao(("Limite formal (vigência corrente)", "125.000,00"), ("Execução", "−51.150,00"), formula="C04")),
             div(stat("Custo previsto até o término", "73.500,00", "11/2026 a 05/2027 · Projeção"), composicao(("7 competências × 10.500,00", "73.500,00"), formula="C13", fonte="projeção operacional v5")),
             min_=240),
        small("Liquidações, pagamentos e retenções não geram execução. Saldo negativo seria exibido como inconsistência."),
    ], "Executado por competência ou etapa, glosas, saldo contratual (C04) e custo até o término.")


@screen("T07C-Projecao.dc.html", "T07.C Valores — Projeção", "r06", "T07.C")
def t07c():
    parc = [("11/2026", "10.500,00", "12/2026"), ("12/2026", "10.500,00", "01/2027"), ("01/2027", "10.500,00", "02/2027"), ("02/2027", "10.500,00", "03/2027"),
            ("03/2027", "10.500,00", "04/2027"), ("04/2027", "10.500,00", "05/2027"), ("05/2027", "10.500,00", "06/2027")]
    return t07page("C Projeção", [
        section("Projeção operacional vigente", row(nat("Projeção"), badge("Versão 5 · vigente", "blue"), gap=6),
                kv([("Método", "Preço mensal fixo (valor mensal vigente) — conforme a modalidade"), ("Horizonte", "01/11/2026 a 31/05/2027 (término formalizado)"),
                    ("Premissas", "Reajuste IPCA de 5,00% aplicado desde 08/2026; sem prorrogação em tramitação"), ("Autor e data", "L. Martins · 06/10/2026")]),
                table(["Competência (custo)", ("Valor", "r"), "Desembolso (mês esperado)"], [list(x_) for x_ in parc], foot=["Total", "73.500,00", ""], dense=True),
                kv([("Previsão no exercício 2026 (custo)", "R$ 21.000,00 · desembolso em 2026: R$ 10.500,00"), ("Previsão no exercício 2027 (custo)", "R$ 52.500,00")]),
                actions(btn("Nova versão de projeção (preserva as anteriores)", kind="primary"), btn("Colar parcelas em grade"), btn("Importar cronograma (L09)", href="Importacao.dc.html"))),
        section("Alteração no meio do exercício (CF06)", table(["Consulta", "Valor mensal aplicável"], [["Julho de 2026", "10.000,00"], ["Agosto de 2026", "10.500,00"],
                                                                                                         ["Projeção anual 2026", "7 × 10.000,00 + 5 × 10.500,00 = 122.500,00"]], dense=True), h=3),
        section("Validação do método por modalidade (CF09)",
                alert("danger", "044/2023 (medição): método “mensal × meses” recusado", "Contrato por medição ou etapas usa cronograma, quantidades ou consumo histórico. "
                      "Exemplo aceito: cronograma 500,00 + 1.800,00 = 2.300,00. Meses sem dado aparecem como “não apurado”."), h=3),
        section("Versões anteriores", table(["Versão", "Data", "Autor", "Motivo"], [["4", "22/05/2026", "L. Martins", "Prorrogação (V3)"], ["3", "10/01/2026", "L. Martins", "Exercício 2026"]], dense=True), h=3),
    ], "Projeção operacional vigente: método, horizonte, premissas, versão, autor e parcelas (custo pela competência e desembolso pela data esperada).")


@screen("T07D-Cenarios.dc.html", "T07.D Valores — Cenários simulados", "r06", "T07.D")
def t07d():
    return t07page("D Cenários simulados", [
        alert("sim", "Cenário simulado", "Cenários não alteram valores formalizados nem geram empenho. O rótulo aparece em tela e em toda exportação."),
        section("Cenários do contrato", table(["Cenário", "Premissas", "Horizonte", ("Cenário", "r"), ("Referência (v5)", "r"), ("Impacto (C14)", "r"), "Ações"],
                                              [[cat(strong("A — visita corretiva adicional"), " ", nat("Cenário simulado")), "+R$ 600,00/mês a partir de 12/2026", "11/2026 a 05/2027", "77.100,00", "73.500,00",
                                                strong("+3.600,00"), col(a("Duplicar", "T07D-Cenarios.dc.html"), a("Excluir", "T07D-Cenarios.dc.html"), gap=4, style="font-size:12px;")],
                                               [cat(strong("B — prorrogação com reajuste de 4,5%"), " ", nat("Cenário simulado")), "Nova vigência 06/2027 a 05/2028; IPCA estimado 4,5%", "06/2027 a 05/2028", "131.670,00", "—",
                                                badge("Comparação recusada — horizontes diferentes", "red"), col(a("Duplicar", "T07D-Cenarios.dc.html"), a("Excluir", "T07D-Cenarios.dc.html"), gap=4, style="font-size:12px;")]],
                                              minw=1000, dense=True),
                actions(btn("Criar cenário", kind="primary", ico="plus"), btn("Simular reajuste (T10.01)", href="T1001-Simulacao.dc.html")), tone="sim"),
        section("Impacto por período — cenário A", table(["Período", ("Referência", "r"), ("Cenário", "r"), ("Impacto", "r")],
                                                         [["11/2026", "10.500,00", "10.500,00", "0,00"], ["12/2026 a 05/2027 (6 meses)", "63.000,00", "66.600,00", "+3.600,00"]],
                                                         foot=["Total", "73.500,00", "77.100,00", "+3.600,00"], dense=True),
                small("Mesma posição, horizonte e conjuntos; projeções não comparáveis têm o cálculo recusado (CF10)."), h=3, tone="sim"),
    ], "Cenários de reajuste, prorrogação ou alteração: premissas, comparação com a projeção de referência e impacto por período (C14).")


# ======================================================================= T08
def mem(e, l, o, f):
    s_ = e - l
    d_ = s_ - o
    r_ = max(0, f - d_)
    return memoria((f"E (empenho atualizado)", money(e)), ("L (liquidado)", money(l)), ("S = E − L", money(s_)), ("O (executado não liquidado)", money(o)),
                   ("D = S − O", money(d_)), ("F (execução futura no horizonte)", money(f)), ("R = máx(0, F − D)", money(r_)), formula="C05–C09 · por conjunto orçamentário")


@screen("Empenhos.dc.html", "T08.A Empenhos — Cobertura", "r06", "T08.A")
def t08a():
    def r_(ctr, ctda, conj, e, l, o, f, insuf, meses, flag=None):
        s_, d_ = e - l, e - l - o
        rr = max(0, f - d_)
        dcell = span(money(d_), style="color:#FFB3B8;font-weight:700;") if d_ < 0 else money(d_)
        return [cat(ctr_cell(ctr, ctda), small(conj), div(flag or badge("Cobertura conclusiva", "green"), style="margin-top:4px;")),
                money(e), money(l), money(s_), money(o), dcell, money(f),
                col(strong(money(rr)) if rr else span("0,00"), mem(e, l, o, f), a("Solicitar reforço", "T0801-Reforco.dc.html") if rr else None, gap=4),
                insuf, meses]
    rows = [r_("044/2023", "Épsilon Elevadores Ltda", "2026 · 3.3.90.39 · 100 · PT 2031", 100000, 40000, 20000, 50000, "01/12/2026", "1,6"),
            r_("027/2024", "Gama Vigilância Ltda", "2026 · 3.3.90.37 · 100 · PT 2031", 2420000, 2400000, 30000, 0, badge("Insuficiência existente", "red"), "Insuficiência existente"),
            r_("012/2025", "Alfa Serviços Prediais Ltda", "2026 · 3.3.90.37 · 100 · PT 2031", 980000, 802400, 91800, 85680, "Sem insuficiência no horizonte (até 28/11/2026)", "1,0"),
            r_("060/2024", "Sigma Climatização Ltda", "2026 · 3.3.90.39 · 100 · PT 2031", 130000, 40000, 11600, 21000, "Sem insuficiência no horizonte (até 31/12/2026)", "2,0"),
            r_("019/2025", "Delta Copeiragem Ltda", "2026 · 3.3.90.37 · 100 · PT 2031", 720000, 496000, 62000, 124000, "Indeterminada", "Não apurado",
               flag=cat(badge("Não conclusiva", "orange"), a(" obrigação sem alocação (3.000,00)", "Pagamentos.dc.html")))]
    rows.append([cat(ctr_cell("031/2023", "Beta Tecnologia S.A."), small("2026 · 3.3.90.39 · 100 · PT 2031"),
                     div(cat(badge("Não conclusiva", "orange"), a(" movimento não classificado", "T08B-Notas.dc.html")), style="margin-top:4px;")),
                 badge("Indeterminado", "gray", dashed=True), "1.040.000,00", "Indeterminado", "130.000,00", "Indeterminado", "260.000,00", "Indeterminado", "Indeterminada", "Não apurado"])
    rows.append([cat(ctr_cell("041/2026", "Lambda Software Ltda"), small("2026 · 3.3.90.40 · 100 · PT 2031"), div(badge("Sem nota registrada", "gray", dashed=True), style="margin-top:4px;")),
                 qual("Não apurado"), "—", "—", "—", "—", "—", a("Nova nota (T08.01)", "T0801-NotaEmpenho.dc.html"), "—", "—"])
    return page("T08 Empenhos e reforços", "empenhos", ["Empenhos", "A Cobertura"],
                [filterbar(fsel("Exercício", "2026", "2027"), fsel("Conjunto orçamentário", "Todos", "3.3.90.37", "3.3.90.39"), fsel("Unidade", "Todas", "GERAD", "GERTIC")),
                 alert("info", "Exemplo de aceite (CF03)", "044/2023: E = 100.000; L = 40.000; O = 20.000; F = 50.000 → S = 60.000; D = 40.000; R = 10.000."),
                 listbar(7, 3),
                 table(["Contrato · conjunto orçamentário · cobertura", ("E", "r"), ("L", "r"), ("S", "r"), ("O", "r"), ("D", "r"), ("F", "r"), ("R e memória", "r"),
                        "Data de insuficiência (C10)", "Meses de cobertura (C16)"], rows, dense=True),
                 small("D < 0 caracteriza insuficiência existente; empenho não equivale a disponibilidade de caixa. Restos a pagar em bloco próprio (T08.C), sem compensar o exercício. "
                       "Igualdade entre F acumulado e D não é insuficiência.")],
                tabs_=tabs(T08_TABS, "A Cobertura"), acts=[btn("Solicitar reforço", href="T0801-Reforco.dc.html", kind="primary"), btn("Exportar RPT05", href="Relatorios.dc.html", small_=True)],
                sub="Quanto está empenhado, até quando o saldo cobre a execução e quanto reforçar (Diretriz, item 7).")


@screen("T08B-Notas.dc.html", "T08.B Empenhos — Notas de empenho", "r06", "T08.B")
def t08b():
    hist = details("Histórico de movimentos — 2026NE00090",
                   table(["Data", "Tipo", "Documento oficial", ("Valor", "r"), "Movimento estornado"],
                         [["15/01/2026", "Inicial", "2026NE00090", "100.000,00", "—"], ["10/03/2026", "Anulação", "2026NE00101", "−30.000,00", "—"],
                          ["12/03/2026", "Estorno de anulação", "2026NE00102", "+10.000,00", "2026NE00101"], ["05/05/2026", "Reforço", "2026NE00130", "+50.000,00", "—"],
                          ["07/05/2026", "Estorno de reforço", "2026NE00131", "−20.000,00", "2026NE00130"]], foot=["", "E", "", "110.000,00", ""], dense=True),
                   small("CF14: E = 100 − 30 + 10 + 50 − 20 = 110 (mil). Estorno aponta movimento do mesmo empenho e do tipo correspondente."))
    rows = [["UG 040100", a("2026NE00012", "T0304-Empenhos.dc.html"), "10/01/2026", "Estimativo", "3.3.90.37 · 100 · 2031", "700.000,00", "300.000,00", "20.000,00", "0,00", "980.000,00", "802.400,00", "177.600,00", estado("Validado")],
            ["UG 040100", "2026NE00044", "12/01/2026", "Estimativo", "3.3.90.39 · 100 · 2031", "80.000,00", "20.000,00", "0,00", "0,00", "100.000,00", "40.000,00", "60.000,00", estado("Validado")],
            ["UG 040100", "2026NE00090", "15/01/2026", "Global", "3.3.90.39 · 100 · 2031", "100.000,00", "50.000,00", "30.000,00", "+10.000 / −20.000", "110.000,00", "40.000,00", "70.000,00", estado("Validado")],
            ["UG 040100", "2026NE00031", "11/01/2026", "Estimativo", "3.3.90.39 · 100 · 2031", "1.300.000,00", "0,00", "0,00", span("1 sem tipo", style="color:#FFC489;"),
             badge("Indeterminado", "gray", dashed=True), "1.040.000,00", "Indeterminado", qual("Importado – não validado")]]
    return page("T08 Empenhos — notas de empenho", "empenhos", [("Empenhos", "Empenhos.dc.html"), "B Notas de empenho"],
                [listbar(4, 1, acts=[btn("Importar notas e movimentos (L04)", href="Importacao.dc.html", small_=True)]),
                 table(["Unidade emitente", "Número", "Data", "Tipo", "Classificação", ("Valor inicial", "r"), ("Reforços", "r"), ("Anulações", "r"), ("Estornos", "r"),
                        ("Valor atualizado", "r"), ("Liquidado", "r"), ("Saldo", "r"), "Validação"], rows, minw=1600, dense=True),
                 hist,
                 alert("warn", "2026NE00031 — movimento não classificado na origem", "Estorno sem tipo torna E “indeterminado” até o saneamento; o sistema não infere sinal. "
                       "Providência de saneamento aberta para L. Martins."),
                 alert("info", "Regras", "Chave: unidade emitente + exercício + número — nota duplicada é rejeitada; relatório oficial com nota já digitada é reconhecido como o mesmo lançamento (CEN05). "
                       "Validação por usuário diferente do que lançou.")],
                tabs_=tabs(T08_TABS, "B Notas de empenho"),
                acts=[btn("Nova nota", href="T0801-NotaEmpenho.dc.html", kind="primary", ico="plus"), btn("Novo movimento", href="T0801-Movimento.dc.html"), btn("Validar selecionadas")],
                sub="Notas do exercício com reforços, anulações, estornos, valor atualizado, liquidado e saldo.")


@screen("T08C-RestosPagar.dc.html", "T08.C Empenhos — Restos a pagar", "r06", "T08.C")
def t08c():
    return page("T08 Empenhos — restos a pagar", "empenhos", [("Empenhos", "Empenhos.dc.html"), "C Restos a pagar"],
                [alert("warn", "Bloco separado", "O saldo de restos a pagar não compensa o exercício corrente nem recebe obrigação de competência posterior (C09; CF11)."),
                 table(["Nota", "Contrato", "Exercício de origem", "Inscrição", "Tipo", ("Inscrito", "r"), ("Saldo", "r"), "Obrigações vinculadas"],
                       [["2025NE00900", "027/2024 · Gama Vigilância Ltda", "2025", "2026", "Não processado", "80.000,00", "80.000,00", "Competências 11/2025 e 12/2025"],
                        ["2025NE00480", "012/2025 · Alfa Serviços Prediais Ltda", "2025", "2026", "Processado", "90.666,67", "0,00", "Competências 11/2025 e 12/2025"]], dense=True),
                 alert("info", "Exemplo (CF11)", "027/2024: restos a pagar com saldo 80.000; exercício 2026 com S = 20.000, O = 30.000, F = 0 → D(2026) = −10.000 (insuficiência existente) "
                       "e R(2026) = 10.000. O saldo de restos a pagar não compensa."),
                 actions(btn("Registrar inscrição", kind="primary"))],
                tabs_=tabs(T08_TABS, "C Restos a pagar"), sub="Notas de exercícios anteriores inscritas, tipo, saldo e obrigações vinculadas.")


@screen("T08D-Solicitacoes.dc.html", "T08.D Empenhos — Solicitações de reforço", "r06", "T08.D")
def t08d():
    rows = [["REF-2026-012", "044/2023 · Épsilon", "10.000,00", mem(100000, 40000, 20000, 50000), "09/11/2026", "01/12/2026", "SEI-040014/000301/2023", "L. Martins",
             estado("Solicitada — aguardando DIRAF", "yellow"), "—"],
            ["REF-2026-013", "027/2024 · Gama", "10.000,00", "C09 · insuficiência existente", "06/11/2026", "10/11/2026", "SEI-040014/000233/2024", "L. Martins",
             estado("Aprovada internamente — aguardando movimento oficial", "blue"), "—"],
            ["REF-2026-007", "012/2025 · Alfa", "300.000,00", "C09 · abril/2026", "20/04/2026", "15/05/2026", "SEI-040014/000418/2025", "L. Martins",
             estado("Atendida", "green"), "2026NE00140 (conciliado)"]]
    return page("T08 Empenhos — solicitações de reforço", "empenhos", [("Empenhos", "Empenhos.dc.html"), "D Solicitações de reforço"],
                [listbar(3, 0), table(["Solicitação", "Contrato", ("Valor estimado", "r"), "Memória", "Solicitada em", "Data necessária", "Processo", "Responsável", "Situação", "Movimento de atendimento"],
                                      rows, minw=1500, dense=True),
                 alert("warn", "Solicitar ou aprovar internamente não altera o saldo", "“Atendida” exige o movimento oficial conciliado. O aviso N07 se repete até o movimento oficial (CN18).")],
                tabs_=tabs(T08_TABS, "D Solicitações de reforço"), acts=[btn("Nova solicitação", href="T0801-Reforco.dc.html", kind="primary", ico="plus"), btn("Atualizar situação")],
                sub="Valor estimado, memória, datas, processo, responsável, situação e movimento de atendimento.")


# ======================================================================= T08.01
def saldos(antes, depois, nota=None):
    keys = [k for k, _ in antes]
    rows = [[k, v1, dict(depois).get(k, v1)] for k, v1 in antes]
    return section("Saldos antes e depois do lançamento", table(["Indicador", ("Antes", "r"), ("Depois", "r")], rows, dense=True), small(nota) if nota else None, h=3)


def t0801(var, body, ladeado, sub):
    return page(f"T08.01 Movimentação financeira — {var}", "empenhos", [("Empenhos", "Empenhos.dc.html"), "Movimentação e solicitação", var],
                [tabs(T0801_TABS, var, label="Variante do lançamento"),
                 modes(importar="Importacao.dc.html", leiaute="L04 e L05", fonte="sistema financeiro", fonte_ativa=False),
                 div(div(*body, style="flex:999 1 560px;min-width:0;display:flex;flex-direction:column;gap:16px;"),
                     div(ladeado, style="flex:1 1 320px;min-width:0;max-width:420px;"), style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start;"),
                 form_actions(validar=True, note="Validação por usuário diferente do que lançou. Rascunho não altera saldos.")],
                h1="T08.01 Movimentação financeira e solicitação de reforço", sub=sub)


@screen("T0801-NotaEmpenho.dc.html", "T08.01 Variante — Nota de empenho", "r06", "T08.01")
def v_nota():
    f = section("Nota de empenho", form_grid(
        field("Contrato", kind="select", req=True, options=["041/2026 — Lambda Software Ltda"]), field("Unidade emitente", "UG 040100", req=True),
        field("Exercício", "2026", req=True), field("Número", "2026NE00212", req=True, note="Chave: unidade emitente + exercício + número."),
        field("Data de emissão", "09/11/2026", req=True, kind="date", note="Ano da emissão igual ao exercício."),
        field("Tipo", kind="select", req=True, options=["Ordinário", "Estimativo", "Global"]), field("Natureza da despesa", "3.3.90.40", req=True),
        field("Fonte", "100", req=True), field("Programa de trabalho", "09.122.0002.2031", req=True), field("Valor inicial", "318.000,00", req=True, kind="money"),
        field("Credor (opcional)", "Lambda Software Ltda")))
    return t0801("Nota de empenho", [f, alert("danger", "Exemplo de rejeição", "Nota 2026NE00044 da UG 040100 já registrada — duplicidade recusada; diferença de valor vira divergência (CEN05).")],
                 saldos([("E (041/2026, 2026)", "Não apurado"), ("S", "Não apurado"), ("D", "Não apurado")], [("E (041/2026, 2026)", "318.000,00"), ("S", "318.000,00"), ("D", "318.000,00")],
                        "Empenho desconhecido é “não apurado”, nunca zero."), "Variante: nota de empenho — todos os campos obrigatórios, exceto credor.")


@screen("T0801-Movimento.dc.html", "T08.01 Variante — Movimento de empenho", "r06", "T08.01")
def v_mov():
    f = section("Movimento de empenho", form_grid(
        field("Nota", kind="select", req=True, options=["2026NE00044 — 044/2023 Épsilon"]),
        field("Tipo", kind="select", req=True, options=["Reforço", "Anulação", "Estorno de reforço", "Estorno de anulação"], note="Não há estorno “sem tipo”."),
        field("Valor", "10.000,00", req=True, kind="money"), field("Data", "10/11/2026", req=True, kind="date"), field("Documento oficial", "2026NE00230", req=True),
        field("Movimento estornado", "", placeholder="Somente para estornos: movimento do mesmo empenho e do tipo correspondente, sem excedê-lo")))
    return t0801("Movimento de empenho", [f, alert("info", "Aceite", "Pedido de reforço de 10.000 não altera a nota; reforço oficial de 10.000 altera exatamente esse valor. "
                                                   "Movimento não classificado na origem fica como pendência e torna E indeterminado.")],
                 saldos([("E", "100.000,00"), ("S", "60.000,00"), ("D", "40.000,00"), ("R", "10.000,00")], [("E", "110.000,00"), ("S", "70.000,00"), ("D", "50.000,00"), ("R", "0,00")]),
                 "Variante: movimento de empenho (reforço, anulação, estorno de reforço, estorno de anulação).")


@screen("T0801-Liquidacao.dc.html", "T08.01 Variante — Liquidação", "r06", "T08.01")
def v_liq():
    f = section("Liquidação", form_grid(
        field("Obrigação", kind="select", req=True, options=["060/2024 · competência 10/2026 · 10.500,00"]), field("Documento fiscal", "NFS-e 778 (emitida 03/11/2026)", req=True),
        field("Valor", "10.500,00", req=True, kind="money"), field("Data", "10/11/2026", req=True, kind="date"),
        field("Referência oficial", "2026NL01022", req=True, note="Única; estorno aponta a liquidação original.")),
        table(["Nota de empenho", ("Valor alocado", "r")], [["2026NE00090", "6.000,00"], ["2026NE00151", "4.000,00"]], foot=["Soma das alocações", "10.000,00"],
              caption="Alocação por nota de empenho (notas do mesmo contrato)", dense=True),
        error_summary([("Soma das alocações (10.000,00) diferente do total da liquidação (10.500,00) — rateio recusado sem ajuste silencioso", "T0801-Liquidacao.dc.html")]))
    return t0801("Liquidação", [f], saldos([("L (conjunto 2026)", "40.000,00"), ("S", "90.000,00"), ("O", "11.600,00"), ("D", "78.400,00")],
                                         [("L (conjunto 2026)", "50.500,00"), ("S", "79.500,00"), ("O", "1.100,00"), ("D", "78.400,00")],
                                         "Depois: valores previstos após corrigir o rateio."), "Variante: liquidação com alocação por nota de empenho.")


@screen("T0801-Pagamento.dc.html", "T08.01 Variante — Pagamento", "r06", "T08.01")
def v_pag():
    f = section("Pagamento", form_grid(
        field("Liquidação", kind="select", req=True, options=["2026NL00877 — 031/2023 Beta · 60.000,00"]), field("Data", "20/10/2026", req=True, kind="date"),
        field("Valor líquido ao credor", "23.000,00", req=True, kind="money"), field("Referência oficial", "2026OB00412", req=True)),
        table(["Retenção", ("Valor", "r"), "Data", "Documento de recolhimento", "Efeito"],
              [["ISS", "2.000,00", "20/10/2026", "GUIA-2026-1187", badge("Recolhida — baixa", "green")],
               ["INSS", "5.000,00", "—", span("Não informado", style="color:#FFC489;"), badge("Apenas calculada — não baixa", "yellow")]], caption="Retenções", dense=True),
        kv([("Baixa bruta (C11)", "23.000,00 + 2.000,00 = R$ 25.000,00"), ("Limite", "Limitada ao liquidado (R$ 60.000,00)")]))
    return t0801("Pagamento", [f, alert("info", "Aceite (CF04)", "Baixa bruta 25.000; liquidado a pagar 35.000; E e execução inalterados; baixa reimportada com a mesma referência não duplica.")],
                 saldos([("Liquidado a pagar", "60.000,00"), ("Retenções apenas calculadas", "0,00"), ("E", "Indeterminado"), ("Execução", "inalterada")],
                        [("Liquidado a pagar", "35.000,00"), ("Retenções apenas calculadas", "5.000,00"), ("E", "Indeterminado"), ("Execução", "inalterada")]),
                 "Variante: pagamento com retenções (baixa bruta = líquido + retenções recolhidas).")


@screen("T0801-Reforco.dc.html", "T08.01 Variante — Solicitação de reforço", "r06", "T08.01")
def v_ref():
    f = section("Solicitação de reforço", form_grid(
        field("Contrato", kind="select", req=True, options=["044/2023 — Épsilon Elevadores Ltda"]), field("Conjunto orçamentário", "2026 · 3.3.90.39 · 100 · PT 2031", req=True, ro=True),
        field("Valor estimado", "10.000,00", req=True, kind="money", nature="Parâmetro interno", help="Proposto pela C09; editável com justificativa."),
        field("Justificativa da edição", "", kind="textarea", placeholder="Obrigatória se o valor proposto for alterado"),
        field("Data necessária", "01/12/2026", req=True, kind="date", note="Data de insuficiência (C10)."), field("Processo", "SEI-040014/000301/2023"),
        field("Responsável", kind="select", options=["L. Martins", "M. Silva"])),
        mem(100000, 40000, 20000, 50000))
    return t0801("Solicitação de reforço", [f], saldos([("E", "100.000,00"), ("D", "40.000,00"), ("R", "10.000,00")], [("E", "100.000,00 (inalterado)"), ("D", "40.000,00"), ("R", "10.000,00")],
                                                     "Solicitar ou aprovar internamente não altera o saldo; só o movimento oficial conciliado."),
                 "Variante: solicitação de reforço com valor e memória propostos pela C09.")
