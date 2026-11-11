"""Gera os artboards (.dc.html), mede as alturas, monta o canvas.json e executa as verificações automáticas.

Uso: python3 build.py            (gera em ../canvas/project)
"""
import copy
import html.parser
import importlib
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "canvas", "project")
MODULES = ["s_inicio", "s_carteira", "s_cadastro", "s_prazos", "s_financas", "s_pagamentos", "s_gestao", "s_admin"]

import shell  # noqa: E402

for m in MODULES:
    if os.path.exists(os.path.join(HERE, m + ".py")):
        importlib.import_module(m)

ROWS = {
    "r01": "T01 Início (abas A, B, C) · T00 Acesso e sessão",
    "r02": "T02 Carteira de contratos",
    "r03": "T03 Ficha única do contrato — abas T03.01 a T03.11",
    "r04": "T04 Cadastro e edição (7 passos e revisão) · T04.01 Formalização de evento",
    "r05": "T05 Vencimentos e continuidade · T06 Prorrogações e substituições",
    "r06": "T07 Valores e planejamento · T08 Empenhos e reforços · T08.01 Movimentação",
    "r07": "T09 Documentos fiscais e pagamentos · T10 Reajustes e T10.01 Simulação",
    "r08": "T11 Providências · T12 Notificações · T13 Relatórios",
    "r09": "T14 Administração — T14.01 a T14.03",
    "r09b": "T14 Administração — T14.04 a T14.07",
    "r10": "Padrões comuns (12.1) e consulta pelo celular (12.6)",
}


class Checker(html.parser.HTMLParser):
    VOID = {"input", "img", "br", "hr", "meta", "link", "col", "source", "area", "base", "wbr"}

    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, t, attrs):
        if t not in self.VOID:
            self.stack.append(t)

    def handle_endtag(self, t):
        if t in self.VOID:
            return
        if not self.stack or self.stack[-1] != t:
            self.errors.append(f"fechamento inesperado </{t}> (pilha: {self.stack[-3:]})")
            if t in self.stack:
                while self.stack and self.stack.pop() != t:
                    pass
        else:
            self.stack.pop()


def main():
    os.makedirs(OUT, exist_ok=True)
    reg = shell.REGISTRY
    files = {}
    for s in reg:
        files[s["file"]] = s["fn"]()
    # escreve versão provisória e mede
    lista = []
    for s in reg:
        path = os.path.join(OUT, s["file"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(files[s["file"]])
        lista.append(dict(file=s["file"], path=path, w=390 if s["mobile"] else 1440))
    tmp_in, tmp_out = os.path.join(HERE, ".medir_in.json"), os.path.join(HERE, ".medir_out.json")
    json.dump(lista, open(tmp_in, "w"))
    subprocess.run(["node", os.path.join(HERE, "medir.js"), tmp_in, tmp_out], check=True)
    med = json.load(open(tmp_out))
    problems = []
    heights = {}
    for s in reg:
        h = max(844 if s["mobile"] else 900, int(math.ceil((med[s["file"]]["h"] + 24) / 40.0) * 40))
        heights[s["file"]] = h
        html_ = files[s["file"]].replace("__H__", str(h))
        with open(os.path.join(OUT, s["file"]), "w", encoding="utf-8") as f:
            f.write(html_)
        files[s["file"]] = html_
        if med[s["file"]]["overflow390"] > 0:
            problems.append(f"{s['file']}: rolagem horizontal da página em 390 px ({med[s['file']]['overflow390']} px) {med.get(s['file'] + '#culpado')}")
    # verificações
    names = set(files)
    for fn, h in files.items():
        for href in re.findall(r'href="([^"#]+\.dc\.html)"', h):
            if href not in names:
                problems.append(f"{fn}: link para artboard inexistente {href}")
        if "{{" in h:
            problems.append(f"{fn}: contém '{{{{'")
        if '<script src="./support.js"></script>' not in h:
            problems.append(f"{fn}: falta support.js")
        body = h.split("<x-dc>", 1)[1].rsplit("</x-dc>", 1)[0]
        ck = Checker()
        ck.feed(body)
        if ck.errors or ck.stack:
            problems.append(f"{fn}: HTML malformado {ck.errors[:3]} pilha final {ck.stack[-3:]}")
    linked = set()
    for h in files.values():
        linked.update(re.findall(r'href="([^"#]+\.dc\.html)"', h))
    for fn in names:
        if fn not in linked and fn != "Main.dc.html":
            problems.append(f"{fn}: nenhum outro artboard aponta para ele")
    # canvas.json
    orig = json.load(open(os.path.join(HERE, "canvas_original.json")))
    cv = copy.deepcopy(orig)
    boards = {k: v for k, v in orig["boards"].items() if v.get("page") and v.get("page") != "page-1"}  # preserva artboards de outras páginas
    notes = {}
    y = 0
    order = []
    for rk in ROWS:
        items = [s for s in reg if s["row"] == rk]
        items.sort(key=lambda s: (0 if s["file"] == "Main.dc.html" else 1 if s["ref"].startswith("T01") else 2))
        if not items:
            continue
        x = 0
        maxh = 0
        for s in items:
            w = 390 if s["mobile"] else 1440
            b = dict(x=x, y=y, w=w, h=heights[s["file"]], title=s["title"], is_interactive=True)
            if not s["mobile"]:
                b["expand"] = "fill"
            boards[s["file"]] = b
            order.append(s["file"])
            x += w + 80
            maxh = max(maxh, heights[s["file"]])
        notes[rk] = dict(kind="title1", text=ROWS[rk], x=0, y=y - 280, maxW=max(2400, x - 80), w=240)
        y += maxh + 120 + 300
    notes["legenda"] = dict(text=("Protótipo navegável do Projeto Básico v0.4 (seção 12) — tema escuro de alto contraste; dados fictícios. "
                                  "Cada aba é um artboard e as abas, menus, trilhas e ações apontam umas para as outras: use Play a partir de "
                                  "“T01.A Início — Ação agora”. A ficha de exemplo é a do contrato 012/2025. Rótulos fixos e estados obrigatórios no "
                                  "artboard “Padrões comuns”."), x=-680, y=0, w=560, fill="blue", size=22)
    for k, v in orig["boards"].items():
        if k not in boards:
            pass  # artboards antigos substituídos pelos mesmos nomes; nenhum é removido sem necessidade
    cv["boards"] = boards
    cv["order"] = order + [k for k in orig["order"] if k in boards and k not in order]
    cv["notes"] = notes
    cv["noteOrder"] = list(notes)
    json.dump(cv, open(os.path.join(OUT, "canvas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    removed = [k for k in orig["boards"] if k not in boards]
    total = sum(len(h.encode()) for h in files.values())
    print(f"{len(files)} artboards · {total / 1e6:.2f} MB · removidos do índice: {removed}")
    print("PROBLEMAS:" if problems else "Sem problemas nas verificações automáticas.")
    for pr in problems:
        print(" -", pr)
    json.dump(dict(problems=problems, heights=heights, overflow={k: v["overflow390"] for k, v in med.items() if "#" not in k},
                   culpados={k: v for k, v in med.items() if "#" in k}),
              open(os.path.join(HERE, "..", "verificacao_automatica.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
