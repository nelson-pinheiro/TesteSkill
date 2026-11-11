"""Núcleo do gerador de protótipos (formato .dc.html do canvas de design).

Moldura comum (seção 12.1 do Projeto Básico v0.4), tokens visuais (Anexo B)
e componentes reutilizados por todas as telas. Todo texto passa por escape;
apenas objetos H (HTML já montado) são inseridos sem escape.
"""
import datetime as dt
import html as _html

POSICAO = dt.date(2026, 11, 10)          # data de posição dos casos de aceite (seção 14)
POSICAO_TXT = "10/11/2026"
VERSAO_SISTEMA = "1.0.0 (protótipo)"
VERSAO_REGRAS = "v0.4 (C01–C22)"

# Tokens (Anexo B: fundo #0B0F14, superfícies #131A22, texto #E6EDF3, acento #5B9BFF)
BG, NAV, SURF, RAISED = "#0B0F14", "#10161D", "#131A22", "#18212B"
LINE, LINE2, LINE3 = "#233040", "#2D3B4D", "#1C2633"
TEXT, TEXT2, MUTED, FAINT = "#E6EDF3", "#C3CFDB", "#A3B1BF", "#8C9AA8"
ACC, ACC2, ACCBG = "#5B9BFF", "#8CC8FF", "#0F2A44"
FONT = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

TONES = {
    "red": ("#3A1418", "#FFB3B8", "#6B2128"),
    "orange": ("#3A2410", "#FFC489", "#6B4219"),
    "yellow": ("#2F2A0E", "#F5DA7A", "#5C5216"),
    "green": ("#0E2E22", "#8FE6BC", "#1D5A42"),
    "blue": ("#0F2A44", "#A8D1FF", "#1F4C78"),
    "teal": ("#0C2C2F", "#82DDE0", "#19575C"),
    "purple": ("#271C3D", "#D2B8FF", "#4A3673"),
    "indigo": ("#1C2148", "#B9C2FF", "#363F80"),
    "pink": ("#3A1530", "#F7B3E0", "#6B2659"),
    "gray": ("#1C2530", "#C3CFDB", "#334355"),
}


class H(str):
    """HTML já montado (não sofre escape)."""


def esc(s):
    return _html.escape(str(s), quote=True)


def x(v):
    if v is None or v is False:
        return ""
    if isinstance(v, H):
        return v
    if isinstance(v, (list, tuple)):
        return "".join(x(i) for i in v)
    return esc(v)


def cat(*parts):
    return H("".join(x(p) for p in parts))


VOID = {"input", "img", "br", "hr", "meta", "link", "col", "source"}


def tag(_tagname, *children, style=None, **attrs):
    name = _tagname
    a = []
    if style:
        a.append(f'style="{esc(style)}"')
    for k, v in attrs.items():
        if v is None or v is False:
            continue
        k = k.rstrip("_").replace("_", "-")
        if v is True:
            a.append(k)
        else:
            a.append(f'{k}="{esc(v)}"')
    open_ = f"<{name}{(' ' + ' '.join(a)) if a else ''}>"
    if name in VOID:
        return H(open_)
    return H(open_ + "".join(x(c) for c in children) + f"</{name}>")


def div(*c, style=None, **a):
    return tag("div", *c, style=style, **a)


def span(*c, style=None, **a):
    return tag("span", *c, style=style, **a)


def p(*c, style=None, **a):
    return tag("p", *c, style=style or f"margin:0;font-size:14px;line-height:1.55;color:{TEXT2};", **a)


def small(*c, style=None):
    return span(*c, style=style or f"font-size:12px;color:{MUTED};line-height:1.5;")


def strong(*c, style=None):
    return tag("strong", *c, style=style or f"color:{TEXT};font-weight:600;")


def a(text, href, style=None, **attrs):
    return tag("a", text, href=href, style=style or f"color:{ACC};text-decoration:underline;text-underline-offset:2px;", **attrs)


def row(*c, gap=12, wrap=True, align="center", justify=None, style=""):
    s = f"display:flex;{'flex-wrap:wrap;' if wrap else ''}align-items:{align};gap:{gap}px;"
    if justify:
        s += f"justify-content:{justify};"
    return div(*c, style=s + style)


