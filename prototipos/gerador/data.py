"""Massa fictícia comum a todas as telas (nenhum nome real de pessoa ou empresa).

Datas calculadas pelas regras C01, C15 e C19 a partir da posição 10/11/2026,
para que prazos, marcos e faixas fiquem coerentes entre as telas.
"""
from core import POSICAO, d, fmt, dias_restantes, menos
import datetime as dt


def cnpj(base12):
    """CNPJ com dígitos verificadores (aceita o formato alfanumérico — valor = código ASCII − 48)."""
    vals = [ord(c) - 48 for c in base12]
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    s = sum(v * w for v, w in zip(vals, w1)) % 11
    d1 = 0 if s < 2 else 11 - s
    w2 = [6] + w1
    s = sum(v * w for v, w in zip(vals + [d1], w2)) % 11
    d2 = 0 if s < 2 else 11 - s
    c = base12 + f"{d1}{d2}"
    return f"{c[0:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:14]}"


ANTECEDENCIA = {"Prorrogar": 120, "Substituir": 240, "Encerrar": 60, "Analisar": 240}

# n, contratada, base CNPJ, objeto, unidade, tipo, modelo, início, término, decisão, risco, valor, mensal, gestor, qualidade, designação, pendências
_RAW = [
    ("012/2025", "Alfa Serviços Prediais Ltda", "123456780001", "Manutenção predial preventiva e corretiva", "GERAD", "Serviço contínuo", "Mensal fixo",
     "29/11/2025", "28/11/2026", "Prorrogar", "Alto", "1.074.400,00", "91.800,00", "P. Nunes", "Validado", "Completa (4 apontamentos)", 5),
    ("027/2024", "Gama Vigilância Ltda", "234567890001", "Vigilância patrimonial armada e desarmada", "GERAD", "Serviço contínuo", "Mensal fixo",
     "06/11/2024", "05/11/2026", "Prorrogar", "Existente", "2.880.000,00", "240.000,00", "P. Nunes", "Validado", "Completa", 4),
    ("031/2023", "Beta Tecnologia S.A.", "345678900001", "Suporte técnico e sustentação de TI", "GERTIC", "Serviço contínuo", "Mensal fixo",
     "01/04/2023", "31/03/2027", "Substituir", "Alto", "1.560.000,00", "130.000,00", "A. Lima", "Validado", "Completa", 2),
    ("044/2023", "Épsilon Elevadores Ltda", "456789010001", "Manutenção de elevadores (por medição)", "GERAD", "Serviço contínuo", "Medição",
     "15/06/2023", "14/06/2027", "Prorrogar", "Sem risco identificado", "612.000,00", "Não aplicável", "P. Nunes", "Validado", "Completa", 1),
    ("019/2025", "Delta Copeiragem Ltda", "567890120001", "Copeiragem com dedicação exclusiva de mão de obra", "GERAD", "Serviço contínuo", "Mensal fixo",
     "01/07/2025", "30/06/2027", "Prorrogar", "Sem risco identificado", "744.000,00", "62.000,00", "G. Freitas", "Validado", "Completa", 2),
    ("038/2024", "Kapa Construções Ltda", "678901230001", "Reforma do arquivo central (obra por escopo)", "GERAD", "Escopo", "Etapas",
     "01/11/2024", "30/10/2026", "Analisar", "Moderado — escopo em prorrogação automática", "480.000,00", "Não aplicável", "P. Nunes", "Validado", "Completa", 1),
    ("041/2026", "Lambda Software Ltda", "789012340001", "Licenças de software de gestão documental", "GERTIC", "Fornecimento", "Quantidades",
     "01/08/2026", "31/07/2027", "Não informada", "Indeterminado", "318.000,00", "Não aplicável", "—", "Validado", "Sem designação há 101 dias", 3),
    ("052/2025", "Ômicron Suprimentos Ltda", "890123450001", "Material de expediente (fornecimento por quantidades)", "DIRAF", "Fornecimento", "Quantidades",
     "16/12/2025", "15/12/2026", "Encerrar", "Não aplicável — encerramento planejado", "115.000,00", "Não aplicável", "L. Teixeira", "Validado", "Completa", 0),
    ("060/2024", "Sigma Climatização Ltda", "901234560001", "Manutenção de ar-condicionado", "GERAD", "Serviço contínuo", "Mensal fixo",
     "01/06/2024", "31/05/2027", "Prorrogar", "Sem risco identificado", "125.000,00", "10.500,00", "P. Nunes", "Validado", "Completa", 1),
    ("021/2025", "Zeta Serviços de Limpeza Ltda", "112233440001", "Limpeza e conservação predial", "DIRSE", "Serviço contínuo", "Mensal fixo",
     "01/05/2025", "30/04/2027", "Prorrogar", "Sem risco identificado", "1.428.000,00", "119.000,00", "S. Moura", "Validado", "Completa", 0),
    ("021/2025", "Eta Transportes Ltda", "223344550001", "Locação de veículos com motorista (carta-contrato)", "CHEGAB", "Serviço contínuo", "Mensal fixo",
     "01/09/2025", "31/08/2027", "Não informada", "Indeterminado", "396.000,00", "33.000,00", "T. Vieira", "Importado – não validado", "Incompleta há 40 dias", 2),
    ("033/2025", "Mu Comunicação Ltda", "334455660001", "Clipping e monitoramento de mídia", "CHEGAB", "Serviço contínuo", "Mensal fixo",
     "19/02/2025", "18/02/2027", "Substituir", "Moderado", "216.000,00", "18.000,00", "T. Vieira", "Validado", "Completa", 2),
    ("047/2024", "Nu Telecom S.A.", "445566770001", "Telefonia fixa e enlaces de dados", "GERTIC", "Serviço contínuo", "Mensal fixo",
     "23/01/2024", "22/01/2027", "Prorrogar", "Alto", "540.000,00", "45.000,00", "A. Lima", "Validado", "Completa", 2),
    ("025/2023", "Xi Reprografia Ltda", "556677880001", "Reprografia e digitalização", "DIRAF", "Serviço contínuo", "Mensal fixo",
     "01/01/2023", "31/12/2026", "Substituir", "Moderado", "264.000,00", "22.000,00", "L. Teixeira", "Validado", "Completa", 0),
]

