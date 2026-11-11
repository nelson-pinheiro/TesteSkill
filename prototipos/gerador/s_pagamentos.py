"""T09 Documentos fiscais e pagamentos (totais fixos e abas A–E) e T10 Reajustes, repactuações e revisões (A–C) com T10.01."""
from shell import *
from s_inicio import ctr_cell

O_TOTAL, LAP_TOTAL, PAGO, IMPED = 338400.00, 105000.00, 6482310.00, 183800.00


def totais():
    return grid(
        div(stat("Executado não liquidado", money(O_TOTAL), "8 obrigações · Execução registrada"),
            composicao(("012/2025 — 10/2026 (atesto incompleto)", "91.800,00"), ("019/2025 — 10/2026 e item sem alocação", "65.000,00"), ("060/2024 — 10/2026 e complementar", "11.600,00"),
                       ("044/2023 — 10/2026", "20.000,00"), ("027/2024 — parcela de 10/2026", "30.000,00"), ("038/2024 — etapa 3 (recebimento presumido)", "120.000,00"), formula="C07")),
        div(stat("Liquidado a pagar", money(LAP_TOTAL), "4 liquidações · C11"),
            composicao(("019/2025 — NFS-e 4471", "62.000,00"), ("031/2023 — NF-e 3301 (pagamento parcial)", "35.000,00"), ("044/2023 — NFS-e 2210 (pagamento parcial)", "6.000,00"),
                       ("015/2022 — encerrado", "2.000,00"), formula="C11")),
        div(stat("Pago no exercício", money(PAGO), "baixas brutas até 10/11/2026"), composicao(("Líquido ao credor", "5.902.610,00"), ("Retenções recolhidas", "579.700,00"), formula="C11")),
        div(stat("Com impedimento", money(IMPED), "3 impedimentos abertos", "orange"),
            composicao(("Atesto incompleto — 012/2025", "91.800,00"), ("Regularidade fiscal — 019/2025", "62.000,00"), ("Documento incorreto — 027/2024", "30.000,00"))),
        min_=240)


def t09page(tab, body, sub, acts=None):
    return page("T09 Documentos fiscais e pagamentos", "pagamentos", ["Pagamentos", tab],
                [filterbar(fsel("Contrato", "Todos", "012/2025", "019/2025", "044/2023", "060/2024"), fsel("Competência", "Todas", "10/2026", "09/2026"),
                           fsel("Situação", "Todas", "Pendentes", "Com impedimento")), totais(), *body],
                tabs_=tabs(T09_TABS, tab), sub=sub, acts=acts)


