"""T04 Cadastro e edição do contrato (7 passos e revisão) e T04.01 Revisão e formalização de evento."""
from shell import *


def rascunho_box():
    return row(row(strong("Rascunho 063/2026 · Upsilon Brigada Ltda"), estado("Rascunho"), gap=8),
               small("Lançado por R. Costa (operador contratual) · última gravação 09/11/2026 16:40 · validação por pessoa diferente de quem lançou"),
               justify="space-between",
               style=f"padding:12px 16px;background:{SURF};border:1px solid {LINE};border-radius:8px;")


def nav_passos(n):
    prev_ = T04_STEPS[n - 2][1] if n > 1 else None
    next_ = T04_STEPS[n][1] if n < len(T04_STEPS) else None
    return row(btn("Passo anterior", href=prev_, ico="back") if prev_ else span(""),
               btn("Próximo passo", href=next_, kind="primary", ico="arrow") if next_ else span(""), justify="space-between")


def passo(n, titulo, body, fonte="PNCP", leiaute="L02", importar="Importacao.dc.html", fonte_ativa=True, ref=None):
    return page(f"T04 Cadastro e edição — passo {n} {titulo}", "carteira",
                [("Carteira", "Carteira.dc.html"), ("Rascunhos", "T02C-Rascunhos.dc.html"), "063/2026", f"Passo {n} {titulo}"],
                [rascunho_box(), stepper(T04_STEPS, n), modes(importar=importar, leiaute=leiaute, fonte=fonte, fonte_ativa=fonte_ativa), *body,
                 form_actions(), nav_passos(n)],
                h1="T04 Cadastro e edição do contrato",
                sub=f"Passo {n} de 7 — {titulo}{' · campos detalhados em ' + ref if ref else ''}. Gravação de rascunho em qualquer ponto.")


@screen("T04-P1-Identificacao.dc.html", "T04 Passo 1 — Identificação", "r04", "T04")
def p1():
    comp = section("Colisão de identidade — decisão obrigatória",
                   alert("warn", "Já existe um contrato com a mesma identidade",
                         "Número normalizado, órgão, natureza do instrumento e contratada coincidem com um registro importado do legado."),
                   table(["Campo", "Em digitação (este rascunho)", "Existente: 63/2026 — importado – não validado"],
                         [["Número normalizado", "63/2026", "63/2026"], ["Órgão", "Rioprevidência", "Rioprevidência"],
                          ["Natureza do instrumento", "Termo de contrato", "Termo de contrato"], ["Contratada (CNPJ)", "Upsilon Brigada Ltda", "Upsilon Brigada Ltda"],
                          ["Origem", origem("Digitado", "R. Costa", "09/11/2026 15:02"),
                           origem("Importado", "Lote L01 de 03/11/2026", "03/11/2026 14:02", "Lote L01 · planilha de acompanhamento · aba Contratos · linha 87")],
                          ["Vigência", "01/12/2026 a 30/11/2027", "Não informado"]], dense=True),
                   field("Decisão", kind="radio", req=True, options=["*Vincular ao existente (continuar sobre o registro importado)", "Corrigir a identificação digitada",
                                                                     "Registrar como distinto, com justificativa"]),
                   field("Justificativa (obrigatória se distinto)", "", kind="textarea", placeholder="Ex.: instrumentos distintos conferidos no SEI"),
                   tone="warn")
    form = section("Identificação (aba T03.01)", form_grid(
        field("Número do contrato", "063/2026", req=True, note="Forma normalizada gerada para busca: 63/2026"),
        field("Ano", "2026", req=True, kind="number"),
        field("Natureza do instrumento", kind="select", req=True, options=["Termo de contrato", "Carta-contrato", "Nota de empenho", "Autorização de compra", "Ordem de serviço", "Outro"]),
        field("Tipo", kind="select", req=True, options=["Serviço contínuo", "Fornecimento", "Escopo"], note="Define os campos das demais abas (tabela 6.4)."),
        field("Modelo de preço", kind="select", req=True, options=["Mensal fixo", "Medição", "Quantidades", "Etapas"]),
        field("Enquadramento no art. 2º da Lei nº 14.133/2021", kind="select", req=True, options=["V — prestação de serviços", "II — compra", "VI — obras e serviços de engenharia", "VII — TIC"],
              nature="Legal", ref="Lei nº 14.133/2021, art. 2º", help="Delimita o universo do RPT15."),
        field("Objeto resumido", "Brigada de incêndio e primeiros socorros", req=True),
        field("Unidade responsável", kind="select", req=True, options=["GERAD", "GERTIC", "DIRAF"]),
        field("Categoria", kind="select", options=["Serviços prediais", "Segurança"]), field("Grupo", kind="select", options=["Segurança contra incêndio", "Vigilância"]),
        field("Criticidade do objeto", kind="select", options=["Essencial", "Relevante", "Comum"], help="Critério de desempate da prioridade (C17)."),
    ), field("Objeto completo (texto do instrumento)", "Prestação de serviços continuados de brigada de incêndio e primeiros socorros, com dedicação exclusiva de mão de obra, "
             "nas sedes do Rioprevidência.", kind="textarea"))
    return passo(1, "Identificação", [comp, form], ref="T03.01, bloco Identificação")