SEI = {"012/2025": "SEI-040014/000418/2025", "027/2024": "SEI-040014/000233/2024", "031/2023": "SEI-040014/000120/2023",
       "044/2023": "SEI-040014/000301/2023", "019/2025": "SEI-040014/000277/2025", "038/2024": "SEI-040014/000519/2024",
       "041/2026": "SEI-040014/000604/2026", "052/2025": "SEI-040014/000702/2025", "060/2024": "SEI-040014/000188/2024",
       "021/2025|Zeta": "SEI-040014/000315/2025", "021/2025|Eta": "SEI-040014/000877/2025", "033/2025": "SEI-040014/000098/2025",
       "047/2024": "SEI-040014/000041/2024", "025/2023": "SEI-040014/000502/2022"}


def _sei(n, ctda):
    return SEI.get(f"{n}|{ctda.split()[0]}", SEI.get(n, "—"))


def c15(c):
    if c["dec"] == "Não informada":
        return None, "A confirmar"
    if c["tipo"] == "Escopo":
        return None, "Não aplicável — escopo"
    ant = ANTECEDENCIA[c["dec"]]
    di = d(c["fim"]) - dt.timedelta(days=ant)
    proc = PROC_ABERTO.get(c["n"])
    if proc:
        sit = "Em andamento" if d(proc) <= di else "Em andamento após o prazo interno"
    elif c["n"] == "025/2023":
        sit = "Concluída (sucessora formalizada)"
    else:
        sit = "A iniciar" if POSICAO <= di else f"Atrasada há {(POSICAO - di).days} dias"
    return fmt(di), sit


PROC_ABERTO = {"012/2025": "15/07/2026", "027/2024": "20/06/2026", "031/2023": "05/08/2026", "033/2025": "28/10/2026",
               "047/2024": "02/10/2026", "052/2025": "10/10/2026"}

REGISTRO_M120 = {"012/2025": "31/07/2026", "027/2024": "01/07/2026", "025/2023": "20/04/2026"}
REGISTRO_M30 = {"012/2025": "05/11/2026"}