@screen("Pagamentos.dc.html", "T09.A Pagamentos — Obrigações", "r07", "T09.A")
def t09a():
    rows = [
        [ctr_cell("012/2025", "Alfa Serviços Prediais Ltda"), "10/2026 · itens 1–5", "91.800,00", "0,00", "91.800,00", "0,00", "31/10/2026", "Limite 15/11/2026 · registrado 03/11/2026",
         "Limite 03/12/2026 · a registrar", span("Não registrada", style="color:#FFC489;"), "2026 · 3.3.90.37", "0,00", "91.800,00"],
        [ctr_cell("019/2025", "Delta Copeiragem Ltda"), "10/2026 · postos", "62.000,00", "0,00", "62.000,00", "0,00", "31/10/2026", "Limite 15/11/2026 · registrado 04/11/2026",
         "Limite 04/12/2026 · a registrar", span("Não registrada", style="color:#FFC489;"), "2026 · 3.3.90.37", "0,00", "62.000,00"],
        [ctr_cell("019/2025", "Delta Copeiragem Ltda"), "09/2026 · reposição de insumos (seq. 2)", "3.000,00", "0,00", "3.000,00", "0,00", "30/09/2026", "Registrado 05/10/2026",
         "Registrado 03/11/2026", "Registrada 08/10/2026", cat(badge("Sem alocação", "orange"), a(" alocar", "Pagamentos.dc.html")), "0,00", "3.000,00"],
        [ctr_cell("060/2024", "Sigma Climatização Ltda"), "10/2026", "10.500,00", "0,00", "10.500,00", "0,00", "31/10/2026", "Limite 15/11/2026 · a registrar (aviso N16 em 10/11)",
         "—", "Não aplicável", "2026 · 3.3.90.39", "0,00", "10.500,00"],
        [ctr_cell("060/2024", "Sigma Climatização Ltda"), "08–10/2026 · complementar (apostila nº 1)", "1.500,00", "0,00", "1.500,00", "0,00", "05/10/2026", "—", "—", "Não aplicável",
         "2026 · 3.3.90.39", "400,00", "1.100,00"],
        [ctr_cell("044/2023", "Épsilon Elevadores Ltda"), "10/2026 · medição", "20.000,00", "0,00", "20.000,00", "0,00", "31/10/2026", "Registrado 03/11/2026", "Limite 03/12/2026", "Não aplicável",
         "2026 · 3.3.90.39", "0,00", "20.000,00"],
        [ctr_cell("027/2024", "Gama Vigilância Ltda"), "10/2026", "240.000,00", "0,00", "240.000,00", "30.000,00", "05/11/2026", "Registrado 05/11/2026", "Limite 05/12/2026",
         "Registrada 06/11/2026", "2026 · 3.3.90.37", "210.000,00", "30.000,00"],
        [ctr_cell("038/2024", "Kapa Construções Ltda"), "Etapa 3 — instalações", "120.000,00", "0,00", "120.000,00", "0,00", "01/10/2026",
         cat(badge("Recebimento presumido — validar", "yellow"), small(" limite 16/10/2026 sem termo")), "—", "Não aplicável", "2026 · 4.4.90.51", "0,00", "120.000,00"],
    ]
    return t09page("A Obrigações", [
        listbar(len(rows), 1),
        table(["Contrato", "Competência ou etapa · item", ("Valor bruto", "r"), ("Glosa", "r"), ("Reconhecido", "r"), ("Controversa", "r"), "Adimplemento",
               "Recebimento provisório (C22)", "Recebimento definitivo (C22)", "Conferência trabalhista", "Alocação orçamentária", ("Liquidado", "r"), ("A liquidar", "r")],
              rows, minw=1900, dense=True),
        alert("info", "Regras", "Repetição da mesma obrigação (contrato, item e competência) é recusada; a segunda medição do mês exige sequência explícita. "
              "Recebimento presumido (art. 20, § 3º) só é gravado após confirmação do gestor (CN23). Conferência trabalhista mensal em contratos com dedicação exclusiva de mão de obra."),
    ], "Da execução ao pagamento, sem confundir execução, liquidação e pagamento.",
        acts=[btn("Nova obrigação", kind="primary", ico="plus"), btn("Estornar com motivo"), btn("Registrar recebimento"), btn("Alocar a conjunto orçamentário")])