@screen("T04-P2-Contratada.dc.html", "T04 Passo 2 — Contratada", "r04", "T04")
def p2():
    form = section("Contratada (aba T03.01)", form_grid(
        field("CNPJ", "41.234.567/0001-07", req=True, origin=origem("Digitado", "R. Costa", "09/11/2026 15:10"),
              note="Dígitos verificadores conferidos; aceita o formato alfanumérico (ex.: 12.ABC.345/01DE-35)."),
        field("Razão social", "Upsilon Brigada Ltda", req=True, ro=True)),
        alert("ok", "Contratada existente reutilizada", "CNPJ já cadastrado em 03/11/2026 (importação L01). O cadastro é reutilizado, não duplicado."),
        table(["Nome", "Papel", "E-mail", "Telefone", "Período", ""],
              [["V. Andrade", "Representante legal", "representante@upsilon.exemplo", "(21) 0000-0101", "desde 20/11/2026", a("Editar", "T04-P2-Contratada.dc.html")],
               ["N. Barros", "Preposto", "preposto@upsilon.exemplo", "(21) 0000-0102", "desde 01/12/2026", a("Editar", "T04-P2-Contratada.dc.html")]],
              caption="Representante, preposto e contatos — ao menos um meio de contato por pessoa", dense=True),
        btn("Adicionar contato", ico="plus", small_=True))
    exemplo = section("Exemplo de validação ao sair do campo",
                      form_grid(field("CNPJ (outro registro)", "41.234.567/0001-08", error="Dígito verificador incorreto — linha não aceita (CEN06)."),
                                field("CNPJ alfanumérico", "12.ABC.345/01DE-35", note="Válido no novo formato alfanumérico (BD44).")))
    return passo(2, "Contratada", [form, exemplo], fonte="PNCP", ref="T03.01, bloco Contratada")


