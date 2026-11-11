"""T00 Acesso e sessão, T01 Início (abas A, B, C), padrões comuns e visões de celular (seção 12.6)."""
from shell import *
from data import C, CONTRATOS


def ctr_cell(n, ctda, extra=None, href="Ficha.dc.html"):
    return cat(a(n, href, style=f"color:{ACC};font-weight:600;text-decoration:underline;"), div(ctda, style=f"color:{TEXT2};font-size:12px;"),
               div(extra, style=f"color:{FAINT};font-size:12px;") if extra else None)


def dias_txt(n):
    if n < 0:
        return span(f"{-n} dias de atraso", style="color:#FFB3B8;font-weight:600;")
    return span(f"em {n} dias")


def globais():
    return filterbar(fsel("Unidade", "Todas as autorizadas", "GERAD", "GERTIC", "DIRAF", "DIRSE", "CHEGAB"),
                     fsel("Responsável", "Todos", "P. Nunes", "A. Lima", "T. Vieira", "L. Martins", "C. Ramos"),
                     fsel("Contratada", "Todas", "Alfa Serviços Prediais Ltda", "Gama Vigilância Ltda", "Beta Tecnologia S.A."),
                     fsel("Categoria", "Todas", "Serviços prediais", "Tecnologia da informação", "Comunicação", "Suprimentos"),
                     fsel("Exercício", "2026", "2027", "2025"),
                     fsel("Situação", "Vigentes e com pendência", "Em vigor", "Encerrados", "Todas"),
                     saved=("Minha carteira — GERAD", "Somente Crítica e Alta"))


# ======================================================================= T00
@screen("T00-Acesso.dc.html", "T00 Acesso — entrada", "r01", "T00")
def t00_acesso():
    card = div(
        div("RIOPREVIDÊNCIA", style=f"font-size:12px;letter-spacing:.1em;color:{FAINT};font-weight:700;"),
        tag("h1", "Controle de Contratos", style=f"margin:4px 0 0;font-size:28px;font-weight:700;color:{TEXT};"),
        p("Autenticação institucional pelo provedor de identidade do Estado. Não há cadastro de senha neste sistema."),
        btn("Entrar com a conta institucional", href="T00-Unidade.dc.html", kind="primary", ico="lock"),
        alert("danger", "Não foi possível concluir a autenticação",
              "Tente novamente ou procure o suporte de tecnologia. (Mensagem genérica: não informa se a conta existe.)"),
        section("Aviso de privacidade", p("Finalidade do tratamento: gestão e controle dos contratos administrativos do Rioprevidência "
                                          "(Lei nº 14.133/2021 e Decreto RJ nº 48.817/2023). Dados pessoais de servidores são minimizados e "
                                          "identificadores funcionais ficam mascarados por padrão."),
                p(cat("Encarregado pelo tratamento de dados pessoais: ", strong("[NOME E CONTATO DO ENCARREGADO — a definir pela instituição]"))),
                small("Tentativas de acesso negadas são registradas na trilha de auditoria."), h=2),
        style=f"width:100%;max-width:520px;box-sizing:border-box;display:flex;flex-direction:column;gap:18px;padding:32px;background:{SURF};border:1px solid {LINE};border-radius:12px;")
    return standalone("T00 Acesso e sessão", [div(card, style="flex:1;display:flex;align-items:center;justify-content:center;padding:48px 16px;"),
                                              footer()])