@screen("T09B-DocFiscais.dc.html", "T09.B Pagamentos — Documentos fiscais", "r07", "T09.B")
def t09b():
    def at(*xs):
        return col(*[small(x_) for x_ in xs], gap=2)
    rows = [
        ["Alfa Serviços Prediais Ltda", "NFS-e · 1 · 1187", "—", "03/11/2026", "10/2026", "91.800,00", "03/12/2026", "Obrigação 10/2026: 91.800,00",
         at("J. Prado · fiscal técnico · 03/11/2026"), cat(badge("Insuficiente", "orange"), small(" 1 de 2 fiscais (CD05)")), "7"],
        ["Delta Copeiragem Ltda", "NFS-e · 1 · 4471", "—", "01/10/2026", "09/2026", "62.000,00", "31/10/2026", "Obrigação 09/2026: 62.000,00",
         at("C. Ramos · fiscal administrativo · 02/10/2026", "M. Lopes · fiscal técnico · 02/10/2026"), badge("Suficiente", "green"),
         cat(strong("40", style="color:#FFC489;font-weight:700;"), small(" · N13 em 15/11/2026; marco legal 01/12/2026"))],
        ["Épsilon Elevadores Ltda", "NFS-e · A · 2210", "—", "05/10/2026", "09/2026", "10.000,00", "04/11/2026", "Obrigação 09/2026: 10.000,00",
         at("R. Moraes · fiscal técnico · 06/10/2026", "S. Pires · fiscal técnico · 06/10/2026"), badge("Suficiente", "green"), "36"],
        ["Épsilon Elevadores Ltda", "NFS-e · A · 2251", "—", "03/11/2026", "10/2026", "20.000,00", "03/12/2026", "Obrigação 10/2026: 20.000,00",
         at("R. Moraes · fiscal único titular · 04/11/2026", "Autoridade designada · 04/11/2026"), cat(badge("Suficiente", "green"), small(" fiscal único + autoridade")), "7"],
        ["Sigma Climatização Ltda", "NFS-e · 1 · 790", "—", "06/10/2026", "08–10/2026", "1.500,00", "05/11/2026", "Rateio: 08/2026 500,00 · 09/2026 500,00 · 10/2026 500,00",
         at("G. Antunes · fiscal técnico", "H. Barros · fiscal técnico"), badge("Suficiente", "green"), "35"],
        ["Gama Vigilância Ltda", "NFS-e · 1 · 9910", "33190112345678000195550010000099101000012345", "04/11/2026", "10/2026", "240.000,00", "04/12/2026", "Obrigação 10/2026: 240.000,00",
         at("Fiscal técnico · 05/11/2026", "Fiscal administrativo · 05/11/2026"), badge("Suficiente", "green"), "6"],
    ]
    return t09page("B Documentos fiscais", [
        listbar(len(rows), 0, acts=[btn("Importar XML ou planilha (L06)", href="Importacao.dc.html", small_=True)]),
        table(["Emissor", "Tipo · série · número", "Chave", "Emissão", "Competência", ("Valor", "r"), "Vencimento", "Rateio por obrigação", "Atestos (quem, qualidade, quando)",
               "Suficiência do atesto (C21)", ("Dias desde a emissão", "r")], rows, minw=1800, dense=True),
        alert("warn", "NFS-e 1187 (012/2025) — impedimento “atesto incompleto” proposto automaticamente", "Contrato com 2 fiscais e 1 atesto: insuficiente (Decreto RJ nº 48.817/2023, art. 22, XXIII e § 2º)."),
        small("Rateio não excede o documento nem a obrigação. Documento duplicado (emissor + tipo + série + número) é rejeitado; vincular documento a obrigação existente não cria nova execução."),
    ], "Documentos fiscais com rateio, atestos e suficiência do atesto (C21).",
        acts=[btn("Novo documento", kind="primary", ico="plus"), btn("Ratear entre obrigações"), btn("Registrar atesto"), btn("Enviar à liquidação")])


@screen("T09C-Liquidacoes.dc.html", "T09.C Pagamentos — Liquidações", "r07", "T09.C")
def t09c():
    rows = [["15/10/2026", "2026NL01011", "019/2025 · Delta", "62.000,00", "2026NE00058: 62.000,00", "—"],
            ["15/10/2026", "2026NL00877", "031/2023 · Beta", "60.000,00", "2026NE00031: 60.000,00", "—"],
            ["20/10/2026", "2026NL00990", "044/2023 · Épsilon", "10.000,00", "2026NE00044: 10.000,00", "—"],
            ["06/11/2026", "2026NL01002", "027/2024 · Gama", "210.000,00", "2026NE00027: 210.000,00", "—"],
            ["02/10/2026", "2026NL00950", "060/2024 · Sigma", "10.000,00", "2026NE00090: 10.000,00", "Estornada por 2026NL00951 (motivo: competência incorreta)"],
            ["08/10/2026", "2026NL00860", "027/2024 · Gama", span("240.500,00", style="color:#FFB3B8;font-weight:600;"), "2026NE00027: 240.500,00",
             badge("Inconsistência: liquidação superior à obrigação (09/2026) em 500,00", "red")]]
    return t09page("C Liquidações", [listbar(len(rows), 0), table(["Data", "Referência oficial", "Contrato", ("Valor", "r"), "Alocação por nota", "Estornos e inconsistências"], rows, minw=1100, dense=True),
                                     small("Soma das alocações igual ao total; notas do mesmo contrato; referência oficial única.")],
                   "Liquidações com alocação por nota de empenho e estornos.", acts=[btn("Nova liquidação (T08.01)", href="T0801-Liquidacao.dc.html", kind="primary", ico="plus")])