@screen("T04-P3-Origem.dc.html", "T04 Passo 3 — Origem e regime", "r04", "T04")
def p3():
    yn = ["Sim", "Não", "Não informado"]
    form = section("Origem e regime jurídico (aba T03.01)", form_grid(
        field("Modalidade ou forma de contratação", kind="select", req=True, options=["Pregão eletrônico", "Concorrência", "Dispensa", "Inexigibilidade"]),
        field("Prazo de divulgação no PNCP", "20 dias úteis", ro=True, nature="Legal", ref="Lei nº 14.133/2021, art. 94", help="Licitação: 20 dias úteis; contratação direta: 10."),
        field("Procedimento de origem", "Pregão eletrônico nº 022/2026"), field("Ata de registro de preços", "", placeholder="Quando aplicável"),
        field("Regime jurídico", kind="select", req=True, options=["Lei nº 14.133/2021", "Lei nº 8.666/1993 (contratos anteriores)"]),
    ))
    mo = section("Mão de obra e condicionantes", form_grid(
        field("Dedicação exclusiva de mão de obra", kind="radio", options=["*Sim", "Não", "Não informado"]),
        field("Predominância de mão de obra", kind="radio", options=["*Sim", "Não", "Não informado"]),
        field("Conta vinculada", kind="radio", options=["*Sim", "Não", "Não informado"]),
        field("Previsão de prorrogação no edital", kind="radio", options=["*Sim", "Não", "Não informado"]),
        field("Sistema estruturante de TI", kind="radio", options=["Sim", "*Não", "Não informado"]), min_=300),
        small("Habilitam repactuação, fiscal administrativo e conferência trabalhista mensal; condicionam tetos de vigência e a decisão “prorrogar”."))
    pz = section("Prazos contratuais (base da C22)", form_grid(
        field("Liquidação (dias)", "10", kind="number", nature="Contrato"), field("Pagamento (dias)", "30", kind="number", nature="Contrato"),
        field("Recebimento provisório (dias)", "15", kind="number", nature="Contrato"), field("Recebimento definitivo (dias)", "30", kind="number", nature="Contrato")),
        small("Lidos do contrato, sem valor padrão."))
    return passo(3, "Origem e regime", [form, mo, pz], ref="T03.01, blocos Origem e Regime jurídico")


@screen("T04-P4-Processos.dc.html", "T04 Passo 4 — Processos", "r04", "T04")
def p4():
    oi = origem("Integrado", "Conector SEI", "09/11/2026 15:20", "Consulta ao SEI · processo SEI-040014/000955/2026")
    form = section("Processos (aba T03.09)", form_grid(
        field("Processo principal — número SEI", "SEI-040014/000955/2026", req=True, origin=oi),
        field("Assunto (do SEI)", "Contratação de brigada de incêndio", ro=True, note="Consultado no SEI em 09/11/2026 15:20"),
        field("Unidade atual (do SEI)", "GERAD", ro=True),
        field("Processo de gestão e fiscalização", "", placeholder="SEI-040014/……/2026", help="Um por contrato; relacionado ao principal (art. 22, I e III).")),
        btn("Buscar no SEI", ico="plug", small_=True),
        table(["Número SEI", "Papel", "Assunto", ""], [["SEI-040014/000901/2026", "Relacionado", "Pesquisa de preços", a("Remover", "T04-P4-Processos.dc.html")]],
              caption="Processos relacionados", dense=True),
        alert("warn", "Pendência para validar", "Falta o processo de gestão e fiscalização. O rascunho pode ser salvo."))
    return passo(4, "Processos", [form], fonte="SEI", ref="T03.09, bloco Processos")