@screen("T00-Unidade.dc.html", "T00 Seleção de unidade", "r01", "T00")
def t00_unidade():
    def vinc(un, perfil, vig, href):
        return tag("li", tag("a", div(strong(un), small(perfil)), small(vig), icon("arrow"), href=href,
                             style=f"display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px;padding:10px 16px;background:{RAISED};border:1px solid {LINE2};border-radius:8px;text-decoration:none;color:{TEXT};"))
    card = div(
        tag("h1", "Selecione a unidade ativa", style=f"margin:0;font-size:24px;font-weight:700;color:{TEXT};"),
        p("Unidades e perfis com vínculo vigente para M. Silva. A unidade ativa pode ser trocada depois no cabeçalho."),
        tag("ul", vinc("GERAD — Gerência Administrativa", "Coordenador", "Vigente desde 01/01/2026", "Main.dc.html"),
            vinc("DIRAF — Diretoria Administrativo-Financeira", "Consulta, auditoria e controle interno", "Vigente até 31/12/2026", "Main.dc.html"),
            style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px;"),
        section("Estado: sem vínculo vigente", alert("warn", "Sem permissão",
                                                     "Você não possui vínculo vigente com nenhuma unidade. Solicite acesso ao coordenador da sua unidade "
                                                     "ou ao administrador técnico. Nenhum dado da carteira é exibido."), tone="warn"),
        style=f"width:100%;max-width:560px;box-sizing:border-box;display:flex;flex-direction:column;gap:18px;padding:32px;background:{SURF};border:1px solid {LINE};border-radius:12px;")
    return standalone("T00 Seleção de unidade", [div(card, style="flex:1;display:flex;align-items:center;justify-content:center;padding:48px 16px;"), footer()])


@screen("T00-Sessao.dc.html", "T00 Sessão expirada", "r01", "T00")
def t00_sessao():
    fundo = col(stepper(T04_STEPS, 6),
                section("Passo 6 — Prazos (rascunho 063/2026)",
                        form_grid(field("Início da vigência", "01/12/2026", req=True, kind="date"),
                                  field("Término da vigência", "30/11/2027", req=True, kind="date"))),
                style="opacity:.35;pointer-events:none;", gap=16)
    dialog = div(
        row(icon("lock", 22, "#F5DA7A"), tag("h2", "Sua sessão expirou", style=f"margin:0;font-size:20px;color:{TEXT};"), gap=10),
        p("A gravação está bloqueada até nova autenticação. O que foi digitado em “Cadastro do contrato 063/2026 — passo 6 Prazos” "
          "foi preservado e será recuperado após autenticar, sem repetir a operação."),
        actions(btn("Autenticar novamente", href="T04-P6-Prazos.dc.html", kind="primary"), btn("Sair", href="T00-Acesso.dc.html")),
        small("A tentativa de gravação com sessão expirada foi registrada na auditoria."),
        role="dialog", aria_modal="true", aria_label="Sessão expirada",
        style=f"position:absolute;left:50%;top:120px;transform:translateX(-50%);width:min(520px,92%);box-sizing:border-box;padding:24px;background:{SURF};border:1px solid {LINE2};border-radius:12px;display:flex;flex-direction:column;gap:14px;box-shadow:0 24px 64px rgba(0,0,0,.6);")
    body = [div(fundo, dialog, style="position:relative;min-height:520px;")]
    return page("T00 Sessão expirada (aviso sobreposto)", "carteira", [("Carteira", "Carteira.dc.html"), "Cadastro", "Sessão expirada"], body,
                sub="Aviso sobreposto à tela em uso; rascunho autorizado recuperado após nova autenticação.")


# ======================================================================= T01
ACAO = [
    ("Crítica", None, "Risco Existente: término 05/11/2026 ultrapassado há 5 dias sem nova vigência, sucessor ou encerramento decidido (C18, ordem 6); D < 0 no conjunto 2026",
     "027/2024", "Gama Vigilância Ltda", "Concluir instrução da prorrogação ou instruir contratação emergencial", "P. Nunes", "07/11/2026", -3, "Existente"),
    ("Alta", "Média", "Risco Moderado — escopo em prorrogação automática (art. 111 da Lei nº 14.133/2021); término há 11 dias",
     "038/2024", "Kapa Construções Ltda", "Avaliar mora ou extinção (objeto não concluído)", "P. Nunes", "25/11/2026", 15, "Moderado — escopo em prorrogação automática"),
    ("Alta", None, "Risco Alto: 18 dias restantes sem procedimento em etapa igual ou posterior a “autorização”; até 60 dias sem nova vigência formalizada",
     "012/2025", "Alfa Serviços Prediais Ltda", "Obter parecer jurídico e autorização da prorrogação (PRC-2026-014)", "P. Nunes", "20/11/2026", 10, "Alto"),
    ("Alta", None, "Piso pelo risco Alto do contrato; garantia a vencer em até 60 dias (30/12/2026) e endosso exigido após o 1º termo aditivo",
     "012/2025", "Alfa Serviços Prediais Ltda", "Solicitar endosso do seguro-garantia", "J. Prado", "24/11/2026", 14, "Alto"),
    ("Alta", None, "Risco Alto: 73 dias restantes, procedimento na etapa 2; marco M120 descumprido em 24/09/2026 (C19)",
     "047/2024", "Nu Telecom S.A.", "Cobrar manifestação da contratada e registrar recomendação do gestor", "A. Lima", "18/11/2026", 8, "Alto"),
    ("Alta", None, "Marco M120 descumprido em 21/10/2026 (C19); início da contratação substituta desconhecido",
     "033/2025", "Mu Comunicação Ltda", "Levantar início estimado da contratação substituta", "T. Vieira", "31/10/2026", -10, "Moderado"),
    ("Alta", None, "Lacuna de continuidade C02 = 14 dias (término 31/03/2027; substituta prevista para 15/04/2027)",
     "031/2023", "Beta Tecnologia S.A.", "Revisar cronograma da contratação substituta", "A. Lima", "30/11/2026", 20, "Alto"),
    ("Alta", None, "Data de insuficiência (C10) em 01/12/2026, em até 60 dias; reforço estimado R = 10.000,00 (C09)",
     "044/2023", "Épsilon Elevadores Ltda", "Solicitar reforço de empenho de R$ 10.000,00", "L. Martins", "20/11/2026", 10, "Sem risco identificado"),
    ("Alta", None, "Designação incompleta há 101 dias — prazo do art. 7º, § 11, do Decreto RJ nº 48.817/2023 excedido (C20)",
     "041/2026", "Lambda Software Ltda", "Publicar ato de designação de gestor e fiscal", "M. Silva", "13/11/2026", 3, "Indeterminado"),
    ("Média", None, "Pedido de repactuação sem movimentação há 52 dias (limiar de 30 dias — parâmetro interno)",
     "019/2025", "Delta Copeiragem Ltda", "Analisar planilha de custos da repactuação (CCT 2026)", "C. Ramos", "18/11/2026", 8, "Sem risco identificado"),
    ("A confirmar", None, "Decisão prevista não informada; cadastro importado não validado",
     "021/2025", "Eta Transportes Ltda", "Registrar decisão prevista e validar o cadastro", "T. Vieira", "30/11/2026", 20, "Indeterminado"),
    ("Planejamento", None, "Encerramento decidido e vigência expirada; acompanhamento apenas da pendência financeira",
     "015/2022", "Teta Limpeza e Conservação Ltda", "Pagar saldo liquidado de R$ 2.000,00 e instruir o termo de encerramento", "L. Martins", "25/11/2026", 15,
     "Não aplicável — vigência encerrada"),
]
AJUSTE = "ajustada por M. Silva em 09/11/2026 — “mora da contratada já notificada; risco ao acervo durante a obra”"


def acao_rows(items, coordenador=True):
    rows = []
    for pr, sug, motivo, n, ctda, prov, resp, prazo, dias, rk in items:
        pcell = col(prio(pr), small(f"Sugerida: {sug} · {AJUSTE}") if sug
                    else small("Sugerida = confirmada" if pr not in ("A confirmar",) else "Aguarda saneamento"), gap=4)
        rows.append([pcell, span(motivo, style=f"color:{TEXT2};font-size:12px;"), ctr_cell(n, ctda),
                     a(prov, "T11B-Todas.dc.html", style=f"color:{TEXT};text-decoration:underline;"),
                     resp, cat(div(prazo), small(dias_txt(dias)) if dias >= 0 else dias_txt(dias)), risco(rk),
                     col(a("Atribuir responsável", "T11B-Todas.dc.html"),
                         a("Confirmar ou ajustar prioridade", "T11B-Todas.dc.html") if coordenador else None, gap=6,
                         style="font-size:12px;min-width:120px;")])
    return rows


@screen("Main.dc.html", "T01.A Início — Ação agora", "r01", "T01.A")
def t01a():
    lista = section("Ação agora",
                    table(["Prioridade (C17)", "Motivo da prioridade", "Contrato (abrir ficha)", "Providência (abrir)", "Responsável", "Prazo", "Risco (C18)", "Ações"],
                          acao_rows(ACAO), dense=True),
                    small("Ordenação: prioridade confirmada; desempate por menor número de dias restantes, maior criticidade do objeto e mais tempo sem "
                          "movimentação. A sugestão original permanece visível após o ajuste pelo coordenador."),
                    sub="12 providências · 1 Crítica · 8 Altas · 1 Média · 1 A confirmar · 1 Planejamento",
                    act=btn("Ver todas as providências (18 abertas)", href="T11B-Todas.dc.html", small_=True))
    conf = section("Conformidade da gestão e fiscalização",
                   grid(div(stat("Contratos com designação incompleta (C20)", "2", "041/2026 (101 dias — prazo do art. 7º, § 11, excedido) · 021/2025 Eta (40 dias)", "orange"),
                            a("Abrir lista (carteira filtrada por designação incompleta)", "Carteira.dc.html"), style="display:flex;flex-direction:column;gap:8px;"),
                        div(stat("Marcos regulamentares descumpridos (C19)", "3", "027/2024 (M30) · 033/2025 (M120) · 047/2024 (M120)", "red"),
                            a("Abrir marcos regulamentares (T05.D)", "T05D-Marcos.dc.html"), style="display:flex;flex-direction:column;gap:8px;"), min_=320),
                   sub="Faixa complementar — indicadores, não bloqueios.")
    return page("T01 Início — o que exige ação agora", "inicio", ["Início", "A Ação agora"],
                [globais(), lista, conf, small(f"Posição {POSICAO_TXT} 07:00 (Brasília) · gestor e fiscal veem apenas os contratos em que são designados.")],
                tabs_=tabs(T01_TABS, "A Ação agora"), sub="O que precisa de ação e a situação da carteira. Filtros globais valem para as três abas.")


def kpi(title, value, natureza, linhas, cobertura, href, link_txt, extra=None, formula=None):
    return div(
        row(span(title, style=f"font-size:14px;font-weight:600;color:{TEXT};"), nat(natureza) if natureza else None, justify="space-between"),
        div(value, style=f"font-size:30px;font-weight:700;color:{TEXT};line-height:1.1;"),
        extra,
        small(f"Posição {POSICAO_TXT} 07:00 · Cobertura: {cobertura}"),
        composicao(*linhas, cobertura=cobertura, formula=formula),
        a(link_txt, href, style=f"color:{ACC};font-size:13px;font-weight:600;"),
        style=f"display:flex;flex-direction:column;gap:8px;padding:16px;background:{SURF};border:1px solid {LINE};border-radius:8px;min-width:0;")


@screen("T01B-Indicadores.dc.html", "T01.B Indicadores da carteira", "r01", "T01.B")
def t01b():
    cards = grid(
        kpi("Contratos vigentes", "12", "Formalizado", [("Serviço contínuo", "10"), ("Fornecimento", "2"), ("Escopo", "0"),
                                                         ("Fora da contagem: 027/2024 (data final ultrapassada)", "1"),
                                                         ("Fora da contagem: 038/2024 (prorrogação automática — art. 111)", "1")],
            "14 de 14 contratos com término validado (incluídos 12; excluídos 2, listados)", "Carteira.dc.html", "Abrir lista (12 contratos · filtro Em vigor)"),
        kpi("Vencimentos por período", "14", "Formalizado", [("Ultrapassado", "2"), ("0–30 dias", "1"), ("31–60 dias", "2"), ("61–90 dias", "1"),
                                                            ("91–180 dias", "3"), ("Acima de 180 dias", "5")],
            "100% (faixas sem sobreposição)", "Vencimentos.dc.html", "Abrir lista por faixas (T05.A)",
            extra=small("Ultrapassado 2 · 0–30: 1 · 31–60: 2 · 61–90: 1 · 91–180: 3 · > 180: 5")),
        kpi("Comprometimento financeiro previsto", "R$ 1.824.150,00", "Projeção", [("11/2026", "1.055.700,00"), ("12/2026", "768.450,00"),
                                                                                    ("Exercício 2027", "6.928.600,00"), ("Não apurado (041/2026 sem projeção validada)", "fora do total")],
            "13 de 14 contratos (1 não apurado, fora do total — nunca zero)", "T01C-Financeiro.dc.html", "Abrir previsão mensal (T01.C)",
            extra=small("Restante do exercício 2026 (C13) · sem duplicar pendências"), formula="C13"),
        kpi("Empenhos insuficientes", "2", "Projeção", [("044/2023 — R (C09)", "10.000,00"), ("027/2024 — R (insuficiência existente)", "10.000,00"),
                                                        ("Dados incompletos (grupo separado)", "3 contratos")],
            "11 de 14 (3 em grupo separado: 019/2025, 031/2023, 041/2026)", "Empenhos.dc.html", "Abrir cobertura (T08.A)",
            extra=small("Reforço estimado total: R$ 20.000,00"), formula="C09"),
        kpi("Pagamentos pendentes", "R$ 105.000,00", "Execução registrada", [("Regularidade fiscal (1 documento)", "62.000,00"),
                                                                              ("Pagamento parcial — programação financeira (2)", "41.000,00"),
                                                                              ("Contrato encerrado com saldo (1)", "2.000,00"),
                                                                              ("Não liquidados (à parte): executado não liquidado", "338.400,00")],
            "100% das liquidações validadas", "T09D-Pagamentos.dc.html", "Abrir liquidado a pagar (T09.D)", extra=small("Liquidado a pagar por motivo (C11)"), formula="C11"),
        kpi("Prorrogações em andamento", "3", None, [("012/2025 — 5 dias sem avanço", "etapa 4"), ("027/2024 — 27 dias sem avanço", "etapa 3"),
                                                     ("047/2024 — 35 dias sem avanço", "etapa 2"), ("Substituições (fora da contagem)", "2")],
            "100% dos procedimentos registrados", "Prorrogacoes.dc.html", "Abrir procedimentos (T06.A)", extra=small("3 contratos distintos · maior tempo sem avanço: 35 dias")),
        kpi("Reajustes pendentes", "3", None, [("Repactuação — sem decisão (019/2025)", "1"), ("Repactuação — deferida, não implantada (021/2025 Zeta)", "1"),
                                               ("Reajuste por índice — em análise (044/2023)", "1"), ("Revisão do equilíbrio", "0")],
            "12 de 14 contratos com data-base informada", "Reajustes.dc.html", "Abrir pedidos (T10.A)", extra=small("Repactuação e revisão em filtros próprios")),
        kpi("Providências vencidas", "2", None, [("P. Nunes — 027/2024 (3 dias)", "1"), ("T. Vieira — 033/2025 (10 dias)", "1"), ("Abertas no total", "18")],
            "100% das providências", "T11C-PorResponsavel.dc.html", "Abrir por responsável (T11.C)", extra=small("de 18 abertas")),
        kpi("Risco de descontinuidade", "9", None, [("Existente", "1"), ("Alto", "3"), ("Moderado (inclui escopo em prorrogação automática e 025/2023)", "3"),
                                                    ("Indeterminado", "2"), ("Sem risco identificado / não aplicável (fora da contagem)", "5")],
            "14 de 14 contratos avaliados", "Vencimentos.dc.html", "Abrir contratos por nível de risco",
            extra=row(risco("Existente"), small("1"), risco("Alto"), small("3"), risco("Moderado"), small("3"), risco("Indeterminado"), small("2"), gap=6),
            formula="C18"),
        min_=300)
    prox = section("Próximos vencimentos", table(["Contrato", "Término formalizado", "Dias restantes", "Decisão prevista", "Risco"],
                                                 [[ctr_cell(c["n"], c["ctda"]), c["fim"], str(c["dias"]), c["dec"], risco(c["risco"])]
                                                  for c in sorted(CONTRATOS, key=lambda c: c["dias"]) if c["dias"] >= 0][:6]),
                   act=btn("Abrir vencimentos (T05)", href="Vencimentos.dc.html", small_=True))
    return page("T01 Início — indicadores da carteira", "inicio", [("Início", "Main.dc.html"), "B Indicadores da carteira"],
                [globais(), alert("info", "Leitura dos indicadores", "Clicar em um cartão abre a lista de origem com os mesmos filtros e a mesma quantidade de registros. "
                                  "Total parcial mostra os excluídos; lacuna nunca é somada como zero (seção 7.7)."), cards, prox],
                tabs_=tabs(T01_TABS, "B Indicadores da carteira"), sub="Nove indicadores da seção 7.7, cada um com valor, cobertura, posição e “Ver composição”.")


DESEMB = [("11/2026", 105000.00, 338400.00, 612300.00), ("12/2026", 0, 0, 768450.00), ("01/2027", 0, 0, 688200.00), ("02/2027", 0, 0, 676200.00),
          ("03/2027", 0, 0, 676200.00), ("04/2027", 0, 0, 546200.00), ("05/2027", 0, 0, 546200.00), ("06/2027", 0, 0, 535700.00),
          ("07/2027", 0, 0, 535700.00), ("08/2027", 0, 0, 512200.00), ("09/2027", 0, 0, 479200.00), ("10/2027", 0, 0, 479200.00),
          ("11/2027", 0, 0, 479200.00), ("12/2027", 0, 0, 774200.00)]


@screen("T01C-Financeiro.dc.html", "T01.C Painel financeiro", "r01", "T01.C")
def t01c():
    tot = [(m, l + o + f) for m, l, o, f in DESEMB]
    mx = max(v for _, v in tot)
    graf = section("Previsão mensal de desembolso — 2026 e 2027 (C13)",
                   row(nat("Execução registrada"), small("liquidado a pagar e executado não liquidado"), nat("Projeção"), small("execução futura prevista (F)"), gap=6),
                   bars([(m, v, money(v)) for m, v in tot], mx),
                   table(["Mês de desembolso", ("Liquidado a pagar", "r"), ("Executado não liquidado (O)", "r"), ("Execução futura prevista (F)", "r"), ("Total", "r")],
                         [[m, money(l) if l else "—", money(o) if o else "—", money(f), strong(money(l + o + f))] for m, l, o, f in DESEMB],
                         caption="Tabela equivalente ao gráfico (R$)",
                         foot=["Total", money(sum(r[1] for r in DESEMB)), money(sum(r[2] for r in DESEMB)), money(sum(r[3] for r in DESEMB)),
                               money(sum(v for _, v in tot))]),
                   small("Custo pela competência; desembolso pelo mês da data esperada de pagamento. Cada item pertence a uma única origem. "
                         "041/2026 sem projeção validada: “não apurado”, fora do total. Prorrogações em tramitação não entram na projeção."),
                   act=btn("Abrir valores e planejamento (T07.C)", href="T07C-Projecao.dc.html", small_=True))
    reforco = section("Contratos com reforço estimado (C09)",
                      table(["Contrato", "Conjunto orçamentário", ("D", "r"), ("F", "r"), ("R", "r"), "Data de insuficiência (C10)", ""],
                            [[ctr_cell("044/2023", "Épsilon Elevadores Ltda", href="Empenhos.dc.html"), "2026 · 3.3.90.39 · 100 · PT 2031", "40.000,00", "50.000,00",
                              strong("10.000,00"), "01/12/2026", a("Abrir T08", "Empenhos.dc.html")],
                             [ctr_cell("027/2024", "Gama Vigilância Ltda", href="Empenhos.dc.html"), "2026 · 3.3.90.37 · 100 · PT 2031", span("−10.000,00", style="color:#FFB3B8;"),
                              "0,00", strong("10.000,00"), badge("Insuficiência existente", "red"), a("Abrir T08", "Empenhos.dc.html")]]),
                      sub="Natureza: Projeção · R = máx(0, F − D)")
    lap = section("Liquidado a pagar por motivo (C11)",
                  table(["Motivo", ("Documentos", "r"), ("Valor", "r"), "Contratos", ""],
                        [["Regularidade fiscal", "1", "62.000,00", "019/2025", a("Abrir T09", "T09D-Pagamentos.dc.html")],
                         ["Pagamento parcial — programação financeira", "2", "41.000,00", "031/2023, 044/2023", a("Abrir T09", "T09D-Pagamentos.dc.html")],
                         ["Contrato encerrado com saldo", "1", "2.000,00", "015/2022", a("Abrir T09", "T09D-Pagamentos.dc.html")]],
                        foot=["Total", "4", "105.000,00", "", ""]),
                  small("Pendente de liquidação (executado não liquidado: R$ 338.400,00) e impedimentos são exibidos separadamente."),
                  sub="Natureza: Execução registrada")
    nc = section("Empenhos com cobertura não conclusiva",
                 table(["Contrato", "Motivo", "Efeito", ""],
                       [[ctr_cell("019/2025", "Delta Copeiragem Ltda"), "Obrigação de 09/2026 (R$ 3.000,00) sem alocação orçamentária", "“Cobertura não confirmada — há obrigações sem alocação”", a("Abrir T09.A", "Pagamentos.dc.html")],
                        [ctr_cell("031/2023", "Beta Tecnologia S.A."), "Movimento não classificado na origem (nota 2026NE00031)", "E “indeterminado” até saneamento", a("Abrir T08.B", "T08B-Notas.dc.html")],
                        [ctr_cell("041/2026", "Lambda Software Ltda"), "Nenhuma nota de empenho registrada", "Empenho “não apurado”, nunca zero", a("Abrir T08.A", "Empenhos.dc.html")]]))
    return page("T01 Início — painel financeiro", "inicio", [("Início", "Main.dc.html"), "C Painel financeiro"],
                [globais(), graf, grid(reforco, lap, min_=520), nc], tabs_=tabs(T01_TABS, "C Painel financeiro"),
                sub="Previsão de desembolso, reforços estimados, liquidado a pagar e cobertura não conclusiva. Cada linha abre T07, T08 ou T09 no contrato.")


# ======================================================================= Padrões comuns (seção 12.1)
@screen("Padroes.dc.html", "Padrões comuns e estados obrigatórios", "r10", "12.1")
def padroes():
    estados = grid(
        section("Carregando", row(icon("clock", 18, MUTED), p("Carregando contratos da unidade GERAD…"), gap=8),
                div(style=f"height:12px;background:{RAISED};border-radius:4px;"), div(style=f"height:12px;width:70%;background:{RAISED};border-radius:4px;"),
                h=3),
        section("Lista vazia", p("Nenhuma providência sob sua responsabilidade."), btn("Nova providência", kind="primary", small_=True), h=3),
        section("Sem resultados", p("Nenhum contrato corresponde à busca “Lambda 2025” com os filtros aplicados."), btn("Limpar filtros", small_=True), h=3),
        section("Dados incompletos", alert("warn", "Total parcial", "Subtotal conhecido R$ 1.824.150,00 · 13 contratos incluídos · 1 excluído (041/2026 sem projeção). Lacuna não é somada como zero."), h=3),
        section("Erro de consulta", alert("danger", "Não foi possível consultar os saldos de empenho", "Os valores não são exibidos como zero. Tente novamente; o erro foi registrado (CI03)."),
                btn("Tentar novamente", small_=True), h=3),
        section("Sessão expirada", p("Aviso sobreposto bloqueia a gravação; o rascunho é recuperado após nova autenticação."),
                a("Ver exemplo (T00 — sessão expirada)", "T00-Sessao.dc.html"), h=3),
        section("Sem permissão", alert("warn", "Acesso negado", "Este contrato não pertence às unidades do seu vínculo nem às suas designações. A tentativa foi registrada na auditoria (CP01)."), h=3),
        min_=300)
    conflito = section("Conflito de versão (CH04)",
                       alert("warn", "Outro usuário gravou este registro enquanto você editava", "Compare as duas versões e escolha como prosseguir; nada foi perdido."),
                       grid(section("Sua versão (não gravada)", kv([("Objeto resumido", "Manutenção predial preventiva, corretiva e emergencial"), ("Editado por", "R. Costa · 10/11/2026 09:12")]), h=3),
                            section("Versão gravada (v7)", kv([("Objeto resumido", "Manutenção predial preventiva e corretiva"), ("Gravado por", "M. Silva · 10/11/2026 09:10")]), h=3), min_=300),
                       actions(btn("Manter a versão gravada"), btn("Aplicar minha versão como nova correção (com motivo)", kind="primary")))
    selos = section("Rótulos fixos (seção 12.1)",
                    kv([("Natureza do valor", row(nat("Formalizado"), nat("Execução registrada"), nat("Projeção"), nat("Cenário simulado"), gap=6)),
                        ("Qualidade", row(qual("Validado"), qual("Importado – não validado"), qual("Não informado"), qual("Não apurado"), gap=6)),
                        ("Prioridade sugerida", row(*[prio(x_) for x_ in ("Crítica", "Alta", "Média", "Planejamento", "A confirmar")], gap=6)),
                        ("Risco", row(*[risco(x_) for x_ in ("Existente", "Alto", "Moderado", "Moderado — escopo em prorrogação automática", "Indeterminado",
                                                            "Sem risco identificado", "Não aplicável — vigência encerrada", "Não aplicável — encerramento planejado")], gap=6)),
                        ("Marco regulamentar", row(*[marco(x_) for x_ in ("A cumprir", "Cumprido", "Cumprido com atraso", "Descumprido", "Não aplicável")], gap=6)),
                        ("Designação", row(desig("Completa"), desig("Incompleta"), desig("Sem designação há 101 dias"), gap=6)),
                        ("Natureza do prazo", row(prazo_nat("Legal"), prazo_nat("Legal regulamentar"), prazo_nat("Contrato"), prazo_nat("Parâmetro interno"), gap=6)),
                        ("Modo de entrada (selo de origem)", row(origem("Digitado"), origem("Importado", "lote 2026-11-03 (R. Costa)", "03/11/2026 14:02"),
                                                                 origem("Integrado", "Conector PNCP", "09/11/2026 03:00"), gap=10))], min_=420))
    form = section("Formulário — padrões",
                   error_summary([("Término da vigência: deve ser igual ou posterior ao início", "T04-P6-Prazos.dc.html"),
                                  ("CNPJ: dígito verificador incorreto", "T04-P2-Contratada.dc.html")]),
                   form_grid(field("CNPJ", "12.345.678/0001-96", req=True, error="Dígito verificador incorreto. Aceita também o formato alfanumérico.",
                                   origin=origem("Importado", "lote 2026-11-03", "03/11/2026 14:02")),
                             field("Prazo de divulgação no PNCP", "20 dias úteis", ro=True, nature="Legal", ref="Lei nº 14.133/2021, art. 94",
                                   help="Definido pela modalidade (20 ou 10 dias úteis)."),
                             field("Antecedência para iniciar a prorrogação", "120 dias", ro=True, nature="Parâmetro interno",
                                   ref="Piso: Decreto RJ nº 48.817/2023, art. 22, XVII", help="Não pode ser inferior a 120 dias.")),
                   form_actions(validar=True, devolver=True))
    hist = section("Modo de consulta histórica", hist_band(), small("Ativado por “Consultar em outra data” no cabeçalho ou pelo seletor “Situação em uma data” da ficha."),
                   a("Ver exemplo na ficha (CH01)", "T03-Historico.dc.html"))
    resp = section("Acessibilidade e responsividade (RNF05 e RNF11)",
                   p("Computador em 1366 × 768 e 1920 × 1080; tablet em 768 px; celular em 360 e 390 px; alvos de toque de 44 × 44 px; estado sempre "
                     "indicado por texto além da cor; no celular, cartões e campos em coluna, sem rolagem horizontal da página; todo gráfico tem tabela equivalente."),
                   a("Ver visões de celular (seção 12.6)", "Celular.dc.html"))
    return page("Padrões comuns e estados obrigatórios", "inicio", [("Início", "Main.dc.html"), "Padrões e estados"],
                [section("Estados obrigatórios", estados, sub="Carregando, lista vazia, sem resultados, dados incompletos, erro de consulta, sem permissão e conflito de versão."),
                 conflito, selos, form, hist, resp],
                sub="Referência da seção 12.1 aplicada a todas as telas do protótipo.")


# ======================================================================= Celular (seção 12.6)
def mcard(*c, tone=None):
    bd = {"red": "#6B2128", "orange": "#6B4219"}.get(tone, LINE)
    return div(*c, style=f"display:flex;flex-direction:column;gap:8px;padding:14px;background:{SURF};border:1px solid {bd};border-radius:10px;")


@screen("Celular.dc.html", "Celular — Ação agora", "r10", "12.6", mobile=True)
def cel_acao():
    ind = div(*[div(div(t_, style=f"font-size:12px;color:{MUTED};"), div(v, style=f"font-size:22px;font-weight:700;color:{TEXT};"),
                    style=f"padding:12px;background:{SURF};border:1px solid {LINE};border-radius:10px;")
                for t_, v in [("Contratos vigentes", "12"), ("Vencem em 30 dias", "1"), ("Risco Existente ou Alto", "4"), ("Providências vencidas", "2")]],
              style="display:grid;grid-template-columns:1fr 1fr;gap:10px;")
    cards = []
    for it in ACAO[:5]:
        pr, sug, motivo, n, ctda, prov, resp, prazo, dias, rk = it
        cards.append(mcard(row(prio(pr), small(f"Prazo {prazo}"), justify="space-between"),
                           strong(f"{n} · {ctda}", style=f"font-size:14px;color:{TEXT};"),
                           p(prov, style=f"margin:0;font-size:14px;color:{TEXT2};line-height:1.45;"),
                           small(f"Motivo: {motivo}"),
                           row(small(f"Responsável: {resp}"), risco(rk), gap=6),
                           btn("Abrir", href="CelularFicha.dc.html", small_=True),
                           tone="red" if pr == "Crítica" else None))
    return mobile_page("Celular — Ação agora", "acao",
                       [tag("h1", "Ação agora", style=f"margin:0;font-size:20px;color:{TEXT};"), ind,
                        small("Cartões de providências com prioridade e motivo"), *cards,
                        a("Ver todas (12)", "Main.dc.html"),
                        small("No celular: providências, ciência, decisões e registros de marco. Carga em massa, conciliação e formulários financeiros extensos ficam no computador.")])


@screen("CelularFicha.dc.html", "Celular — Ficha do contrato", "r10", "12.6", mobile=True)
def cel_ficha():
    c = C("012/2025")
    seletor = tag("select", *[tag("option", t_[0]) for t_ in T03_TABS[1:2] + T03_TABS[:1] + T03_TABS[2:]], id="aba-cel",
                  style=inp_style() + f"background:{SURF};")
    return mobile_page("Celular — Ficha", "ficha", [
        a("‹ Ação agora", "Celular.dc.html", style=f"color:{ACC};font-size:14px;text-decoration:none;"),
        tag("h1", f"{c['n']} · {c['ctda']}", style=f"margin:0;font-size:19px;color:{TEXT};line-height:1.3;"),
        small(c["obj"]),
        row(desig("Completa"), risco("Alto"), qual("Validado"), gap=6),
        mcard(small("Término formalizado"), div("28/11/2026", style=f"font-size:24px;font-weight:700;color:{TEXT};"),
              small("18 dias restantes · fonte: contrato 012/2025 assinado em 28/11/2025")),
        div(tag("label", "Aba da ficha", **{"for": "aba-cel"}, style=f"font-size:13px;font-weight:600;color:{TEXT};"), seletor,
            style="display:flex;flex-direction:column;gap:6px;"),
        mcard(row(strong("Formalizado"), nat("Formalizado"), justify="space-between"),
              kv([("Vigência", "29/11/2025 a 28/11/2026"), ("Valor atualizado (vigência corrente)", "R$ 1.074.400,00"), ("Valor mensal vigente", "R$ 91.800,00")], min_=300)),
        mcard(row(strong("Em tramitação"), badge("Não altera o término", "gray"), justify="space-between"),
              kv([("Procedimento", "PRC-2026-014 · Prorrogação"), ("Etapa", "4 Análise jurídica (desde 05/11/2026)"), ("Término pretendido (minuta)", "28/11/2027")], min_=300)),
        mcard(strong("Marcos regulamentares (C19)"),
              row(small("M120 31/07/2026"), marco("Cumprido"), gap=6), row(small("M30 29/10/2026"), marco("Cumprido com atraso"), gap=6)),
        actions(btn("Registrar providência", href="CelularNotificacao.dc.html", kind="primary", small_=True), btn("Registrar marco", small_=True)),
    ])


@screen("CelularNotificacao.dc.html", "Celular — Notificação", "r10", "12.6", mobile=True)
def cel_notif():
    return mobile_page("Celular — Notificação", "notif", [
        a("‹ Notificações", "Notificacoes.dc.html", style=f"color:{ACC};font-size:14px;text-decoration:none;"),
        row(badge("N01 · Aproximação do término", "blue"), prio("Alta"), gap=6),
        tag("h1", "012/2025 · Alfa Serviços Prediais Ltda", style=f"margin:0;font-size:19px;color:{TEXT};line-height:1.3;"),
        mcard(small("Motivo"), p("Término da vigência formalizada em 28/11/2026 — antecedência de 30 dias (parâmetro interno).", style=f"margin:0;font-size:15px;color:{TEXT};line-height:1.5;")),
        mcard(kv([("Data-limite", "28/11/2026 · em 18 dias"), ("Responsável", "P. Nunes (gestor)"), ("Próxima ação", "Obter parecer jurídico e autorização da prorrogação"),
                  ("Gerada em", "29/10/2026 07:00 (Brasília)"), ("Dados atualizados em", "10/11/2026 07:00 — fonte: registros validados")], min_=300)),
        btn("Registrar ciência", kind="secondary"),
        btn("Abrir providência", href="T11B-Todas.dc.html", kind="primary"),
        alert("info", None, "Registrar ciência não conclui a providência."),
        a("Abrir a ficha do contrato", "CelularFicha.dc.html"),
    ])