@screen("T09D-Pagamentos.dc.html", "T09.D Pagamentos — Pagamentos e retenções", "r07", "T09.D")
def t09d():
    rows = [["20/10/2026", "2026OB00412", "031/2023 · Beta — 2026NL00877", "23.000,00", "ISS 2.000,00", "INSS 5.000,00", "25.000,00", "60.000,00", strong("35.000,00")],
            ["28/10/2026", "2026OB00430", "044/2023 · Épsilon — 2026NL00990", "3.700,00", "ISS 300,00", "—", "4.000,00", "10.000,00", strong("6.000,00")],
            ["15/10/2026", "2026OB00301", cat("015/2022 · Teta — 2026NL00799 ", badge("Encerrado — permanece listado", "gray")), "2.850,00", "ISS 150,00", "—", "3.000,00", "5.000,00", strong("2.000,00")],
            ["—", "—", "019/2025 · Delta — 2026NL01011", "—", "—", "—", "0,00", "62.000,00", cat(strong("62.000,00"), small(" impedimento: regularidade fiscal"))]]
    return t09page("D Pagamentos e retenções", [
        listbar(4, 0, acts=[btn("Importar liquidações e pagamentos (L05)", href="Importacao.dc.html", small_=True)]),
        table(["Data", "Referência oficial", "Liquidação", ("Líquido", "r"), "Retenções recolhidas", "Apenas calculadas", ("Baixa bruta", "r"), ("Liquidado", "r"), ("Saldo a pagar", "r")],
              rows, foot=["", "", "Total", "29.550,00", "", "", "32.000,00", "137.000,00", "105.000,00"], minw=1300, dense=True),
        alert("info", "Exemplos de aceite", "CF04: líquido 23.000 + retenção recolhida 2.000 = baixa 25.000; liquidado a pagar 35.000. "
              "CF05: documento de 10.000 integralmente liquidado com pagamento de 4.000 mantém 6.000 a pagar. Retenção apenas calculada não baixa."),
    ], "Pagamentos com retenções recolhidas e apenas calculadas, baixa bruta e saldo a pagar.", acts=[btn("Novo pagamento (T08.01)", href="T0801-Pagamento.dc.html", kind="primary", ico="plus")])


@screen("T09E-Impedimentos.dc.html", "T09.E Pagamentos — Impedimentos", "r07", "T09.E")
def t09e():
    rows = [[badge("Atesto incompleto", "orange"), "012/2025 · NFS-e 1187 — falta o atesto de F. Dias (fiscal administrativo)", "F. Dias", a("Colher 2º atesto", "T11B-Todas.dc.html"), "03/11/2026", "—",
             small("Proposto automaticamente pela C21")],
            [badge("Regularidade fiscal", "orange"), "019/2025 · NFS-e 4471 — certidão federal vencida", "L. Martins", a("Solicitar certidão atualizada", "T11B-Todas.dc.html"), "15/10/2026", "—", ""],
            [badge("Documento incorreto", "orange"), "027/2024 · NFS-e 9910 — parcela de 30.000,00 sem medição correspondente", "P. Nunes", a("Solicitar carta de correção", "T11B-Todas.dc.html"), "05/11/2026", "—", ""],
            [badge("Recebimento pendente", "gray"), "060/2024 · NFS-e 701 (09/2026)", "G. Antunes", "—", "02/10/2026", "08/10/2026", small("Resolvido com termo de recebimento")]]
    return t09page("E Impedimentos", [
        listbar(4, 0),
        table(["Causa", "Descrição", "Responsável", "Providência vinculada", "Abertura", "Resolução", "Observação"], rows, minw=1100, dense=True),
        small("Causas: atesto incompleto, comprovação trabalhista, regularidade fiscal, glosa em discussão, falta de empenho, documento incorreto, recebimento pendente ou outra."),
    ], "Impedimentos ao pagamento, com providência vinculada.", acts=[btn("Abrir impedimento", kind="primary", ico="plus"), btn("Vincular providência"), btn("Resolver")])