@screen("T04-P5-Responsaveis.dc.html", "T04 Passo 5 — Responsáveis", "r04", "T04")
def p5():
    ato = section("Ato de designação", form_grid(
        field("Número do ato", "PORT GERAD nº 131/2026", req=True), field("Data do ato", "24/11/2026", req=True, kind="date"),
        field("Autoridade", "Diretoria Administrativo-Financeira", req=True),
        field("Publicação no Diário Oficial", "", kind="date", placeholder="dd/mm/aaaa", help="Ou dispensa justificada; publicação não anterior ao ato."),
        field("Comissão", kind="radio", options=["Sim", "*Não"]), field("Processo · documento", "SEI-040014/000955/2026 · doc. 48010022")))
    des = section("Designações", table(["Pessoa", "Papel", "Titularidade", "Início", "Termo de Ciência", "Declaração de ausência de impedimento"],
                                       [["E. Campos (efetivo)", "Gestor", "Titular", "01/12/2026", "25/11/2026", "Assinada"],
                                        ["B. Lopes (efetivo)", "Fiscal técnico", "Titular", "01/12/2026", "25/11/2026", "Assinada"],
                                        ["K. Melo (efetivo)", "Fiscal administrativo", "Titular", "01/12/2026", span("Não informado", style="color:#FFC489;"), "Assinada"],
                                        ["O. Reis (efetivo)", "Gestor", "Suplente", "01/12/2026", "25/11/2026", "Assinada"]], dense=True),
                  btn("Adicionar designação", ico="plus", small_=True),
                  alert("warn", "Composição mínima conferida (C20) — não impede o rascunho",
                        "Titulares completos. Suplentes exigidos: 2 (1 de gestor + 1 para cada 2 fiscais); existentes: 1. 1 Termo de Ciência não informado."),
                  small("Designação exige ato. Importação pelo leiaute L03 disponível."))
    return passo(5, "Responsáveis", [ato, des], fonte=None, leiaute="L03", ref="T03.08")


@screen("T04-P6-Prazos.dc.html", "T04 Passo 6 — Prazos", "r04", "T04")
def p6():
    form = section("Vigência (aba T03.02)", form_grid(
        field("Data de assinatura", "", kind="date", placeholder="dd/mm/aaaa", note="Preenchida na formalização do instrumento assinado."),
        field("Início da vigência", "01/12/2026", req=True, kind="date"), field("Término da vigência", "30/11/2027", req=True, kind="date", note="Término ≥ início."),
        field("Prazo de execução", "12 meses")),
        alert("info", "Teto legal de vigência", "Serviço contínuo: até 5 anos, prorrogável até 10 anos se previsto no edital (Lei nº 14.133/2021, arts. 106 e 107). Período informado: 12 meses."))
    dec = section("Decisão prevista e data interna (C15)", form_grid(
        field("Decisão prevista", kind="select", options=["Prorrogar", "Substituir", "Encerrar", "Analisar"]),
        field("Data interna de início das providências", "02/08/2027", ro=True, nature="Parâmetro interno", ref="Antecedência de 120 dias para prorrogar (piso regulamentar)",
              help="Término − antecedência."),
        field("Fixar manualmente", kind="checkbox", options=["Fixar data interna manualmente (exige justificativa)"]),
        field("Justificativa da fixação manual", "", kind="textarea", placeholder="Obrigatória quando fixada manualmente")),
        alert("warn", "Piso regulamentar", "Para prorrogar, substituir ou analisar, a antecedência não pode ser inferior a 120 dias (Decreto RJ nº 48.817/2023, art. 22, XVII). "
              "Uma tentativa de fixar 60 dias é recusada (CV07)."),
        kv([("Marcos regulamentares previstos (C19)", "M120 em 02/08/2027 · M30 em 31/10/2027")]))
    return passo(6, "Prazos", [form, dec], ref="T03.02")