def col(*c, gap=12, style=""):
    return div(*c, style=f"display:flex;flex-direction:column;gap:{gap}px;" + style)


def grid(*c, min_=280, gap=16, style=""):
    return div(*c, style=f"display:grid;grid-template-columns:repeat(auto-fit,minmax(min({min_}px,100%),1fr));gap:{gap}px;" + style)


# ------------------------------------------------------------------ ícones
ICONS = {
    "home": '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "refresh": '<path d="M20 11a8 8 0 0 0-14.9-4M4 4v4h4M4 13a8 8 0 0 0 14.9 4M20 20v-4h-4"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M2 20h20"/>',
    "wallet": '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14h2"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "percent": '<path d="M5 19L19 5"/><circle cx="7" cy="7" r="2"/><circle cx="17" cy="17" r="2"/>',
    "check": '<path d="M9 11l3 3 8-8"/><path d="M20 12v7a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h11"/>',
    "bell": '<path d="M6 8a6 6 0 1 1 12 0c0 7 3 8 3 8H3s3-1 3-8"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "report": '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "warn": '<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4M12 17h.01"/>',
    "x": '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>',
    "ok": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "upload": '<path d="M12 15V3M7 8l5-5 5 5"/><path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"/>',
    "plug": '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "edit": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M14 6l4 4"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "file": '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5"/>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
}


def icon(name, size=18, color="currentColor"):
    return H(
        f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" '
        f'style="flex:none;">{ICONS[name]}</svg>'
    )


# ------------------------------------------------------------------ selos (rótulos fixos — seção 12.1)
def badge(text, tone="gray", dashed=False, title=None):
    bg, fg, bd = TONES[tone]
    return span(
        text,
        style=(f"display:inline-flex;align-items:center;gap:4px;min-height:22px;padding:1px 8px;border-radius:4px;"
               f"font-size:12px;font-weight:600;line-height:1.3;white-space:nowrap;background:{bg};color:{fg};"
               f"border:1px {'dashed' if dashed else 'solid'} {bd};box-sizing:border-box;"),
        title=title,
    )


def outline(text, color=TEXT2, bd=LINE2):
    return span(text, style=(f"display:inline-flex;align-items:center;min-height:22px;padding:1px 8px;border-radius:4px;"
                             f"font-size:12px;font-weight:600;white-space:nowrap;color:{color};border:1px solid {bd};box-sizing:border-box;"))


PRIO = {"Crítica": "red", "Alta": "orange", "Média": "yellow", "Planejamento": "blue", "A confirmar": "gray"}


def prio(p):
    return badge(p, PRIO[p], dashed=(p == "A confirmar"))


def risco(r):
    if r.startswith("Existente"):
        t = "red"
    elif r.startswith("Alto"):
        t = "orange"
    elif r.startswith("Moderado"):
        t = "yellow"
    elif r.startswith("Sem risco"):
        t = "green"
    else:
        t = "gray"
    return badge(r, t, dashed=r.startswith("Indeterminado"))


def risco_lbl(r):
    return cat(small("Risco: "), risco(r))


def qual(q):
    t = {"Validado": "green", "Importado – não validado": "purple"}.get(q, "gray")
    return badge(q, t, dashed=q in ("Não informado", "Não apurado"))


def nat(n):
    t = {"Formalizado": "blue", "Execução registrada": "teal", "Projeção": "indigo", "Cenário simulado": "pink",
         "Simulação": "pink"}[n]
    return badge(n, t)


def marco(m):
    t = {"A cumprir": "gray", "Cumprido": "green", "Cumprido com atraso": "yellow", "Descumprido": "red",
         "Não aplicável": "gray"}[m]
    return badge(m, t, dashed=(m == "Não aplicável"))


def desig(d):
    if d.startswith("Completa"):
        t = "green"
    elif d.startswith("Sem designação"):
        t = "red"
    else:
        t = "orange"
    return badge(d, t)