# ======================================================================= T10
def t10page(tab, body, sub, acts=None):
    return page("T10 Reajustes, repactuações e revisões", "reajustes", ["Reajustes", tab], body, tabs_=tabs(T10_TABS, tab), sub=sub,
                acts=acts or [btn("Exportar RPT08", href="Relatorios.dc.html", small_=True)])


@screen("Reajustes.dc.html", "T10.A Reajustes — Pedidos", "r07", "T10.A")
def t10a():
    rows = [
        [a("PED-2026-021", "T1001-Simulacao.dc.html"), "019/2025 · Delta", badge("Repactuação", "teal"), "Cláusula 10ª", "CCT 2026", "01/01/2026", "01/2026", "19/09/2026", "25/09/2026",
         cat(div("24/11/2026"), prazo_nat("Contrato")), "7,8% (mão de obra)", a("Ver memória", "T1001-Simulacao.dc.html"), "Análise da fiscalização · 52 dias sem movimentação", "C. Ramos", "—", "—", "—"],
        [a("PED-2026-024", "T1001-Simulacao.dc.html"), "044/2023 · Épsilon", badge("Reajuste", "blue"), "Cláusula 8ª", "IPCA", "15/06/2025", "06/2025 a 05/2026", "20/10/2026", "22/10/2026",
         cat(div("22/11/2026"), prazo_nat("Legal supletivo")), "4,4%", a("Ver memória", "T1001-Simulacao.dc.html"), "Cálculo", "P. Nunes", "—", "—", "—"],
        [a("PED-2026-015", "T1001-Simulacao.dc.html"), "021/2025 · Zeta", badge("Repactuação", "teal"), "Cláusula 11ª", "CCT 2026", "01/01/2026", "01/2026", "10/08/2026", "18/08/2026",
         cat(div("17/10/2026"), prazo_nat("Parâmetro interno")), "6,1%", a("Ver memória", "T1001-Simulacao.dc.html"), "Decidido — aguardando formalização", "S. Moura",
         "Deferido em 30/10/2026", span("Pendente (apostila)", style="color:#FFC489;"), "01/01/2026 (retroativo)"],
        [a("PED-2026-009", "T10C-Retroativos.dc.html"), "060/2024 · Sigma", badge("Reajuste", "blue"), "Cláusula 7ª", "IPCA", "01/08/2025", "08/2025 a 07/2026", "05/08/2026", "10/08/2026",
         cat(div("10/09/2026"), prazo_nat("Legal supletivo")), "5,00%", a("Ver memória", "T10C-Retroativos.dc.html"), "Formalizado", "P. Nunes", "Deferido em 28/09/2026",
         "Apostila nº 1 (05/10/2026)", "01/08/2026"],
        [a("PED-2026-004", "Reajustes.dc.html"), "047/2024 · Nu Telecom", badge("Revisão do equilíbrio", "purple"), "Art. 124, II, d", "—", "—", "—", "02/03/2026", "20/03/2026",
         cat(div("20/04/2026"), prazo_nat("Parâmetro interno")), "R$ 3.200,00/mês", a("Ver memória", "Reajustes.dc.html"), "Encerrado", "A. Lima", "Indeferido em 12/05/2026", "—", "—"],
    ]
    return t10page("A Pedidos", [
        row(tabs([("Todos", "Reajustes.dc.html"), ("Reajuste", "Reajustes.dc.html"), ("Repactuação", "Reajustes.dc.html"), ("Revisão do equilíbrio", "Reajustes.dc.html")], "Todos",
                 label="Filtros por tipo"), gap=8),
        listbar(len(rows), 0),
        table(["Pedido", "Contrato", "Tipo", "Previsão e cláusula", "Índice", "Data-base", "Período de referência", "Pedido em", "Instrução completa", "Prazo de resposta (natureza)",
               "Solicitado", "Memória", "Etapa", "Responsável", "Decisão", "Formalização", "Início dos efeitos"], rows, minw=2200, dense=True),
        alert("info", "Regras", "Pedido e simulação não entram no valor oficial. Indeferidos e cancelados permanecem consultáveis. Prazo contratual rotulado “Contrato”; supletivo de 1 mês, “Legal”; "
              "prazo interno, “Parâmetro interno” (CN16)."),
    ], "Pedidos, decisões, formalização e retroativos (Diretriz, item 8).",
        acts=[btn("Novo pedido", kind="primary", ico="plus"), btn("Registrar decisão"), btn("Simular (T10.01)", href="T1001-Simulacao.dc.html"), btn("Formalizar (T04.01)", href="T0401-Formalizacao.dc.html")])


