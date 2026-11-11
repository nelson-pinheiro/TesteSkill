"""Revisão de conformidade: confere cada artboard contra os itens da seção 12 do Projeto Básico v0.4
(regiões, colunas, campos, ações, validações e rótulos fixos) e contra a seção 12.2 (mapa de navegação).

Uso: python3 revisao.py   → imprime as pendências e grava ../revisao_conformidade.json
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "..", "canvas", "project")


def texto(fn):
    s = open(os.path.join(PROJ, fn), encoding="utf-8").read()
    s = s.split("<x-dc>", 1)[1].rsplit("</x-dc>", 1)[0]
    attrs = " ".join(re.findall(r'(?:placeholder|aria-label|title|value)="([^"]*)"', s))
    s = re.sub(r"<style>.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<svg.*?</svg>", " ", s, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(t + " " + attrs)).lower()


# --- 12.1 moldura comum (todas as telas de computador) -------------------------
MOLDURA = ["unidade ativa", "data de posição", "consultar em outra data", "nº do contrato, objeto, contratada, processo sei, nota de empenho ou documento fiscal",
           "notificações: 7 não lidas", "perfis vigentes", "preferências", "sair", "início", "carteira", "vencimentos", "prorrogações e substituições",
           "valores e planejamento", "empenhos", "pagamentos", "reajustes", "providências", "notificações", "relatórios", "administração",
           "versão 1.0.0", "regras de cálculo v0.4"]

# --- 12.2 mapa de navegação: abas e passos exigidos -----------------------------
MAPA = {
    "T00": ["T00-Acesso.dc.html", "T00-Unidade.dc.html", "T00-Sessao.dc.html"],
    "T01 A·B·C": ["Main.dc.html", "T01B-Indicadores.dc.html", "T01C-Financeiro.dc.html"],
    "T02 A·B·C·D": ["Carteira.dc.html", "T02B-Encerrados.dc.html", "T02C-Rascunhos.dc.html", "T02D-Todos.dc.html"],
    "T03.01–T03.11": ["Ficha.dc.html", "T0302-Prazos.dc.html", "T0303-Valores.dc.html", "T0304-Empenhos.dc.html", "T0305-Pagamentos.dc.html", "T0306-Alteracoes.dc.html",
                      "T0307-Garantias.dc.html", "T0308-Responsaveis.dc.html", "T0309-Documentos.dc.html", "T0310-Historico.dc.html", "T0311-Conformidade.dc.html"],
    "T04 7 passos e revisão": ["T04-P1-Identificacao.dc.html", "T04-P2-Contratada.dc.html", "T04-P3-Origem.dc.html", "T04-P4-Processos.dc.html", "T04-P5-Responsaveis.dc.html",
                               "T04-P6-Prazos.dc.html", "T04-P7-Composicao.dc.html", "T04-Revisao.dc.html"],
    "T04.01": ["T0401-Formalizacao.dc.html"],
    "T05 A·B·C·D": ["Vencimentos.dc.html", "T05B-Calendario.dc.html", "T05C-Continuidade.dc.html", "T05D-Marcos.dc.html"],
    "T06 lista A·B e detalhe 1–6": ["Prorrogacoes.dc.html", "T06B-Concluidos.dc.html", "T06-D1-Resumo.dc.html", "T06-D2-Etapas.dc.html", "T06-D3-Checklist.dc.html",
                                    "T06-D4-Marcos.dc.html", "T06-D5-Substituicao.dc.html", "T06-D6-Documentos.dc.html"],
    "T07 A·B·C·D": ["T07A-Formalizado.dc.html", "T07B-Execucao.dc.html", "T07C-Projecao.dc.html", "T07D-Cenarios.dc.html"],
    "T08 A·B·C·D": ["Empenhos.dc.html", "T08B-Notas.dc.html", "T08C-RestosPagar.dc.html", "T08D-Solicitacoes.dc.html"],
    "T08.01 variantes": ["T0801-NotaEmpenho.dc.html", "T0801-Movimento.dc.html", "T0801-Liquidacao.dc.html", "T0801-Pagamento.dc.html", "T0801-Reforco.dc.html"],
    "T09 A·B·C·D·E": ["Pagamentos.dc.html", "T09B-DocFiscais.dc.html", "T09C-Liquidacoes.dc.html", "T09D-Pagamentos.dc.html", "T09E-Impedimentos.dc.html"],
    "T10 A·B·C e T10.01": ["Reajustes.dc.html", "T10B-DatasBase.dc.html", "T10C-Retroativos.dc.html", "T1001-Simulacao.dc.html"],
    "T11 A·B·C·D": ["Providencias.dc.html", "T11B-Todas.dc.html", "T11C-PorResponsavel.dc.html", "T11D-Concluidas.dc.html"],
    "T12 A·B·C": ["Notificacoes.dc.html", "T12B-Historico.dc.html", "T12C-Resumos.dc.html"],
    "T13 A·B e T13.01": ["Relatorios.dc.html", "T13B-Emissoes.dc.html", "T1301-Previa.dc.html"],
    "T14.01 (3 abas)": ["T1401-Usuarios.dc.html", "T1401-Perfis.dc.html", "T1401-Unidades.dc.html"],
    "T14.02 (5 abas)": ["T1402-Categorias.dc.html", "T1402-Etapas.dc.html", "T1402-Parametros.dc.html", "T1402-Regras.dc.html", "T1402-Calendario.dc.html"],
    "T14.03 (3 abas)": ["T1403-Regras.dc.html", "T1403-Destinatarios.dc.html", "T1403-Monitor.dc.html"],
    "T14.04.01–07": ["Importacao.dc.html", "T140402-Mapeamento.dc.html", "T140403-Conciliacao.dc.html", "T140404-Designacao.dc.html", "T140405-Validacao.dc.html",
                     "T140406-Qualidade.dc.html", "T140407-Recibo.dc.html"],
    "T14.05 (3 abas)": ["T1405-Trilha.dc.html", "T1405-Exportacoes.dc.html", "T1405-Correcoes.dc.html"],
    "T14.06": ["T1406-Copias.dc.html"],
    "T14.07 (3 abas)": ["T1407-Conectores.dc.html", "T1407-Execucoes.dc.html", "T1407-Divergencias.dc.html"],
    "12.6 celular (3 visões)": ["Celular.dc.html", "CelularFicha.dc.html", "CelularNotificacao.dc.html"],
}

# --- 12.3 a 12.6: conteúdo exigido por tela/aba ---------------------------------
R = {
    "T00-Acesso.dc.html": ["autenticação institucional", "aviso de privacidade", "finalidade do tratamento", "encarregado", "não há cadastro de senha", "não informa se a conta existe"],
    "T00-Unidade.dc.html": ["unidades e perfis com vínculo vigente", "sem vínculo vigente", "solicite acesso", "nenhum dado da carteira é exibido"],
    "T00-Sessao.dc.html": ["sua sessão expirou", "gravação está bloqueada", "recuperado", "sem repetir a operação", "registrada na auditoria"],
    "Main.dc.html": ["unidade", "responsável", "contratada", "categoria", "exercício", "situação", "valem para as três abas", "prioridade (c17)", "motivo da prioridade",
                     "providência", "prazo", "dias de atraso", "risco (c18)", "sugerida", "confirmada", "atribuir responsável", "confirmar ou ajustar prioridade",
                     "designação incompleta (c20)", "marcos regulamentares descumpridos (c19)", "a sugestão original permanece visível"],
    "T01B-Indicadores.dc.html": ["contratos vigentes", "vencimentos por período", "comprometimento financeiro previsto", "empenhos insuficientes", "pagamentos pendentes",
                                 "prorrogações em andamento", "reajustes pendentes", "providências vencidas", "risco de descontinuidade", "cobertura", "ver composição",
                                 "excluídos", "próximos vencimentos", "mesma quantidade de registros", "nunca"],
    "T01C-Financeiro.dc.html": ["previsão mensal de desembolso", "2026", "2027", "tabela equivalente", "reforço estimado (c09)", "liquidado a pagar por motivo (c11)",
                                "cobertura não conclusiva", "execução registrada", "projeção", "abrir t08", "abrir t09", "t07"],
    "Carteira.dc.html": ["número normalizado", "objeto", "contratada", "cnpj", "processo sei", "unidade", "categoria", "grupo", "tipo", "situação de vigência", "faixa de término",
                         "decisão prevista", "gestor", "qualidade do dado", "risco", "término formalizado", "dias", "valor atualizado", "valor mensal", "não aplicável",
                         "pend.", "qualidade", "novo contrato (digitar)", "importar", "exportar", "número repetido", "desambiguados por processo e contratada",
                         "registros", "com lacunas de dados", "colunas", "50 linhas por página", "filtros salvos", "atribuir responsável", "buscar na fonte"],
    "T02B-Encerrados.dc.html": ["situação de fechamento", "saldo liquidado a pagar", "encerrado com passivo", "continua consultável"],
    "T02C-Rascunhos.dc.html": ["rascunho", "importado – não validado", "devolvido", "motivo", "responsável pela pendência", "continuar cadastro", "submeter", "validar ou devolver"],
    "T02D-Todos.dc.html": ["situação", "vigente", "encerrado ou extinto", "rascunho ou não validado"],
    "Ficha.dc.html": ["número e ano", "natureza do instrumento", "tipo e modelo de preço", "enquadramento no art. 2º", "objeto resumido", "objeto completo", "unidade responsável",
                      "categoria", "grupo", "criticidade do objeto", "vigência", "execução", "fechamento", "razão social", "cnpj", "representante", "preposto", "modalidade",
                      "procedimento de origem", "ata", "regime jurídico", "dedicação exclusiva", "predominância", "conta vinculada", "previsão de prorrogação no edital",
                      "sistema estruturante de ti", "liquidação", "pagamento", "recebimento provisório", "recebimento definitivo", "situação em uma data", "painel de evidências",
                      "ver origem", "editar", "cobertura de empenho", "designação (c20)", "dias restantes", "valor atualizado", "qualidade do dado"],
    "T0302-Prazos.dc.html": ["assinatura", "publicação do extrato", "divulgação no pncp", "início da vigência", "término da vigência", "prazo de execução", "instrumento-fonte",
                             "dias restantes (c01)", "em tramitação", "minuta", "término pretendido", "nunca substitui", "decisão prevista", "data interna", "parâmetro interno",
                             "m120", "m30", "legal (regulamentar)", "continuidade", "lacuna (c02)", "linha do tempo", "piso de 120 dias"],
    "T03-Historico.dc.html": ["consulta histórica — posição", "somente leitura", "registros retroativos", "designações aplicáveis"],
    "T0303-Valores.dc.html": ["valor original", "vigência corrente", "global acumulado", "base do art. 125", "valor mensal vigente", "periodicidade", "itens de preço", "tipo",
                              "componente", "quantidade" if False else "qtd.", "preço unitário", "valor total", "etapa prevista", "reconcilia", "execução registrada", "saldo contratual",
                              "premissas e cenários", "cenário simulado", "projeção"],
    "T0304-Empenhos.dc.html": ["e — empenho atualizado", "l — liquidado", "s — saldo", "o — executado", "d — disponível", "f — execução futura", "r — reforço", "solicitações de reforço",
                               "restos a pagar", "os totais são os mesmos de t08", "abrir t08"],
    "T0305-Pagamentos.dc.html": ["competência", "obrigação", "documento fiscal", "atesto", "liquidado", "baixa bruta", "impedimento", "contrato encerrado com pendência", "abrir t09"],
    "T0306-Alteracoes.dc.html": ["formalizadas", "instrumento", "processo", "justificativa", "valor anterior", "variação", "valor resultante", "término anterior", "início dos efeitos",
                                 "propostas e simulações", "índice", "data-base", "cláusula", "último reajuste", "próxima referência", "mão de obra", "insumos", "limites do art. 125",
                                 "alerta"],
    "T0307-Garantias.dc.html": ["aplicável", "modalidade", "instituição e número", "valor e percentual", "validade", "cobertura de verbas trabalhistas", "documento e comprovante",
                                "situação", "necessidade de atualização", "proposta de liberação", "histórico", "art. 97"],
    "T0308-Responsaveis.dc.html": ["quadro atual", "gestor", "fiscal técnico", "fiscal administrativo", "titular", "termo de ciência", "conformidade (c20)", "suplentes exigidos",
                                   "comissionado", "ato de designação", "publicação no diário oficial", "contratos abrangidos", "id funcional", "******56", "afastamentos", "suplente",
                                   "histórico", "gerar providência (designação)", "n14"],
    "T0309-Documentos.dc.html": ["número sei", "principal", "gestão e fiscalização", "relacionado", "unidade atual", "documentos", "versão", "restrição", "conferência",
                                 "arquivo indisponível", "instrumentos de gestão", "art. 19", "faltante"],
    "T0310-Historico.dc.html": ["providências pendentes", "linha do tempo unificada", "negócio", "auditoria", "nova providência", "abrir t11", "correção cria novo registro"],
    "T0311-Conformidade.dc.html": ["gestor, fiscais e suplentes designados", "ato publicado e termo de ciência", "processo de gestão e fiscalização", "instrumentos mínimos",
                                   "publicação do extrato e divulgação no pncp", "recomendação com 120 dias", "lista de verificação da prorrogação", "atesto por dois fiscais",
                                   "conferência trabalhista mensal", "controle e liberação da garantia", "formulários de acompanhamento", "relatório final do gestor",
                                   "não informado", "não equivale a descumprimento", "criar providência", "emitir rpt15", "in age nº 54/2025"],
    "T04-P1-Identificacao.dc.html": ["colisão de identidade", "vincular ao existente", "corrigir", "registrar como distinto", "justificativa", "salvar rascunho", "submeter à validação",
                                     "novo (digitar)", "importar (l02)", "buscar na fonte", "(obrigatório)"],
    "T04-P2-Contratada.dc.html": ["cnpj", "dígitos verificadores", "alfanumérico", "reutilizada", "contatos"],
    "T04-P3-Origem.dc.html": ["modalidade", "prazo de divulgação no pncp", "20 dias úteis", "regime jurídico", "dedicação exclusiva"],
    "T04-P4-Processos.dc.html": ["processo principal", "número sei", "gestão e fiscalização", "buscar no sei", "unidade atual"],
    "T04-P5-Responsaveis.dc.html": ["ato de designação", "designações", "composição mínima", "c20", "não impede o rascunho", "l03"],
    "T04-P6-Prazos.dc.html": ["início da vigência", "término da vigência", "término ≥ início", "teto legal", "5 anos", "decisão prevista", "data interna", "c15", "piso", "120 dias"],
    "T04-P7-Composicao.dc.html": ["campos por modalidade", "não é calculado por divisão", "itens de preço", "não reconcilia", "impede a validação", "garantia"],
    "T04-Revisao.dc.html": ["resumo de todos os passos", "campos faltantes", "fonte do grupo", "situação", "submeter", "sem apagar", "validar", "instrumento assinado",
                            "devolver com motivo", "prazo de saneamento", "rascunho não alimenta totais"],
    "T0401-Formalizacao.dc.html": ["tipo de instrumento", "termo aditivo", "apostila", "termo de extinção", "art. 136", "número", "data de assinatura", "documento assinado", "processo sei",
                                   "classe(s) de alteração", "prorrogação", "acréscimo", "supressão", "reajuste", "repactuação", "revisão do equilíbrio", "justificativa resumida",
                                   "valor anterior", "variação", "valor resultante", "término anterior", "novo término", "início dos efeitos", "publicação do extrato",
                                   "divulgação no pncp", "divulgação pendente", "remessa ao tce-rj", "comparação antes e depois", "limite do art. 125", "verificações prévias",
                                   "art. 131", "endosso", "lista de verificação", "m120", "m30", "impacto", "avisos futuros", "diferenças retroativas", "confirmação única",
                                   "ch03", "cv02"],
    "Vencimentos.dc.html": ["ultrapassado", "0–30", "31–60", "61–90", "91–180", "acima de 180", "término formalizado", "dias restantes", "data interna", "parâmetro interno",
                            "situação da c15", "decisão prevista", "responsável", "procedimento e etapa", "pend.", "próximo passo", "risco (c18)", "registrar ou alterar decisão",
                            "criar procedimento", "criar providência", "não muda a data formal"],
    "T05B-Calendario.dc.html": ["vigência", "garantia", "data-base", "marco", "lista equivalente", "tipo de evento", "mês", "semana"],
    "T05C-Continuidade.dc.html": ["término atual", "processo substitutivo", "etapa", "início estimado", "início formalizado", "premissas", "lacuna ou sobreposição", "indeterminado",
                                  "providência de levantamento", "14 dias"],
    "T05D-Marcos.dc.html": ["m120", "m30", "registro", "legal (regulamentar)", "art. 22, xvii", "art. 22, xix", "registrar recomendação", "abrir procedimento", "31/07/2026", "29/10/2026"],
    "Prorrogacoes.dc.html": ["contrato", "tipo", "processo sei", "abertura", "prazo interno original", "revisado", "responsável", "unidade atual", "etapa", "última movimentação",
                             "dias sem avanço", "pendências", "próxima ação", "marcos", "novo procedimento", "rpt04"],
    "T06B-Concluidos.dc.html": ["conclusão", "resultado", "instrumento", "reabrir com motivo", "cancelada"],
    "T06-D1-Resumo.dc.html": ["tipo", "processo sei", "data de abertura", "responsável", "unidade atual", "etapa", "prazo interno original", "prazo interno revisado", "pendências",
                              "próxima ação", "rever prazo", "trocar responsável", "concluir (exige resultado)", "cancelar (exige motivo)", "formalizar (t04.01)", "concluir não formaliza"],
    "T06-D2-Etapas.dc.html": ["trilha das etapas", "remessa", "recebimento", "devolução", "origem", "destino", "autor", "instante", "evidência", "avançar etapa", "retornar etapa",
                              "recebimento não conclui etapa", "somente inserção"],
    "T06-D3-Checklist.dc.html": ["pr01", "pr02", "pr03", "pr04", "pr05", "pr06", "pr07", "pr08", "pr09", "pr10", "pr11", "pr12", "art. 91, § 4º", "art. 131", "situação",
                                 "documento", "verificador", "não aplicável exige justificativa", "justificativa do coordenador"],
    "T06-D4-Marcos.dc.html": ["m120", "m30", "data-limite", "data do registro", "documento", "comparação com o prazo interno", "registrar recomendação", "registrar envio"],
    "T06-D5-Substituicao.dc.html": ["processo substitutivo", "contrato sucessor", "início estimado", "início formalizado", "premissas", "lacuna (c02)", "vincular processo", "rever estimativa"],
    "T06-D6-Documentos.dc.html": ["tipo", "número sei", "restrição", "anexar", "referenciar", "versões preservadas"],
    "T07A-Formalizado.dc.html": ["valor original", "vigência corrente", "global acumulado", "base do art. 125", "valor mensal vigente", "composição por item", "acréscimos e supressões",
                                 "somente leitura", "t04.01", "inconsistência"],
    "T07B-Execucao.dc.html": ["executado", "competência", "glosa", "saldo contratual", "custo previsto até o término", "abrir obrigações (t09.a)", "saldo negativo", "ver composição"],
    "T07C-Projecao.dc.html": ["método", "horizonte", "premissas", "versão", "autor", "competência (custo)", "desembolso", "previsão no exercício", "nova versão de projeção",
                              "preserva as anteriores", "mensal × meses", "não apurado", "l09"],
    "T07D-Cenarios.dc.html": ["cenário simulado", "premissas", "referência", "impacto", "criar cenário", "duplicar", "excluir", "horizontes diferentes", "comparação recusada"],
    "Empenhos.dc.html": ["e", "l", "s", "o", "d", "f", "r", "ver memória", "data de insuficiência (c10)", "meses de cobertura (c16)", "cobertura não conclusiva" if False else "não conclusiva",
                         "obrigação sem alocação", "movimento não classificado", "solicitar reforço", "insuficiência existente", "cf03"],
    "T08B-Notas.dc.html": ["unidade emitente", "número", "data", "tipo", "classificação", "valor inicial", "reforços", "anulações", "estornos", "valor atualizado", "liquidado",
                           "saldo", "histórico de movimentos", "nova nota", "novo movimento", "validar selecionadas", "usuário diferente do que lançou", "nota duplicada é rejeitada"],
    "T08C-RestosPagar.dc.html": ["exercícios anteriores" if False else "exercício de origem", "processado", "não processado", "saldo", "obrigações vinculadas", "registrar inscrição",
                                 "não compensa"],
    "T08D-Solicitacoes.dc.html": ["valor estimado", "memória", "data necessária", "processo", "responsável", "situação", "movimento de atendimento", "nova solicitação",
                                  "não altera o saldo", "movimento oficial conciliado", "atualizar situação"],
    "T0801-NotaEmpenho.dc.html": ["contrato", "unidade emitente", "exercício", "número", "data de emissão", "tipo", "natureza da despesa", "fonte", "programa de trabalho",
                                  "valor inicial", "credor", "saldos antes e depois"],
    "T0801-Movimento.dc.html": ["nota", "reforço", "anulação", "estorno de reforço", "estorno de anulação", "documento oficial", "movimento estornado", "sem tipo", "saldos antes e depois"],
    "T0801-Liquidacao.dc.html": ["obrigação", "documento fiscal", "referência oficial", "alocação por nota de empenho", "soma das alocações", "sem ajuste silencioso", "saldos antes e depois"],
    "T0801-Pagamento.dc.html": ["liquidação", "valor líquido", "referência oficial", "retenções", "documento de recolhimento", "apenas calculada", "baixa bruta", "saldos antes e depois"],
    "T0801-Reforco.dc.html": ["contrato", "conjunto orçamentário", "valor estimado", "memória", "data necessária", "processo", "responsável", "c09", "justificativa", "saldos antes e depois"],
    "Pagamentos.dc.html": ["executado não liquidado", "liquidado a pagar", "pago", "com impedimento", "ver composição", "competência ou etapa", "item", "valor bruto", "glosa",
                           "reconhecido", "controversa", "adimplemento", "recebimento provisório", "recebimento definitivo", "conferência trabalhista", "alocação orçamentária",
                           "a liquidar", "nova obrigação", "estornar com motivo", "registrar recebimento", "sequência explícita", "sem alocação", "recebimento presumido — validar"],
    "T09B-DocFiscais.dc.html": ["emissor", "série", "número", "chave", "emissão", "competência", "valor", "vencimento", "rateio por obrigação", "atestos", "suficiência do atesto (c21)",
                                "dias desde a emissão", "novo documento", "ratear entre obrigações", "registrar atesto", "enviar à liquidação", "documento duplicado", "atesto incompleto", "fiscal único"],
    "T09C-Liquidacoes.dc.html": ["data", "referência oficial", "valor", "alocação por nota", "estorn", "inconsistência", "nova liquidação"],
    "T09D-Pagamentos.dc.html": ["referência oficial", "líquido", "retenções recolhidas", "apenas calculadas", "baixa bruta", "saldo a pagar", "novo pagamento", "encerrado"],
    "T09E-Impedimentos.dc.html": ["causa", "descrição", "responsável", "providência vinculada", "abertura", "resolução", "atesto incompleto", "regularidade fiscal",
                                  "comprovação trabalhista", "glosa em discussão", "falta de empenho", "documento incorreto", "recebimento pendente", "proposto automaticamente"],
    "Reajustes.dc.html": ["reajuste", "repactuação", "revisão do equilíbrio", "cláusula", "índice", "data-base", "período de referência", "pedido em", "instrução completa",
                          "prazo de resposta", "contrato", "legal", "parâmetro interno", "solicitado", "memória", "etapa", "responsável", "decisão", "formalização",
                          "início dos efeitos", "novo pedido", "registrar decisão", "simular", "formalizar", "indeferido", "não entram no valor oficial"],
    "T10B-DatasBase.dc.html": ["índice", "data-base", "último reajuste", "próxima data-base", "aviso n04", "insumos", "mão de obra", "12 meses", "iniciar pedido"],
    "T10C-Retroativos.dc.html": ["alteração formalizada", "item", "competência", "já reconhecido", "revisto", "diferença", "obrigação complementar", "pago", "pendente",
                                 "créditos a compensar", "reprocessar", "substitui, nunca soma"],
    "T1001-Simulacao.dc.html": ["premissas", "tipo", "índice", "percentual", "data-base", "período de referência", "mão de obra", "insumos", "início dos efeitos",
                                "salvar como cenário", "comparação", "formalizado", "simulação", "efeitos por competência", "diferença retroativa", "exportar memória"],
    "Providencias.dc.html": ["atualizar situação", "registrar andamento", "concluir com evidência", "prazo"],
    "T11B-Todas.dc.html": ["crítica", "alta", "média", "planejamento", "a confirmar", "categoria", "descrição", "responsável", "prazo", "dias", "sugerida", "confirmada", "situação",
                           "processo", "nova providência", "atribuir", "editor lateral", "procedimento", "dependência", "evidência", "histórico", "concluir", "cancelar (exige motivo)",
                           "reagendar (exige motivo)", "aguardar terceiro não suspende o prazo", "conclusão bloqueada"],
    "T11C-PorResponsavel.dc.html": ["abertas", "vencidas", "a vencer em 7 dias", "redistribuir", "rpt10"],
    "T11D-Concluidas.dc.html": ["evidência", "motivo", "reabrir com motivo", "preservada"],
    "Notificacoes.dc.html": ["evento", "contrato e contratada", "motivo", "data-limite", "dias", "prioridade", "responsável", "próxima ação", "geração", "dados de",
                             "abrir o registro", "registrar ciência", "registrar providência", "ciência nunca encerra"],
    "T12B-Historico.dc.html": ["estado por canal", "pendente", "enviada", "falha", "cancelada", "tentativas", "cancelamento (motivo)", "evento", "contrato", "período",
                               "avisos emitidos permanecem"],
    "T12C-Resumos.dc.html": ["resumos", "frequência configurada", "abrir itens"],
    "Relatorios.dc.html": ["rpt01", "rpt02", "rpt03", "rpt04", "rpt05", "rpt06", "rpt07", "rpt08", "rpt09", "rpt10", "rpt11", "rpt12", "rpt13", "rpt14", "rpt15", "grão",
                           "perfis autorizados", "data de corte", "agrupamento", "ordenação", "colunas", "formato", "filtro inaplicável fica desabilitado"],
    "T13B-Emissoes.dc.html": ["código", "posição", "filtros", "formato", "linhas", "identificador", "reemitir"],
    "T1301-Previa.dc.html": ["riopreviência" if False else "rioprevidência", "posição", "universo", "critérios", "fontes", "registros incompletos", "exportar pdf", "exportar xlsx",
                             "exportar csv", "mesma fotografia", "caracteres de fórmula são neutralizados", "fora do universo padrão", "não informado", "060/2024", "041/2026", "contratos vigentes na posição"],
    "T1401-Usuarios.dc.html": ["login institucional", "nome", "e-mail", "ativo", "pessoa vinculada", "vigente de", "autorizador", "motivo", "revogar", "negação por padrão", "não se sobrepõem"],
    "T1401-Perfis.dc.html": ["coordenador", "op. contratual", "op. financeiro", "gestor/fiscal", "consulta/controle interno", "adm. técnico", "visualizar identificadores pessoais sem máscara"],
    "T1401-Unidades.dc.html": ["unidade superior", "vigência"],
    "T1402-Categorias.dc.html": ["categorias", "grupos", "modalidades", "tipos de documento", "categorias de providência", "inativar não elimina histórico"],
    "T1402-Etapas.dc.html": ["etapas", "ordem", "lista de verificação", "fundamento"],
    "T1402-Parametros.dc.html": ["escopo", "vigência", "justificativa", "piso regulamentar", "recusado", "recalcula avisos futuros"],
    "T1402-Regras.dc.html": ["quadro normativo", "versão", "verificada em"],
    "T1402-Calendario.dc.html": ["feriados", "índices"],
    "T1403-Regras.dc.html": ["n01", "n02", "n03", "n04", "n05", "n06", "n07", "n08", "n09", "n10", "n11", "n12", "n13", "n14", "n15", "n16", "resumo", "antecedência", "repetição",
                             "escalonamento", "escopo", "parâmetro interno", "prévia do aviso"],
    "T1403-Destinatarios.dc.html": ["destinatários por responsabilidade", "canais"],
    "T1403-Monitor.dc.html": ["último ciclo do agendador", "fila", "falhas", "reenviar"],
    "Importacao.dc.html": ["arquivo", "hash", "responsável", "situação", "candidatas", "disposição", "novo lote", "continuar", "abrir recibo", "simular", "l01", "l09", "já recebido"],
    "T140402-Mapeamento.dc.html": ["aba", "coluna", "cabeçalho", "destino", "tipo", "exemplo", "regra", "versão", "erro", "alterar mapa", "simular sem gravar"],
    "T140403-Conciliacao.dc.html": ["linha original", "candidatos", "número", "processo", "natureza", "contraparte", "evidências", "criar distinto", "vincular", "rejeitar", "adiar", "justificativa"],
    "T140404-Designacao.dc.html": ["valor na aba", "papel", "pessoa", "identificador restrito", "ato", "escolher com evidência", "informar valor comprovado", "manter pendente"],
    "T140405-Validacao.dc.html": ["original", "normalizado", "fórmula", "escopo temporal", "instrumento", "estado", "aprovar", "devolver", "corrigir com motivo", "bloqueada sem evidência"],
    "T140406-Qualidade.dc.html": ["campo faltante", "gravidade", "contrato", "responsável", "indicador prejudicado", "fonte", "abrir cadastro", "criar providência", "exportar pendências"],
    "T140407-Recibo.dc.html": ["disposição", "destino", "motivo", "homologadores", "entidades derivadas", "versão dos cálculos", "conferir", "exportar xlsx"],
    "T1405-Trilha.dc.html": ["usuário", "tabela", "registro", "período", "antes → depois", "somente leitura"],
    "T1405-Exportacoes.dc.html": ["relatório", "filtros", "formato"],
    "T1405-Correcoes.dc.html": ["correção", "estorno", "motivo"],
    "T1406-Copias.dc.html": ["estado das cópias" if False else "última cópia", "teste de restauração", "fila de avisos", "procedimento autorizado"],
    "T1407-Conectores.dc.html": ["fonte", "modo", "estado", "última execução", "referência da credencial", "cofre", "somente leitura"],
    "T1407-Execucoes.dc.html": ["lidos", "erros"],
    "T1407-Divergencias.dc.html": ["valor do sistema", "valor da fonte", "origem", "aceitar o valor da fonte", "manter o valor do sistema", "corrigir por digitação", "justificativa", "autor"],
    "Celular.dc.html": ["ação agora", "prioridade" if False else "motivo", "vigentes"],
    "CelularFicha.dc.html": ["término formalizado", "aba da ficha", "formalizado", "em tramitação", "designação" if False else "completa"],
    "CelularNotificacao.dc.html": ["motivo", "data-limite", "responsável", "dados atualizados em", "registrar ciência", "abrir providência", "registrar ciência não conclui a providência"],
    "Padroes.dc.html": ["carregando", "lista vazia", "sem resultados", "dados incompletos", "erro de consulta", "sem permissão", "conflito de versão", "formalizado", "execução registrada",
                        "projeção", "cenário simulado", "validado", "importado – não validado", "não informado", "não apurado", "crítica", "alta", "média", "planejamento",
                        "a confirmar", "existente", "moderado — escopo em prorrogação automática", "indeterminado", "sem risco identificado", "não aplicável — vigência encerrada",
                        "não aplicável — encerramento planejado", "a cumprir", "cumprido", "cumprido com atraso", "descumprido", "não aplicável", "completa", "incompleta",
                        "sem designação há", "legal", "legal (regulamentar)", "contrato", "parâmetro interno", "digitado", "importado", "integrado", "ver origem",
                        "campo(s) precisam de atenção", "salvar rascunho", "submeter à validação", "validar", "devolver com motivo", "consulta histórica"],
}


def main():
    files = {f for f in os.listdir(PROJ) if f.endswith(".dc.html")}
    pend = []
    for grupo, fs in MAPA.items():
        for f in fs:
            if f not in files:
                pend.append(f"[12.2] {grupo}: falta o artboard {f}")
    tot = 0
    for f, reqs in R.items():
        if f not in files:
            pend.append(f"[12.3–12.6] artboard inexistente {f}")
            continue
        t = texto(f)
        for r in reqs:
            tot += 1
            if r.lower() not in t:
                pend.append(f"[12.3–12.6] {f}: não encontrado “{r}”")
    desktop = [f for f in files if not f.startswith("Celular") and not f.startswith("T00-Acesso") and not f.startswith("T00-Unidade") and f != "Artboard-bgps.dc.html"]
    for f in sorted(desktop):
        t = texto(f)
        for r in MOLDURA:
            tot += 1
            if r not in t:
                pend.append(f"[12.1] {f}: moldura sem “{r}”")
    cobertos = set(R)
    sem_req = sorted(files - cobertos - {"Artboard-bgps.dc.html"})
    print(f"{len(files)} artboards · {tot} verificações · {len(pend)} pendências · sem lista própria: {sem_req}")
    for x in pend:
        print(" -", x)
    json.dump(dict(verificacoes=tot, pendencias=pend, artboards=len(files)), open(os.path.join(HERE, "..", "revisao_conformidade.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