def prazo_nat(n):
    lbl = {"Parâmetro interno": "Parâmetro interno (configurável)", "Legal regulamentar": "Legal (regulamentar)"}.get(n, n)
    color = {"Legal": "#A8D1FF", "Legal regulamentar": "#A8D1FF", "Contrato": "#82DDE0", "Legal supletivo": "#A8D1FF"}.get(n, TEXT2)
    bd = {"Legal": "#1F4C78", "Legal regulamentar": "#1F4C78", "Contrato": "#19575C", "Legal supletivo": "#1F4C78"}.get(n, LINE2)
    return outline(lbl, color, bd)


def estado(t, tone=None):
    tones = {"pendente": "yellow", "enviada": "green", "falha": "red", "cancelada": "gray", "Pendente": "yellow",
             "Atendido": "green", "Não aplicável": "gray", "Aberta": "blue", "Em andamento": "blue",
             "Aguardando terceiro": "purple", "Concluída": "green", "Cancelada": "gray", "Rascunho": "gray",
             "Submetido à validação": "blue", "Devolvido": "orange", "Validado": "green"}
    return badge(t, tone or tones.get(t, "gray"))


# ------------------------------------------------------------------ origem do dado (seção 12.1 — selo e "Ver origem")
def origem(modo="Digitado", autor="R. Costa", quando="12/03/2026 10:14", fonte=None, doc=None):
    color = {"Digitado": "#C3CFDB", "Importado": "#D2B8FF", "Integrado": "#82DDE0"}[modo]
    fonte = fonte or {"Digitado": "Digitação na tela T04", "Importado": "Lote L01 · planilha de acompanhamento · aba Contratos · célula H87",
                      "Integrado": "Sincronização PNCP · execução nº 2026-11-09-0300"}[modo]
    panel = div(
        div("Proveniência do dado", style=f"font-size:12px;font-weight:700;color:{TEXT};margin-bottom:6px;"),
        tag("dl", *[cat(tag("dt", k, style=f"color:{FAINT};"), tag("dd", v, style=f"margin:0;color:{TEXT2};"))
                     for k, v in [("Modo", modo), ("Fonte", fonte), ("Autor", autor), ("Data", quando),
                                  ("Documento de suporte", doc or "SEI-040014/000418/2025 · doc. 41029337")]],
            style="display:grid;grid-template-columns:auto 1fr;gap:4px 10px;margin:0;font-size:12px;"),
        style=f"margin-top:6px;padding:10px 12px;background:{BG};border:1px solid {LINE2};border-radius:6px;min-width:240px;",
    )
    return tag("details",
               tag("summary", outline(modo, color), span("Ver origem", style=f"font-size:12px;color:{ACC};text-decoration:underline;"),
                   style="display:inline-flex;align-items:center;gap:6px;cursor:pointer;list-style:none;"),
               panel, style="display:inline-block;")


# ------------------------------------------------------------------ controles
def btn(text, href=None, kind="secondary", ico=None, disabled=False, title=None, small_=False):
    h = 36 if small_ else 44
    base = (f"display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:{h}px;padding:0 {12 if small_ else 16}px;"
            f"border-radius:6px;font:600 {13 if small_ else 14}px {FONT};text-decoration:none;cursor:pointer;box-sizing:border-box;text-align:center;max-width:100%;")
    if kind == "primary":
        s = base + f"background:{ACC};color:#06111F;border:1px solid {ACC};"
    elif kind == "danger":
        s = base + "background:#3A1418;color:#FFB3B8;border:1px solid #6B2128;"
    elif kind == "ghost":
        s = base + f"background:transparent;color:{ACC};border:1px solid transparent;"
    else:
        s = base + f"background:{RAISED};color:{TEXT};border:1px solid {LINE2};"
    if disabled:
        s += "opacity:.55;cursor:not-allowed;"
    kids = cat(icon(ico, 16) if ico else None, text)
    if href and not disabled:
        return tag("a", kids, href=href, style=s, title=title)
    return tag("button", kids, type="button", style=s, disabled=disabled, title=title)


def actions(*b, justify=None):
    return row(*b, gap=8, justify=justify)


def inp_style(w=None):
    return (f"width:{w or '100%'};max-width:100%;min-height:44px;box-sizing:border-box;padding:0 12px;background:{BG};color:{TEXT};"
            f"border:1px solid {LINE2};border-radius:6px;font:400 14px {FONT};")


_fid = [0]


def _id(prefix="f"):
    _fid[0] += 1
    return f"{prefix}{_fid[0]}"