@screen("T10B-DatasBase.dc.html", "T10.B Reajustes — Datas-base", "r07", "T10.B")
def t10b():
    rows = [[ctr_cell("012/2025", "Alfa Serviços Prediais Ltda"), "Insumos: IPCA · Mão de obra: CCT", "Insumos 08/2025 · Mão de obra 01/01/2026", "Nenhum",
             "Insumos 08/2026 (habilitado) · Mão de obra 01/01/2027", cat(div("90 dias"), prazo_nat("Parâmetro interno")), "03/10/2026 (mão de obra)", a("Iniciar pedido", "Reajustes.dc.html")],
            [ctr_cell("019/2025", "Delta Copeiragem Ltda"), "Insumos: IPCA · Mão de obra: CCT", "Insumos 07/2025 · Mão de obra 01/01/2026", "Nenhum",
             "Mão de obra 01/01/2027 · insumos 07/2026 (habilitado)", cat(div("90 dias"), prazo_nat("Parâmetro interno")), "03/10/2026", a("Abrir pedido PED-2026-021", "Reajustes.dc.html")],
            [ctr_cell("033/2025", "Mu Comunicação Ltda"), "IPCA", "01/03/2026", "Nenhum", "01/03/2027", cat(div("90 dias"), prazo_nat("Parâmetro interno")), "01/12/2026 (CN15)", small("Pedido habilitado após 12 meses")],
            [ctr_cell("047/2024", "Nu Telecom S.A."), "IST", "23/01/2026", "23/01/2026 (3,9%)", "23/01/2027", cat(div("90 dias"), prazo_nat("Parâmetro interno")), "25/10/2026 (emitido)", a("Iniciar pedido", "Reajustes.dc.html")],
            [ctr_cell("060/2024", "Sigma Climatização Ltda"), "IPCA", "01/08/2026", "01/08/2026 (5,00% — apostila nº 1)", "01/08/2027", cat(div("90 dias"), prazo_nat("Parâmetro interno")), "03/05/2027", small("Interregno de 12 meses")]]
    return t10page("B Datas-base", [listbar(len(rows), 1), table(["Contrato", "Índice", "Data-base", "Último reajuste", "Próxima data-base", "Antecedência do aviso N04", "Aviso N04", "Ação"], rows, minw=1300, dense=True),
                                    small("Para repactuação, datas distintas de insumos e de mão de obra. Pedido habilitado após o interregno de 12 meses da data-base.")],
                   "Agenda das próximas datas-base por contrato, com índice, último reajuste e antecedência do aviso N04.")