@screen("T04-P7-Composicao.dc.html", "T04 Passo 7 — Composição financeira", "r04", "T04")
def p7():
    form = section("Campos por modalidade — serviço contínuo (tabela 6.4)", form_grid(
        field("Valor global informado", "462.000,00", req=True, kind="money"), field("Valor mensal informado", "38.500,00", kind="money",
                                                                                     note="Informado a partir do instrumento; não é calculado por divisão."),
        field("Periodicidade", kind="select", req=True, options=["Mensal", "Bimestral", "Trimestral"]),
        field("Data-base de reajuste (data do orçamento estimado)", "09/2026", req=True),
        field("Repactuação aplicável (mão de obra)", kind="radio", options=["*Sim", "Não"]),
        field("Dedicação exclusiva de mão de obra", "Sim (passo 3)", ro=True)))
    itens = section("Itens de preço", table(["Nº", "Tipo", "Componente", "Descrição", "Unidade", ("Qtd.", "r"), ("Preço unitário", "r"), ("Valor mensal", "r"), ("Valor total", "r")],
                                            [["1", "Posto", "Mão de obra", "Brigadista diurno", "posto", "4", "6.200,00", "24.800,00", "297.600,00"],
                                             ["2", "Posto", "Mão de obra", "Brigadista noturno", "posto", "2", "6.700,00", "13.400,00", "160.800,00"]],
                                            foot=["", "", "", "Total", "", "", "", "38.200,00", "458.400,00"], dense=True),
                    btn("Adicionar item", ico="plus", small_=True), btn("Colar em grade", small_=True), btn("Importar itens (L09)", href="Importacao.dc.html", small_=True),
                    alert("danger", "Composição não reconcilia com o valor informado",
                          "Itens somam R$ 38.200,00/mês (R$ 458.400,00) e o valor informado é R$ 38.500,00/mês (R$ 462.000,00): diferença de R$ 300,00/mês. "
                          "A divergência impede a validação; o rascunho pode ser salvo."))
    gar = section("Garantia (aba T03.07)", form_grid(
        field("Aplicável", kind="radio", req=True, options=["*Sim", "Não (exige justificativa)", "Não avaliado"]),
        field("Modalidade", kind="select", options=["Seguro-garantia", "Caução", "Fiança bancária", "Título de capitalização"]),
        field("Valor", "23.100,00", kind="money"), field("Percentual", "5,00%", help="Até 5%, ou até 10% com justificativa (arts. 96 a 99)."),
        field("Validade", "", placeholder="dd/mm/aaaa a dd/mm/aaaa", note="Em seguro-garantia, validade inferior à vigência gera alerta (art. 97)."),
        field("Cobertura de verbas trabalhistas", kind="radio", options=["*Sim", "Não", "Não informado"])))
    return passo(7, "Composição financeira", [form, itens, gar], fonte=None, leiaute="L09", ref="T03.03 e T03.07")


@screen("T04-Revisao.dc.html", "T04 Revisão — submeter, validar ou devolver", "r04", "T04")
def revisao():
    rows = [["1 Identificação", estado("Validado", "green"), "—", "Digitado (vinculado ao registro importado)", a("Abrir", "T04-P1-Identificacao.dc.html")],
            ["2 Contratada", badge("Completo", "green"), "—", "Digitado; contratada reutilizada", a("Abrir", "T04-P2-Contratada.dc.html")],
            ["3 Origem e regime", badge("Completo", "green"), "—", "Digitado", a("Abrir", "T04-P3-Origem.dc.html")],
            ["4 Processos", badge("Incompleto", "orange"), "Processo de gestão e fiscalização", "Integrado (SEI)", a("Abrir", "T04-P4-Processos.dc.html")],
            ["5 Responsáveis", badge("Completo com apontamentos", "yellow"), "1 Termo de Ciência; 1 suplente de fiscal (C20 — não bloqueia)", "Digitado", a("Abrir", "T04-P5-Responsaveis.dc.html")],
            ["6 Prazos", badge("Incompleto", "orange"), "Data de assinatura (na formalização)", "Digitado", a("Abrir", "T04-P6-Prazos.dc.html")],
            ["7 Composição financeira", badge("Divergente", "red"), "Itens não reconciliam (diferença de R$ 300,00/mês)", "Digitado", a("Abrir", "T04-P7-Composicao.dc.html")]]
    return page("T04 Cadastro e edição — revisão", "carteira",
                [("Carteira", "Carteira.dc.html"), ("Rascunhos", "T02C-Rascunhos.dc.html"), "063/2026", "Revisão"],
                [rascunho_box(), stepper(T04_STEPS, 8),
                 section("Resumo de todos os passos", table(["Passo", "Situação", "Campos faltantes", "Fonte do grupo", ""], rows, dense=True)),
                 error_summary([("Processo de gestão e fiscalização (passo 4)", "T04-P4-Processos.dc.html"),
                                ("Composição financeira divergente (passo 7)", "T04-P7-Composicao.dc.html"),
                                ("Instrumento assinado não anexado", "T0401-Formalizacao.dc.html")]),
                 grid(section("Submeter", p("Lista o que falta sem apagar o que foi digitado. Rascunho não alimenta totais (MIG08)."),
                              btn("Submeter à validação", kind="primary"), h=3),
                      section("Validar (coordenador)", p("Exige instrumento assinado anexado e fonte de cada grupo. Lançado por R. Costa; validação por M. Silva permitida."),
                              btn("Validar", kind="primary", disabled=True, title="Faltam instrumento assinado e saneamento das pendências"),
                              small("Bloqueado: instrumento assinado não anexado; composição divergente."), h=3),
                      section("Devolver com motivo", field("Motivo", "Corrigir composição de itens (diferença de R$ 300,00/mês) e informar processo de gestão.", req=True, kind="textarea"),
                              field("Prazo de saneamento", "17/11/2026", req=True, kind="date"), btn("Devolver com motivo"), h=3), min_=300),
                 form_actions(submit=False, note="Segregação: o operador contratual não valida o próprio lançamento (CP03). Exceções registram autorizador e motivo.")],
                h1="T04 Cadastro e edição do contrato", sub="Revisão — resumo de todos os passos, com campos faltantes, fonte de cada grupo e situação de validação.")