def field(label, value="", req=False, kind="text", options=None, help=None, nature=None, ref=None, origin=None,
          error=None, ro=False, w=None, placeholder=None, rows=3, note=None):
    """Campo de formulário: rótulo sempre visível, obrigatório indicado por texto (seção 12.1)."""
    fid = _id()
    lab = tag("label", label, span(" (obrigatório)", style=f"color:{FAINT};font-weight:500;") if req else None,
              **{"for": fid}, style=f"font-size:13px;font-weight:600;color:{TEXT};")
    bd = "#E5484D" if error else LINE2
    st = inp_style(w).replace(f"border:1px solid {LINE2}", f"border:1px solid {bd}")
    if ro:
        st += f"background:{RAISED};color:{TEXT2};"
    if kind == "select":
        opts = options or [value]
        ctl = tag("select", *[tag("option", o) for o in opts], id=fid, style=st, disabled=ro or None)
    elif kind == "textarea":
        ctl = tag("textarea", value, id=fid, rows=str(rows), style=st + "padding:10px 12px;min-height:72px;line-height:1.5;",
                  readonly=ro or None, placeholder=placeholder)
    elif kind in ("radio", "checkbox"):
        items = []
        for i, o in enumerate(options or []):
            oid = f"{fid}_{i}"
            chk = o.startswith("*")
            o = o.lstrip("*")
            items.append(tag("label", tag("input", type=kind, id=oid, name=fid, checked=chk or None,
                                          style=f"width:18px;height:18px;accent-color:{ACC};margin:0;"),
                             span(o), **{"for": oid},
                             style=f"display:flex;align-items:center;gap:8px;min-height:36px;font-size:14px;color:{TEXT2};"))
        ctl = div(*items, id=fid, style="display:flex;flex-wrap:wrap;gap:4px 18px;")
        lab = tag("span", label, span(" (obrigatório)", style=f"color:{FAINT};font-weight:500;") if req else None,
                  style=f"font-size:13px;font-weight:600;color:{TEXT};")
    else:
        typ = {"date": "text", "money": "text", "number": "text"}.get(kind, kind)
        ctl = tag("input", type=typ, id=fid, value=value if value != "" else None, placeholder=placeholder,
                  readonly=ro or None, inputmode="decimal" if kind == "money" else None,
                  style=st + ("text-align:right;font-variant-numeric:tabular-nums;" if kind == "money" else ""),
                  aria_invalid="true" if error else None)
    helpers = []
    if nature or help:
        helpers.append(row(prazo_nat(nature) if nature else None,
                           small(help) if help else None, small(ref, style=f"font-size:12px;color:{FAINT};") if ref else None, gap=6))
    if error:
        helpers.append(row(icon("x", 14, "#FF8A8F"), span(error, style="font-size:12px;color:#FFB3B8;"), gap=6))
    if note:
        helpers.append(small(note))
    top = row(lab, origin, gap=8, justify="space-between")
    return div(top, ctl, *helpers, style="display:flex;flex-direction:column;gap:6px;min-width:0;")


def form_grid(*fields, min_=260):
    return grid(*fields, min_=min_, gap=16)


# ------------------------------------------------------------------ blocos
def section(title, *children, act=None, sub=None, tone=None, id=None, h=2):
    bd = {"warn": "#6B4219", "danger": "#6B2128", "sim": "#6B2659"}.get(tone, LINE)
    head = row(col(tag(f"h{h}", title, style=f"margin:0;font-size:{17 if h == 2 else 15}px;font-weight:600;color:{TEXT};line-height:1.3;"),
                   small(sub) if sub else None, gap=4),
               act, justify="space-between", align="flex-start") if (title or act) else None
    return tag("section", head, *children, id=id,
               style=f"background:{SURF};border:1px solid {bd};border-radius:8px;padding:20px;display:flex;flex-direction:column;gap:16px;min-width:0;")


