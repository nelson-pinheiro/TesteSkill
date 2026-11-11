"""Moldura da aplicação (seção 12.1) e registro das telas."""
from core import *  # noqa: F401,F403

MENU = [
    ("inicio", "Início", "Main.dc.html", "home"),
    ("carteira", "Carteira", "Carteira.dc.html", "briefcase"),
    ("venc", "Vencimentos", "Vencimentos.dc.html", "calendar"),
    ("prorrog", "Prorrogações e substituições", "Prorrogacoes.dc.html", "refresh"),
    ("valores", "Valores e planejamento", "T07A-Formalizado.dc.html", "chart"),
    ("empenhos", "Empenhos", "Empenhos.dc.html", "wallet"),
    ("pagamentos", "Pagamentos", "Pagamentos.dc.html", "receipt"),
    ("reajustes", "Reajustes", "Reajustes.dc.html", "percent"),
    ("provid", "Providências", "Providencias.dc.html", "check"),
    ("notif", "Notificações", "Notificacoes.dc.html", "bell"),
    ("relat", "Relatórios", "Relatorios.dc.html", "report"),
    ("admin", "Administração", "T1401-Usuarios.dc.html", "gear"),
]
ADMIN = [
    ("T14.01", "Usuários, perfis e unidades", "T1401-Usuarios.dc.html"),
    ("T14.02", "Cadastros e parâmetros", "T1402-Categorias.dc.html"),
    ("T14.03", "Configuração de notificações", "T1403-Regras.dc.html"),
    ("T14.04", "Importação e conciliação", "Importacao.dc.html"),
    ("T14.05", "Auditoria e correções", "T1405-Trilha.dc.html"),
    ("T14.06", "Cópias e recuperação", "T1406-Copias.dc.html"),
    ("T14.07", "Integrações", "T1407-Conectores.dc.html"),
]

REGISTRY = []   # (file, meta, builder)


def screen(file, title, row, ref, mobile=False, standalone=False):
    def deco(fn):
        REGISTRY.append(dict(file=file, title=title, row=row, ref=ref, mobile=mobile, standalone=standalone, fn=fn))
        return fn
    return deco


HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#0B0F14}}
a{{color:#5B9BFF}}a:hover{{color:#8CC8FF}}
summary::-webkit-details-marker{{display:none}}
:focus-visible{{outline:2px solid #8CC8FF;outline-offset:2px}}
</style>
</helmet>
"""

TAIL = """</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":__H__}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""


def doc(title, root, w=1440):
    return HEAD.format(title=esc(title)) + root + "\n" + TAIL.format(w=w)


def header(perfil="Coordenador", unidade="GERAD", nome="M. Silva", ini="MS"):
    unidade_sel = tag("select", tag("option", f"{unidade} — {perfil}"), tag("option", "DIRAF — Consulta, auditoria e controle interno"),
                      id="unidade-ativa", style=inp_style("250px") + f"background:{SURF};min-height:40px;")
    posicao = tag("details",
                  tag("summary", span("Consultar em outra data", style=f"color:{ACC};text-decoration:underline;font-size:13px;"),
                      style="cursor:pointer;list-style:none;min-height:40px;display:flex;align-items:center;"),
                  div(field("Data da consulta (somente leitura)", "15/03/2026", kind="date"),
                      btn("Consultar", href="T03-Historico.dc.html", kind="primary", small_=True),
                      small("A tela passa a exibir a faixa “Consulta histórica — posição dd/mm/aaaa” e fica somente leitura."),
                      style=f"position:absolute;z-index:30;margin-top:6px;width:280px;padding:14px;background:{SURF};border:1px solid {LINE2};border-radius:8px;display:flex;flex-direction:column;gap:10px;box-shadow:0 12px 32px rgba(0,0,0,.45);"))
    busca = div(
        tag("label", "Busca global", **{"for": "busca-global"},
            style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;"),
        span(icon("search", 16, FAINT), style="position:absolute;left:12px;top:12px;display:flex;"),
        tag("input", type="search", id="busca-global",
            placeholder="Nº do contrato, objeto, contratada, processo SEI, nota de empenho ou documento fiscal",
            style=inp_style("100%") + f"padding-left:36px;background:{SURF};min-height:40px;"),
        style="position:relative;flex:1 1 300px;min-width:220px;max-width:520px;")
    sino = tag("a", icon("bell", 20), span("7", style="position:absolute;top:2px;right:0;min-width:18px;height:18px;padding:0 4px;box-sizing:border-box;border-radius:9px;background:#E5484D;color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;"),
               href="Notificacoes.dc.html", aria_label="Notificações: 7 não lidas",
               style=f"position:relative;display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:6px;color:{TEXT};border:1px solid {LINE2};box-sizing:border-box;")
    menu_user = tag("details",
                    tag("summary", span(ini, style=f"display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:{ACCBG};color:{ACC2};font-size:12px;font-weight:700;"),
                        span(nome, style=f"font-size:13px;color:{TEXT};"),
                        style="cursor:pointer;list-style:none;display:flex;align-items:center;gap:8px;min-height:44px;",
                        aria_label="Menu do usuário"),
                    div(div("Perfis vigentes", style=f"font-size:12px;color:{FAINT};font-weight:600;"),
                        div(f"{perfil} · {unidade} (desde 01/01/2026)", style=f"font-size:13px;color:{TEXT};"),
                        div("Consulta, auditoria e controle interno · DIRAF (até 31/12/2026)" if nome == "M. Silva" else "Sem perfil de negócio (função técnica)", style=f"font-size:13px;color:{TEXT};"),
                        tag("hr", style=f"border:0;border-top:1px solid {LINE};margin:4px 0;"),
                        a("Preferências (resumos e avisos)", "T12C-Resumos.dc.html"), a("Sair", "T00-Acesso.dc.html"),
                        style=f"position:absolute;right:0;z-index:30;margin-top:6px;width:300px;padding:14px;background:{SURF};border:1px solid {LINE2};border-radius:8px;display:flex;flex-direction:column;gap:8px;box-shadow:0 12px 32px rgba(0,0,0,.45);"),
                    style="position:relative;")
    return tag("header",
               tag("a", div("RIOPREVIDÊNCIA", style=f"font-size:11px;letter-spacing:.08em;color:{FAINT};font-weight:700;"),
                   div("Controle de Contratos", style=f"font-size:15px;font-weight:700;color:{TEXT};"),
                   href="Main.dc.html", style="text-decoration:none;display:flex;flex-direction:column;min-width:170px;"),
               div(tag("label", "Unidade ativa", **{"for": "unidade-ativa"}, style=f"font-size:12px;color:{FAINT};font-weight:600;"),
                   unidade_sel, style="display:flex;flex-direction:column;gap:2px;"),
               div(span("Data de posição", style=f"font-size:12px;color:{FAINT};font-weight:600;"),
                   row(strong(f"{POSICAO_TXT}", style=f"font-size:14px;color:{TEXT};font-weight:700;"), small("hoje · Brasília"), posicao, gap=8),
                   style="display:flex;flex-direction:column;gap:2px;position:relative;"),
               busca, sino, menu_user,
               style=f"position:sticky;top:0;z-index:20;display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px;padding:10px 24px;background:#0E141B;border-bottom:1px solid #1F2933;")


def sidebar(active):
    items = []
    for key, lbl, href, ic in MENU:
        act = key == active
        s = (f"display:flex;align-items:center;gap:10px;min-height:42px;padding:0 12px;border-radius:6px;text-decoration:none;font-size:14px;"
             f"background:{RAISED if act else 'transparent'};color:{'#FFFFFF' if act else MUTED};font-weight:{600 if act else 500};")
        items.append(tag("li", tag("a", icon(ic), lbl, href=href, style=s, aria_current="page" if act else None)))
        if key == "admin" and act:
            sub = [tag("li", tag("a", span(c, style=f"color:{FAINT};font-size:11px;"), span(n), href=h,
                                 style=f"display:flex;flex-direction:column;padding:6px 12px 6px 40px;text-decoration:none;font-size:13px;color:{MUTED};line-height:1.3;"))
                   for c, n, h in ADMIN]
            items.append(tag("li", tag("ul", *sub, style="list-style:none;margin:0;padding:0;")))
    return tag("nav",
               tag("ul", *items, style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px;"),
               div(div("Protótipo", style=f"font-size:11px;letter-spacing:.06em;color:{FAINT};font-weight:700;"),
                   a("Padrões e estados", "Padroes.dc.html"), a("Visões de celular", "Celular.dc.html"), a("Acesso e sessão (T00)", "T00-Acesso.dc.html"),
                   style=f"margin-top:12px;padding:12px;border-top:1px solid {LINE3};display:flex;flex-direction:column;gap:6px;font-size:13px;"),
               aria_label="Menu principal",
               style=f"flex:1 1 220px;max-width:248px;background:{NAV};border-right:1px solid #1F2933;padding:16px 10px;box-sizing:border-box;")


def crumbs(items):
    parts = []
    for i, it in enumerate(items):
        if i:
            parts.append(span("/", aria_hidden="true", style=f"color:{FAINT};"))
        if isinstance(it, tuple):
            parts.append(a(it[0], it[1], style=f"color:{MUTED};text-decoration:none;"))
        else:
            parts.append(span(it, style=f"color:{TEXT2};"))
    return tag("nav", *parts, aria_label="Trilha de navegação", style="display:flex;flex-wrap:wrap;gap:6px;font-size:12px;")


def footer():
    return tag("footer",
               span(f"Sistema de Controle de Contratos · versão {VERSAO_SISTEMA}"),
               span(f"Regras de cálculo {VERSAO_REGRAS}"),
               span("Protótipo navegável — dados fictícios; prevalece o catálogo da seção 12 do Projeto Básico v0.4"),
               style=f"display:flex;flex-wrap:wrap;gap:6px 24px;padding:14px 24px;border-top:1px solid #1F2933;font-size:12px;color:{FAINT};background:#0E141B;")


def hist_band(data="15/03/2026"):
    return div(icon("clock", 18, "#F5DA7A"),
               strong(f"Consulta histórica — posição {data}", style="color:#F5DA7A;font-weight:700;"),
               small("Somente leitura: a posição corrente não é sobrescrita; registros retroativos aparecem evidenciados."),
               a("Voltar à posição de hoje", "Ficha.dc.html"),
               role="status",
               style="display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;padding:10px 14px;background:#2F2A0E;border:1px solid #5C5216;border-radius:6px;")


def page(title, menu, crumb, body, tabs_=None, sub=None, acts=None, band=None, perfil="Coordenador", h1=None, unidade="GERAD", nome="M. Silva", ini="MS"):
    main = tag("main",
               crumbs(crumb),
               row(col(tag("h1", h1 or title, style=f"margin:0;font-size:24px;font-weight:600;line-height:1.25;color:{TEXT};"),
                       small(sub, style=f"font-size:13px;color:{MUTED};line-height:1.5;") if sub else None, gap=4),
                   actions(*acts) if acts else None, justify="space-between", align="flex-start"),
               band, tabs_, *body,
               style="flex:999 1 560px;min-width:0;padding:20px 28px 32px;box-sizing:border-box;display:flex;flex-direction:column;gap:20px;")
    root = div(header(perfil, unidade, nome, ini), div(sidebar(menu), main, style="display:flex;flex-wrap:wrap;align-items:stretch;"), footer(),
               style=f"min-height:100vh;background:{BG};color:{TEXT};font-family:{FONT};font-variant-numeric:tabular-nums;")
    return doc(title, root)


def mobile_nav(active):
    items = [("acao", "Ação agora", "Celular.dc.html", "home"), ("ficha", "Ficha", "CelularFicha.dc.html", "file"),
             ("notif", "Notificação", "CelularNotificacao.dc.html", "bell")]
    lis = [tag("li", tag("a", icon(ic, 20), span(lbl, style="font-size:11px;"), href=h, aria_current="page" if k == active else None,
                         style=f"display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:56px;text-decoration:none;color:{ACC2 if k == active else MUTED};font-weight:{600 if k == active else 500};"),
                  style="flex:1;") for k, lbl, h, ic in items]
    return tag("nav", tag("ul", *lis, style="list-style:none;margin:0;padding:0;display:flex;"), aria_label="Navegação do celular",
               style=f"position:sticky;bottom:0;background:#0E141B;border-top:1px solid #1F2933;")


def mobile_page(title, active, body):
    top = tag("header",
              row(div(div("RIOPREVIDÊNCIA", style=f"font-size:10px;letter-spacing:.08em;color:{FAINT};font-weight:700;"),
                      div("Controle de Contratos", style=f"font-size:15px;font-weight:700;color:{TEXT};")),
                  tag("a", icon("bell", 20), span("7", style="position:absolute;top:4px;right:2px;min-width:16px;height:16px;border-radius:8px;background:#E5484D;color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;"),
                      href="CelularNotificacao.dc.html", aria_label="Notificações: 7 não lidas",
                      style=f"position:relative;display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;color:{TEXT};"),
                  justify="space-between", wrap=False),
              row(badge("GERAD · Coordenador", "gray"), small(f"Posição {POSICAO_TXT} · Brasília"), gap=8),
              style=f"padding:12px 16px;background:#0E141B;border-bottom:1px solid #1F2933;display:flex;flex-direction:column;gap:8px;")
    main = tag("main", *body, style="padding:16px;display:flex;flex-direction:column;gap:14px;flex:1;")
    root = div(top, main, mobile_nav(active),
               style=f"width:390px;min-height:844px;display:flex;flex-direction:column;background:{BG};color:{TEXT};font-family:{FONT};font-variant-numeric:tabular-nums;box-sizing:border-box;")
    return doc(title, root, w=390)


def standalone(title, body):
    root = div(*body, style=f"min-height:100vh;background:{BG};color:{TEXT};font-family:{FONT};display:flex;flex-direction:column;")
    return doc(title, root)


# Abas compartilhadas -----------------------------------------------------
T01_TABS = [("A Ação agora", "Main.dc.html"), ("B Indicadores da carteira", "T01B-Indicadores.dc.html"), ("C Painel financeiro", "T01C-Financeiro.dc.html")]
T02_TABS = [("A Vigentes", "Carteira.dc.html"), ("B Encerrados e extintos", "T02B-Encerrados.dc.html"),
            ("C Rascunhos e não validados", "T02C-Rascunhos.dc.html"), ("D Todos", "T02D-Todos.dc.html")]
T03_TABS = [("T03.01 Identificação", "Ficha.dc.html"), ("T03.02 Prazos", "T0302-Prazos.dc.html"),
            ("T03.03 Valores", "T0303-Valores.dc.html"), ("T03.04 Empenhos", "T0304-Empenhos.dc.html"),
            ("T03.05 Fiscais e pagamentos", "T0305-Pagamentos.dc.html"), ("T03.06 Alterações", "T0306-Alteracoes.dc.html"),
            ("T03.07 Garantias", "T0307-Garantias.dc.html"), ("T03.08 Responsáveis", "T0308-Responsaveis.dc.html"),
            ("T03.09 Documentos", "T0309-Documentos.dc.html"), ("T03.10 Providências e histórico", "T0310-Historico.dc.html"),
            ("T03.11 Conformidade", "T0311-Conformidade.dc.html")]
T04_STEPS = [("Identificação", "T04-P1-Identificacao.dc.html"), ("Contratada", "T04-P2-Contratada.dc.html"),
             ("Origem e regime", "T04-P3-Origem.dc.html"), ("Processos", "T04-P4-Processos.dc.html"),
             ("Responsáveis", "T04-P5-Responsaveis.dc.html"), ("Prazos", "T04-P6-Prazos.dc.html"),
             ("Composição financeira", "T04-P7-Composicao.dc.html"), ("Revisão", "T04-Revisao.dc.html")]
T05_TABS = [("A Lista por faixas", "Vencimentos.dc.html"), ("B Calendário", "T05B-Calendario.dc.html"),
            ("C Continuidade", "T05C-Continuidade.dc.html"), ("D Marcos regulamentares", "T05D-Marcos.dc.html")]
T06_TABS = [("A Em andamento", "Prorrogacoes.dc.html"), ("B Concluídos e cancelados", "T06B-Concluidos.dc.html")]
T06_DET = [("1 Resumo", "T06-D1-Resumo.dc.html"), ("2 Etapas e movimentações", "T06-D2-Etapas.dc.html"),
           ("3 Lista de verificação", "T06-D3-Checklist.dc.html"), ("4 Marcos e prazos", "T06-D4-Marcos.dc.html"),
           ("5 Substituição", "T06-D5-Substituicao.dc.html", "disabled"), ("6 Documentos", "T06-D6-Documentos.dc.html")]
T07_TABS = [("A Formalizado", "T07A-Formalizado.dc.html"), ("B Execução registrada", "T07B-Execucao.dc.html"),
            ("C Projeção", "T07C-Projecao.dc.html"), ("D Cenários simulados", "T07D-Cenarios.dc.html")]
T08_TABS = [("A Cobertura", "Empenhos.dc.html"), ("B Notas de empenho", "T08B-Notas.dc.html"),
            ("C Restos a pagar", "T08C-RestosPagar.dc.html"), ("D Solicitações de reforço", "T08D-Solicitacoes.dc.html")]
T0801_TABS = [("Nota de empenho", "T0801-NotaEmpenho.dc.html"), ("Movimento de empenho", "T0801-Movimento.dc.html"),
              ("Liquidação", "T0801-Liquidacao.dc.html"), ("Pagamento", "T0801-Pagamento.dc.html"),
              ("Solicitação de reforço", "T0801-Reforco.dc.html")]
T09_TABS = [("A Obrigações", "Pagamentos.dc.html"), ("B Documentos fiscais", "T09B-DocFiscais.dc.html"),
            ("C Liquidações", "T09C-Liquidacoes.dc.html"), ("D Pagamentos e retenções", "T09D-Pagamentos.dc.html"),
            ("E Impedimentos", "T09E-Impedimentos.dc.html")]
T10_TABS = [("A Pedidos", "Reajustes.dc.html"), ("B Datas-base", "T10B-DatasBase.dc.html"), ("C Retroativos", "T10C-Retroativos.dc.html")]
T11_TABS = [("A Minhas", "Providencias.dc.html"), ("B Todas", "T11B-Todas.dc.html"), ("C Por responsável", "T11C-PorResponsavel.dc.html"),
            ("D Concluídas e canceladas", "T11D-Concluidas.dc.html")]
T12_TABS = [("A Não lidas", "Notificacoes.dc.html"), ("B Histórico", "T12B-Historico.dc.html"), ("C Resumos", "T12C-Resumos.dc.html")]
T13_TABS = [("A Catálogo", "Relatorios.dc.html"), ("B Emissões recentes", "T13B-Emissoes.dc.html")]
T1401_TABS = [("Usuários", "T1401-Usuarios.dc.html"), ("Perfis e permissões", "T1401-Perfis.dc.html"), ("Unidades", "T1401-Unidades.dc.html")]
T1402_TABS = [("Categorias e grupos", "T1402-Categorias.dc.html"), ("Etapas e listas de verificação", "T1402-Etapas.dc.html"),
              ("Parâmetros internos", "T1402-Parametros.dc.html"), ("Regras jurídicas", "T1402-Regras.dc.html"),
              ("Calendário e índices", "T1402-Calendario.dc.html")]
T1403_TABS = [("Regras por evento", "T1403-Regras.dc.html"), ("Destinatários e canais", "T1403-Destinatarios.dc.html"), ("Monitor", "T1403-Monitor.dc.html")]
T1404_TABS = [("T14.04.01 Lotes", "Importacao.dc.html"), ("02 Prévia e mapeamento", "T140402-Mapeamento.dc.html"),
              ("03 Conciliação de contratos", "T140403-Conciliacao.dc.html"), ("04 Divergências de designação", "T140404-Designacao.dc.html"),
              ("05 Validação por domínio", "T140405-Validacao.dc.html"), ("06 Qualidade da carteira", "T140406-Qualidade.dc.html"),
              ("07 Recibo e reconciliação", "T140407-Recibo.dc.html")]
T1405_TABS = [("Trilha", "T1405-Trilha.dc.html"), ("Exportações", "T1405-Exportacoes.dc.html"), ("Correções", "T1405-Correcoes.dc.html")]
T1407_TABS = [("Conectores", "T1407-Conectores.dc.html"), ("Execuções", "T1407-Execucoes.dc.html"), ("Divergências", "T1407-Divergencias.dc.html")]