@screen("T0401-Formalizacao.dc.html", "T04.01 Revisão e formalização de evento", "r04", "T04.01")
def t0401():
    campos = section("Instrumento", form_grid(
        field("Tipo de instrumento", kind="select", req=True, options=["Termo aditivo", "Contrato", "Apostila", "Termo de extinção"],
              nature="Legal", ref="Lei nº 14.133/2021, art. 136", help="Apostila só para reajuste, repactuação e demais hipóteses do art. 136."),
        field("Número", "2º TA", req=True, note="Único por contrato e tipo."), field("Data de assinatura", "", req=True, kind="date", placeholder="dd/mm/aaaa"),
        field("Documento assinado", "", req=True, placeholder="Anexar arquivo ou referência SEI", error="Obrigatório para formalizar — minuta não altera a vigência (CV02)."),
        field("Processo SEI", "SEI-040014/000512/2026", req=True),
        field("Classe(s) de alteração", kind="checkbox", req=True, options=["*Prorrogação", "Acréscimo", "Supressão", "Reajuste", "Repactuação", "Revisão do equilíbrio", "Outra"],
              note="Cada classe gera um evento próprio; a mesma classe não se repete no mesmo instrumento."),
        field("Justificativa resumida e fundamento", "Prorrogação por 12 meses — vantajosidade demonstrada (Lei nº 14.133/2021, art. 107).", req=True, kind="textarea"),
        field("Valor anterior (vigência corrente)", "1.074.400,00", ro=True, kind="money", note="Vem da versão vigente V2."),
        field("Variação", "+1.101.600,00", kind="money"), field("Valor resultante (nova vigência)", "1.101.600,00", ro=True, kind="money", note="12 × R$ 91.800,00"),
        field("Término anterior", "28/11/2026", ro=True), field("Novo término", "28/11/2027", req=True, note="Posterior ao anterior."),
        field("Início dos efeitos", "29/11/2026", req=True, kind="date", note="Retroativo calcula diferenças por competência (C12)."),
        field("Publicação do extrato", "", kind="date", placeholder="dd/mm/aaaa", note="Opcional no registro; ausência gera pendência."),
        field("Divulgação no PNCP (data e nº de controle)", "", placeholder="Enquanto vazio: “formalizado — divulgação pendente”", help="Contador em dias úteis (C01)."),
        field("Remessa ao TCE-RJ", kind="radio", options=["Sim", "Não", "*Não informado"], nature="Legal", ref="Decreto RJ nº 48.817/2023, art. 22, II; hipóteses a validar"),
    ))
    comp = section("Comparação antes e depois",
                   table(["Aspecto", "Antes (V2)", "Depois (V3 proposta)"],
                         [["Vigência", "29/11/2025 a 28/11/2026", "29/11/2026 a 28/11/2027"],
                          ["Valor — vigência corrente", "1.074.400,00", "1.101.600,00"],
                          ["Valor — global acumulado", "1.074.400,00", "2.176.000,00"],
                          ["Valor — base do art. 125", "1.020.000,00", "1.020.000,00 (inalterada por esta alteração)"],
                          ["Itens de preço", "5 itens · R$ 91.800,00/mês", "5 itens · R$ 91.800,00/mês"],
                          ["Limite do art. 125 consumido / restante", "5,33% / 19,67%", "5,33% / 19,67%"]], dense=True),
                   small("Alerta fundamentado se o acréscimo acumulado superar o limite legal."))
    verif = section("Verificações prévias",
                    table(["Verificação", "Resultado", "Natureza"],
                          [["Pedido de reequilíbrio pendente (art. 131)", badge("Não há", "green"), prazo_nat("Legal")],
                           ["Garantia que exigirá endosso", span("Sim — validade 30/12/2026 inferior à nova vigência (art. 97)", style="color:#FFC489;"), prazo_nat("Legal")],
                           ["Lista de verificação da prorrogação", span("10 de 12 atendidos (PR08 e PR11 pendentes)", style="color:#FFC489;"), prazo_nat("Legal regulamentar")],
                           ["Marcos M120 e M30", cat(marco("Cumprido"), " ", marco("Cumprido com atraso")), prazo_nat("Legal regulamentar")]], dense=True),
                    field("Justificativa para prosseguir com pendências legais", "", kind="textarea", req=True, placeholder="Exigida para PR08, PR11 e M30 com atraso"),
                    tone="warn")
    imp = section("Impacto",
                  table(["Efeito", "Detalhe"],
                        [["Projeções a recalcular", "Projeção operacional v3 → v4 (12/2026 a 11/2027)"],
                         ["Avisos futuros a cancelar", "N01 de 28/11/2026 (antecedência de 30 dias já emitida é preservada); N15 da vigência atual"],
                         ["Avisos a gerar", "N01 para 28/11/2027 (180/120/90/60/30 dias); N11 após o registro validado; N09 (garantia)"],
                         ["Diferenças retroativas previstas", "Nenhuma (efeitos a partir de 29/11/2026)"]], dense=True),
                  alert("info", "Confirmação única", "Aplica instrumento, alteração, nova versão e recálculo na mesma transação. Duplo clique ou repetição não duplica o efeito (CH03)."))
    conf = section("Confirmação",
                   actions(btn("Confirmar formalização", kind="primary", disabled=True, title="Anexe o documento assinado e justifique as pendências legais"),
                           btn("Salvar rascunho", ico="file"), btn("Voltar ao procedimento", href="T06-D1-Resumo.dc.html")),
                   small("Bloqueado: falta o instrumento assinado. Depois de confirmar, o sistema mostra o resumo antes e depois e envia o aviso N11."))
    return page("T04.01 Revisão e formalização de evento", "carteira",
                [("Carteira", "Carteira.dc.html"), ("012/2025", "Ficha.dc.html"), "Formalização de evento"],
                [alert("info", "Acesso: coordenador", "Registrar o instrumento assinado (contrato, termo aditivo ou apostila) e aplicar seus efeitos uma única vez."),
                 campos, comp, verif, imp, conf],
                sub="Contrato 012/2025 · Alfa Serviços Prediais Ltda · 2º termo aditivo (prorrogação) — procedimento PRC-2026-014.",
                acts=[btn("Confirmar divulgação no PNCP (buscar na fonte)", href="T1407-Conectores.dc.html", ico="plug", small_=True)])