def alert(kind, title, *body):
    ic, bg, bd, fg = {
        "info": ("info", "#0E1C2C", "#1F4C78", "#A8D1FF"),
        "warn": ("warn", "#241A0C", "#6B4219", "#FFC489"),
        "danger": ("x", "#24100F", "#6B2128", "#FFB3B8"),
        "ok": ("ok", "#0C2219", "#1D5A42", "#8FE6BC"),
        "sim": ("info", "#26101F", "#6B2659", "#F7B3E0"),
    }[kind]
    return div(icon(ic, 18, fg),
               div(strong(title, style=f"color:{fg};font-weight:600;font-size:14px;") if title else None,
                   *[div(b, style=f"font-size:13px;line-height:1.55;color:{TEXT2};margin-top:2px;") for b in body],
                   style="min-width:0;"),
               role="status" if kind in ("info", "ok") else None,
               style=f"display:flex;gap:10px;align-items:flex-start;padding:12px 14px;background:{bg};border:1px solid {bd};border-radius:6px;")


def details(summary, *body, open_=False):
    return tag("details",
               tag("summary", summary, style=f"cursor:pointer;color:{ACC};font-size:13px;font-weight:600;min-height:28px;display:flex;align-items:center;gap:6px;"),
               div(*body, style=f"margin-top:8px;padding:12px;background:{BG};border:1px solid {LINE2};border-radius:6px;display:flex;flex-direction:column;gap:8px;"),
               open=open_ or None)


def composicao(*linhas, fonte="registros validados", cobertura=None, formula=None):
    """'Ver composição' de indicador/total (seção 12.1 — Contexto)."""
    body = [tag("dl", *[cat(tag("dt", k, style=f"color:{FAINT};"), tag("dd", v, style=f"margin:0;text-align:right;color:{TEXT};font-variant-numeric:tabular-nums;"))
                        for k, v in linhas],
                style="display:grid;grid-template-columns:1fr auto;gap:4px 12px;margin:0;font-size:12px;")]
    meta = [f"Posição {POSICAO_TXT} 07:00 (Brasília)", f"Fonte: {fonte}"]
    if formula:
        meta.append(f"Fórmula: {formula}")
    if cobertura:
        meta.append(f"Cobertura: {cobertura}")
    body.append(small(" · ".join(meta)))
    return details("Ver composição", *body)


def memoria(*linhas, formula=None):
    return details("Ver memória", tag("dl", *[cat(tag("dt", k, style=f"color:{FAINT};"), tag("dd", v, style=f"margin:0;text-align:right;color:{TEXT};"))
                                                for k, v in linhas],
                                       style="display:grid;grid-template-columns:1fr auto;gap:4px 12px;margin:0;font-size:12px;"),
                   small(formula) if formula else None)


def kv(items, min_=220):
    """Pares rótulo/valor somente leitura."""
    cells = []
    for it in items:
        k, v = it[0], it[1]
        extra = it[2] if len(it) > 2 else None
        cells.append(div(div(k, style=f"font-size:12px;color:{FAINT};font-weight:500;"),
                         div(v, style=f"font-size:14px;color:{TEXT};margin-top:3px;line-height:1.45;font-variant-numeric:tabular-nums;"),
                         div(extra, style="margin-top:4px;") if extra else None,
                         style="min-width:0;"))
    return grid(*cells, min_=min_, gap=14)


def table(cols, rows, caption=None, foot=None, minw=None, dense=False, zebra=False):
    pad = "8px 10px" if dense else "10px 12px"
    ths = []
    aligns = []
    for c in cols:
        name, al = (c if isinstance(c, tuple) else (c, "l"))
        aligns.append("right" if al == "r" else ("center" if al == "c" else "left"))
        ths.append(tag("th", name, scope="col",
                       style=f"text-align:{aligns[-1]};padding:{pad};color:{MUTED};font-weight:600;font-size:12px;border-bottom:1px solid {LINE};white-space:nowrap;background:{RAISED};"))
    trs = []
    for i, r in enumerate(rows):
        tds = []
        for j, cval in enumerate(r):
            al = aligns[j] if j < len(aligns) else "left"
            tds.append(tag("td", cval, style=f"text-align:{al};padding:{pad};border-bottom:1px solid {LINE3};vertical-align:top;color:{TEXT};"))
        trs.append(tag("tr", *tds, style=f"background:{RAISED if zebra and i % 2 else 'transparent'};"))
    t = tag("table", tag("caption", caption, style=f"text-align:left;font-size:12px;color:{MUTED};padding:0 0 8px;font-weight:600;") if caption else None,
            tag("thead", tag("tr", *ths)), tag("tbody", *trs),
            tag("tfoot", tag("tr", *[tag("td", f, style=f"text-align:{aligns[j] if j < len(aligns) else 'left'};padding:{pad};color:{TEXT};font-weight:700;border-top:1px solid {LINE2};") for j, f in enumerate(foot)])) if foot else None,
            style=f"width:100%;{'min-width:%dpx;' % minw if minw else ''}border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums;line-height:1.45;")
    return div(t, style=f"overflow-x:auto;border:1px solid {LINE};border-radius:6px;")