def marco_sit(limite, registro, aplicavel=True):
    if not aplicavel:
        return "Não aplicável"
    if registro:
        return "Cumprido" if d(registro) <= d(limite) else "Cumprido com atraso"
    return "A cumprir" if POSICAO <= d(limite) else "Descumprido"


def marcos(c):
    aplic120 = c["dec"] not in ("Encerrar",) and c["tipo"] != "Escopo"
    aplic30 = c["dec"] == "Prorrogar" and c["tipo"] != "Escopo"
    m120, m30 = menos(c["fim"], 120), menos(c["fim"], 30)
    r120, r30 = REGISTRO_M120.get(c["n"]), REGISTRO_M30.get(c["n"])
    return dict(m120=m120, r120=r120, s120=marco_sit(m120, r120, aplic120), m30=m30, r30=r30, s30=marco_sit(m30, r30, aplic30))


def faixa(dias):
    if dias < 0:
        return "Ultrapassado"
    if dias <= 30:
        return "0–30 dias"
    if dias <= 60:
        return "31–60 dias"
    if dias <= 90:
        return "61–90 dias"
    if dias <= 180:
        return "91–180 dias"
    return "Acima de 180 dias"


CONTRATOS = []
for r in _RAW:
    c = dict(zip(["n", "ctda", "cnpjb", "obj", "un", "tipo", "modelo", "ini", "fim", "dec", "risco", "valor", "mensal", "gestor",
                  "qual", "desig", "pend"], r))
    c["cnpj"] = cnpj(c["cnpjb"])
    c["dias"] = dias_restantes(c["fim"])
    c["sei"] = _sei(c["n"], c["ctda"])
    c["faixa"] = faixa(c["dias"])
    c["c15_data"], c["c15_sit"] = c15(c)
    c.update(marcos(c))
    if c["n"] == "027/2024":
        c["sit"] = "Data final ultrapassada — validar formalização"
    elif c["n"] == "038/2024":
        c["sit"] = "Prorrogada automaticamente — escopo não concluído (art. 111)"
    else:
        c["sit"] = "Em vigor"
    CONTRATOS.append(c)


def C(n, ctda=None):
    for c in CONTRATOS:
        if c["n"] == n and (ctda is None or c["ctda"].startswith(ctda)):
            return c
    raise KeyError(n)


ENCERRADOS = [
    dict(n="015/2022", ctda="Teta Limpeza e Conservação Ltda", obj="Limpeza e conservação (contrato anterior)", un="GERAD", tipo="Serviço contínuo",
         sit="Encerrado", fim="30/09/2026", fech="Pendências financeiras", lap="2.000,00", valor="1.140.000,00", mensal="95.000,00",
         risco="Não aplicável — vigência encerrada", qual="Validado", gestor="G. Freitas"),
    dict(n="017/2024", ctda="Rho Eventos Ltda", obj="Organização de eventos institucionais (sob demanda)", un="CHEGAB", tipo="Serviço contínuo",
         sit="Extinto antecipadamente", fim="15/06/2026", fech="Pendências administrativas", lap="0,00", valor="180.000,00", mensal="Não aplicável",
         risco="Não aplicável — vigência encerrada", qual="Validado", gestor="T. Vieira"),
    dict(n="009/2023", ctda="Pi Jardinagem Ltda", obj="Jardinagem e paisagismo", un="GERAD", tipo="Serviço contínuo",
         sit="Encerrado", fim="31/03/2026", fech="Encerrado administrativamente", lap="0,00", valor="96.000,00", mensal="8.000,00",
         risco="Não aplicável — vigência encerrada", qual="Validado", gestor="P. Nunes"),
]

PESSOAS = {
    "M. Silva": "Coordenadora · GERAD (usuária da sessão)", "R. Costa": "Operador contratual · GERAD",
    "L. Martins": "Operadora financeira · DIRAF", "P. Nunes": "Gestor · GERAD", "J. Prado": "Fiscal técnico · GERAD",
    "F. Dias": "Fiscal administrativo · GERAD", "A. Lima": "Gestor · GERTIC", "T. Vieira": "Gestor · CHEGAB",
    "C. Ramos": "Fiscal administrativo · GERAD", "G. Freitas": "Gestor · GERAD", "L. Teixeira": "Gestora · DIRAF",
    "S. Moura": "Gestora · DIRSE",
}