@screen("T10C-Retroativos.dc.html", "T10.C Reajustes — Retroativos", "r07", "T10.C")
def t10c():
    rows = [["Apostila nº 1 — 060/2024", "Itens 1 e 2", "08/2026", "10.000,00", "10.500,00", "500,00", a("OC-2026-0801", "Pagamentos.dc.html"), "400,00", "100,00"],
            ["Apostila nº 1 — 060/2024", "Itens 1 e 2", "09/2026", "10.000,00", "10.500,00", "500,00", a("OC-2026-0901", "Pagamentos.dc.html"), "0,00", "500,00"],
            ["Apostila nº 1 — 060/2024", "Itens 1 e 2", "10/2026", "10.000,00", "10.500,00", "500,00", a("OC-2026-1001", "Pagamentos.dc.html"), "0,00", "500,00"]]
    return t10page("C Retroativos", [
        section("Diferenças por alteração formalizada, item e competência (C12)",
                table(["Alteração formalizada", "Item", "Competência", ("Já reconhecido", "r"), ("Revisto", "r"), ("Diferença", "r"), "Obrigação complementar", ("Pago", "r"), ("Pendente", "r")],
                      rows, foot=["Total", "", "", "30.000,00", "31.500,00", "1.500,00", "", "400,00", "1.100,00"], minw=1100, dense=True),
                actions(btn("Reprocessar (substitui, nunca soma)", kind="primary"), btn("Abrir obrigação complementar", href="Pagamentos.dc.html")),
                small("Só diferença formalmente reconhecida gera obrigação. Reprocessar e reimportar não alteram o resultado (CF07)."), h=3),
        section("Créditos a compensar (bloco próprio)",
                table(["Alteração formalizada", "Item", "Competência", ("Reconhecido", "r"), ("Revisto", "r"), ("Crédito a compensar", "r")],
                      [["Apostila nº 2 — 047/2024 (correção do índice IST)", "Item 1", "09/2026", "45.020,00", "45.000,00", "20,00"]], dense=True),
                small("Diferença negativa gera “crédito a compensar”, nunca obrigação negativa (CR03)."), h=3),
    ], "Por alteração formalizada, item e competência: reconhecido, revisto, diferença, obrigação complementar, pago e pendente.")


@screen("T1001-Simulacao.dc.html", "T10.01 Simulação e memória de cálculo", "r07", "T10.01")
def t1001():
    return page("T10.01 Simulação e memória de cálculo", "reajustes", [("Reajustes", "Reajustes.dc.html"), "PED-2026-021", "Simulação"], [
        alert("sim", "Simulação", "Rótulo “Simulação” em todas as saídas. Alterar o percentual recalcula a hipótese e mantém o valor formal (CR02)."),
        section("Premissas", form_grid(
            field("Tipo", kind="select", options=["Repactuação", "Reajuste", "Revisão do equilíbrio"]), field("Percentual — mão de obra", "6,20%"),
            field("Índice — insumos", "IPCA 4,10%"), field("Data-base", "01/01/2026 (CCT 2026)"), field("Período de referência", "01/2026"),
            field("Início dos efeitos", "01/01/2026", kind="date")),
            actions(btn("Recalcular"), btn("Salvar como cenário (T07.D)", href="T07D-Cenarios.dc.html", kind="primary")), tone="sim"),
        section("Comparação", row(nat("Formalizado"), nat("Simulação"), gap=6),
                table(["Componente", ("Formalizado (mensal)", "r"), ("Simulado (mensal)", "r"), ("Diferença", "r")],
                      [["Mão de obra (postos)", "54.000,00", "57.348,00", "+3.348,00"], ["Insumos", "8.000,00", "8.328,00", "+328,00"]],
                      foot=["Total", "62.000,00", "65.676,00", "+3.676,00"], dense=True),
                table(["Competências", ("Diferença por competência", "r"), ("Diferença retroativa estimada", "r")],
                      [["01/2026 a 10/2026 (10 competências)", "3.676,00", "36.760,00"], ["11/2026 em diante", "3.676,00", "—"]], caption="Efeitos por competência (simulação)", dense=True),
                actions(btn("Exportar memória", ico="download")), tone="sim"),
        small("Contrato 019/2025 · Delta Copeiragem Ltda · pedido de 7,8% (mão de obra). O valor formal permanece R$ 62.000,00/mês até a formalização em T04.01."),
    ], h1="T10.01 Simulação e memória de cálculo", sub="Premissas e comparação entre valores formalizados e simulados, por item e no total.")