def listbar(n, gaps, acts=None, extra=None):
    """Contador 'N registros · M com lacunas de dados', colunas configuráveis e exportação (seção 12.1 — Listas)."""
    return row(
        row(strong(f"{n} registros"), span("·", style=f"color:{FAINT};"),
            span(f"{gaps} com lacunas de dados", style=f"color:{TEXT2};font-size:14px;"), extra, gap=8),
        actions(btn("Colunas", ico="gear", small_=True), btn("Exportar XLSX", ico="download", small_=True),
                btn("CSV", small_=True), btn("PDF", small_=True), *(acts or [])),
        justify="space-between")


def pager(txt):
    return row(small(txt), actions(btn("Anterior", small_=True, disabled=True), btn("Próxima", small_=True, disabled=True)),
               justify="space-between")


def filterbar(*fields, saved=("Meus vencimentos — GERAD", "Contratos com lacunas")):
    sel = tag("select", *[tag("option", s) for s in ("Filtros salvos…",) + tuple(saved)], style=inp_style("220px"),
              aria_label="Filtros salvos")
    return div(
        grid(*fields, min_=170, gap=12),
        row(sel, btn("Salvar filtro", small_=True), btn("Limpar filtros", kind="ghost", small_=True),
            small("Filtros e posição persistem ao voltar de um registro."), gap=8),
        style=f"display:flex;flex-direction:column;gap:12px;padding:16px;background:{SURF};border:1px solid {LINE};border-radius:8px;")


def fsel(label, *opts):
    return field(label, kind="select", options=list(opts))


def tabs(items, active, label="Abas"):
    lis = []
    for it in items:
        lbl, href = it[0], it[1]
        dis = len(it) > 2 and it[2] == "disabled"
        is_act = lbl == active
        s = (f"display:inline-flex;align-items:center;min-height:44px;padding:0 14px;font-size:14px;text-decoration:none;white-space:nowrap;"
             f"border-bottom:2px solid {ACC if is_act else 'transparent'};color:{TEXT if is_act else MUTED};font-weight:{600 if is_act else 500};")
        if dis:
            lis.append(tag("li", span(lbl, style=s + "opacity:.5;", title="Visível quando o tipo é substituição")))
        else:
            lis.append(tag("li", tag("a", lbl, href=href, style=s, aria_current="page" if is_act else None)))
    return tag("nav", tag("ul", *lis, style="list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:2px;"),
               aria_label=label, style=f"border-bottom:1px solid {LINE};")


def stat(label, value, sub=None, tone=None):
    color = {"red": "#FFB3B8", "orange": "#FFC489", "green": "#8FE6BC", "yellow": "#F5DA7A"}.get(tone, TEXT)
    return div(div(label, style=f"font-size:12px;color:{MUTED};font-weight:600;"),
               div(value, style=f"font-size:22px;font-weight:700;color:{color};margin-top:4px;font-variant-numeric:tabular-nums;line-height:1.2;"),
               div(sub, style=f"font-size:12px;color:{MUTED};margin-top:4px;line-height:1.45;") if sub else None,
               style=f"padding:14px 16px;background:{SURF};border:1px solid {LINE};border-radius:8px;min-width:0;")


def bars(data, maxv, unit="R$ mi", color=ACC, label_w=64):
    """Gráfico de barras horizontais simples (decorativo; sempre acompanhado de tabela equivalente)."""
    rows_ = []
    for lbl, v, txt in data:
        pct = 0 if v is None else max(1, round(100 * v / maxv))
        rows_.append(div(span(lbl, style=f"color:{MUTED};"),
                         div(div(style=f"width:{pct}%;height:14px;background:{color};border-radius:3px;"),
                             style=f"height:14px;background:{RAISED};border-radius:3px;"),
                         span(txt, style="text-align:right;"),
                         style=f"display:grid;grid-template-columns:{label_w}px 1fr 96px;align-items:center;gap:10px;font-size:12px;font-variant-numeric:tabular-nums;"))
    return div(*rows_, aria_hidden="true", style="display:flex;flex-direction:column;gap:6px;")


def stepper(steps, current):
    items = []
    for i, (lbl, href) in enumerate(steps):
        n = i + 1
        state = "done" if n < current else ("cur" if n == current else "todo")
        circ = {"done": f"background:{ACCBG};color:{ACC2};border:1px solid #1F4C78;",
                "cur": f"background:{ACC};color:#06111F;border:1px solid {ACC};",
                "todo": f"background:transparent;color:{MUTED};border:1px solid {LINE2};"}[state]
        num = "R" if lbl.startswith("Revisão") else str(n)
        items.append(tag("li", tag("a", span(num, style=f"display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;font-size:12px;font-weight:700;{circ}"),
                                   span(lbl, style=f"font-size:13px;color:{TEXT if state == 'cur' else MUTED};font-weight:{600 if state == 'cur' else 500};"),
                                   href=href, aria_current="step" if state == "cur" else None,
                                   style="display:flex;align-items:center;gap:8px;min-height:44px;text-decoration:none;padding:0 6px;")))
    return tag("nav", tag("ol", *items, style="list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 10px;"),
               aria_label="Passos do cadastro",
               style=f"padding:8px 12px;background:{SURF};border:1px solid {LINE};border-radius:8px;")


def modes(importar="Importacao.dc.html", leiaute="L02", fonte=None, fonte_ativa=True):
    """Modos de entrada de dados (seção 12.1): Novo (digitar) sempre presente; Importar; Buscar na fonte."""
    return row(
        span("Modo de entrada:", style=f"font-size:13px;color:{MUTED};font-weight:600;"),
        badge("Novo (digitar) — sempre disponível", "blue"),
        btn(f"Importar ({leiaute})", href=importar, ico="upload", small_=True) if importar else None,
        btn(f"Buscar na fonte ({fonte})", ico="plug", small_=True, disabled=not fonte_ativa,
            title=None if fonte_ativa else "Conector inativo — consulte T14.07") if fonte else None,
        small("Importado ou integrado entra como “Importado – não validado”; correção por digitação preserva a origem anterior."),
        gap=8)


def form_actions(validar=False, devolver=False, submit=True, extra=None, note=None):
    return div(
        actions(btn("Salvar rascunho", ico="file"),
                btn("Submeter à validação", kind="primary") if submit else None,
                btn("Validar", kind="primary") if validar else None,
                btn("Devolver com motivo") if devolver else None,
                *(extra or [])),
        small(note or "Rascunho não alimenta totais. Falha ao salvar preserva o que foi digitado; conflito de versão mostra as duas versões lado a lado."),
        style=f"display:flex;flex-direction:column;gap:8px;padding:16px;background:{SURF};border:1px solid {LINE};border-radius:8px;")


def error_summary(items):
    """Resumo de erros no topo, com atalho para cada campo (seção 12.1 — Formulários)."""
    return div(
        row(icon("x", 18, "#FFB3B8"), strong(f"{len(items)} campo(s) precisam de atenção antes de submeter", style="color:#FFB3B8;font-weight:600;"), gap=8),
        tag("ul", *[tag("li", a(t, h)) for t, h in items], style=f"margin:6px 0 0 26px;padding:0;font-size:13px;line-height:1.7;color:{TEXT2};"),
        role="alert",
        style="padding:12px 14px;background:#24100F;border:1px solid #6B2128;border-radius:6px;")


def money(v):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s


def d(s):
    dd, mm, yy = s.split("/")
    return dt.date(int(yy), int(mm), int(dd))


def fmt(dte):
    return dte.strftime("%d/%m/%Y")


def dias_restantes(termino):
    return (d(termino) - POSICAO).days


def menos(termino, n):
    return fmt(d(termino) - dt.timedelta(days=n))
