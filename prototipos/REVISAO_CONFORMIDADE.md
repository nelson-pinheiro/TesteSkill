# Protótipos de tela — revisão de conformidade com o Projeto Básico v0.4

**Publicação.** https://claude.ai/artifact/CaBDHKNLAAgPuyQWMBRZbP (artefato privado do proprietário; versão 8).

**Objeto.** Refatoração dos 14 protótipos da v0.3 e criação dos que faltavam, para cobrir **todas as telas, abas, passos e subvisões** da seção 12 do *Projeto básico do sistema de controle de contratos do Rioprevidência* (versão 0.4, 10/11/2026), publicados como protótipo navegável no artefato *Protótipos — Sistema de Gestão de Contratos*.

**Resultado.** 104 artboards (101 de computador e 3 de celular), todos ligados entre si por menu lateral, abas, trilha de navegação, cabeçalho e ações. A revisão automática executa **3.343 verificações** (seção 12 e moldura comum da seção 12.1) e termina com **0 pendências**; a verificação de navegação confirma que todos os links apontam para artboards existentes e que nenhuma tela fica sem link de entrada.

| Item | Quantidade |
| --- | --- |
| Artboards de computador | 101 (incluindo T00, a consulta histórica e o artboard “Padrões comuns”) |
| Artboards de celular (seção 12.6) | 3 — Ação agora, Ficha, Notificação |
| Verificações de conteúdo por tela (seções 12.3 a 12.6) | 1.165 |
| Verificações da moldura comum (seção 12.1) em cada tela de computador | 2.178 |
| Pendências na última rodada | 0 |

## 1 Fontes usadas

- `Projeto_Basico_Sistema_Contratos_Rioprevidencia_v0_4.md`: seções 7 (regras C01 a C22, risco C18, prioridade C17, indicadores 7.7), 9 (eventos N01 a N16), 10 (perfis e matriz 10.2), 12 (telas, abas e formulários), 13 (RPT01 a RPT15), 14 (casos de aceite), 16 (leiautes L01 a L09) e Anexo B (referência visual).
- `modelo_dados_v0_4.sql`: dados de referência (seis perfis, vinte permissões, etapas da prorrogação, itens PR01 a PR12, categorias de providência, regras jurídicas e parâmetros da C15).
- `testes_modelo_dados_v0_4.sql` e seção 14.1: os valores dos exemplos reproduzem os casos de aceite (CF03, CF04, CF05, CF06, CF07, CF11, CF12, CF14, CV01, CV05, CV06, CV07, CD01, CD02, CD05, CD06, CH01, CH02, CH03, CR02, CR03, CR04, CN02, CN06, CN07, CN15, CN19, CN23, CE04, CEN03 a CEN06).
- `dicionario_dados_v0_4.md` e diagrama de alto nível: nomes de tabelas e visões citados nas telas.

## 2 Matriz: mapa de navegação (12.2) → artboards

| Tela e abas exigidas | Artboards | Itens verificados |
| --- | --- | --- |
| T00 | `T00-Acesso.dc.html` — T00 Acesso — entrada<br>`T00-Unidade.dc.html` — T00 Seleção de unidade<br>`T00-Sessao.dc.html` — T00 Sessão expirada | 15 |
| T01 A·B·C | `Main.dc.html` — T01.A Início — Ação agora<br>`T01B-Indicadores.dc.html` — T01.B Indicadores da carteira<br>`T01C-Financeiro.dc.html` — T01.C Painel financeiro | 47 |
| T02 A·B·C·D | `Carteira.dc.html` — T02.A Carteira — Vigentes<br>`T02B-Encerrados.dc.html` — T02.B Carteira — Encerrados e extintos<br>`T02C-Rascunhos.dc.html` — T02.C Carteira — Rascunhos e não validados<br>`T02D-Todos.dc.html` — T02.D Carteira — Todos | 50 |
| T03.01–T03.11 | `Ficha.dc.html` — T03.01 Ficha — Identificação, contratada e origem<br>`T0302-Prazos.dc.html` — T03.02 Ficha — Prazos e continuidade<br>`T0303-Valores.dc.html` — T03.03 Ficha — Valores e composição<br>`T0304-Empenhos.dc.html` — T03.04 Ficha — Empenhos<br>`T0305-Pagamentos.dc.html` — T03.05 Ficha — Documentos fiscais e pagamentos<br>`T0306-Alteracoes.dc.html` — T03.06 Ficha — Alterações e reajustes<br>`T0307-Garantias.dc.html` — T03.07 Ficha — Garantias e seguros<br>`T0308-Responsaveis.dc.html` — T03.08 Ficha — Responsáveis e designações<br>`T0309-Documentos.dc.html` — T03.09 Ficha — Documentos e processos<br>`T0310-Historico.dc.html` — T03.10 Ficha — Providências e histórico<br>`T0311-Conformidade.dc.html` — T03.11 Ficha — Conformidade da gestão e fiscalização | 187 |
| T04 7 passos e revisão | `T04-P1-Identificacao.dc.html` — T04 Passo 1 — Identificação<br>`T04-P2-Contratada.dc.html` — T04 Passo 2 — Contratada<br>`T04-P3-Origem.dc.html` — T04 Passo 3 — Origem e regime<br>`T04-P4-Processos.dc.html` — T04 Passo 4 — Processos<br>`T04-P5-Responsaveis.dc.html` — T04 Passo 5 — Responsáveis<br>`T04-P6-Prazos.dc.html` — T04 Passo 6 — Prazos<br>`T04-P7-Composicao.dc.html` — T04 Passo 7 — Composição financeira<br>`T04-Revisao.dc.html` — T04 Revisão — submeter, validar ou devolver | 59 |
| T04.01 | `T0401-Formalizacao.dc.html` — T04.01 Revisão e formalização de evento | 41 |
| T05 A·B·C·D | `Vencimentos.dc.html` — T05.A Vencimentos — Lista por faixas<br>`T05B-Calendario.dc.html` — T05.B Vencimentos — Calendário<br>`T05C-Continuidade.dc.html` — T05.C Vencimentos — Continuidade<br>`T05D-Marcos.dc.html` — T05.D Vencimentos — Marcos regulamentares | 49 |
| T06 lista A·B e detalhe 1–6 | `Prorrogacoes.dc.html` — T06.A Procedimentos — Em andamento<br>`T06B-Concluidos.dc.html` — T06.B Procedimentos — Concluídos e cancelados<br>`T06-D1-Resumo.dc.html` — T06 Detalhe — 1 Resumo<br>`T06-D2-Etapas.dc.html` — T06 Detalhe — 2 Etapas e movimentações<br>`T06-D3-Checklist.dc.html` — T06 Detalhe — 3 Lista de verificação<br>`T06-D4-Marcos.dc.html` — T06 Detalhe — 4 Marcos e prazos<br>`T06-D5-Substituicao.dc.html` — T06 Detalhe — 5 Substituição<br>`T06-D6-Documentos.dc.html` — T06 Detalhe — 6 Documentos | 91 |
| T07 A·B·C·D | `T07A-Formalizado.dc.html` — T07.A Valores — Formalizado<br>`T07B-Execucao.dc.html` — T07.B Valores — Execução registrada<br>`T07C-Projecao.dc.html` — T07.C Valores — Projeção<br>`T07D-Cenarios.dc.html` — T07.D Valores — Cenários simulados | 40 |
| T08 A·B·C·D | `Empenhos.dc.html` — T08.A Empenhos — Cobertura<br>`T08B-Notas.dc.html` — T08.B Empenhos — Notas de empenho<br>`T08C-RestosPagar.dc.html` — T08.C Empenhos — Restos a pagar<br>`T08D-Solicitacoes.dc.html` — T08.D Empenhos — Solicitações de reforço | 52 |
| T08.01 variantes | `T0801-NotaEmpenho.dc.html` — T08.01 Variante — Nota de empenho<br>`T0801-Movimento.dc.html` — T08.01 Variante — Movimento de empenho<br>`T0801-Liquidacao.dc.html` — T08.01 Variante — Liquidação<br>`T0801-Pagamento.dc.html` — T08.01 Variante — Pagamento<br>`T0801-Reforco.dc.html` — T08.01 Variante — Solicitação de reforço | 46 |
| T09 A·B·C·D·E | `Pagamentos.dc.html` — T09.A Pagamentos — Obrigações<br>`T09B-DocFiscais.dc.html` — T09.B Pagamentos — Documentos fiscais<br>`T09C-Liquidacoes.dc.html` — T09.C Pagamentos — Liquidações<br>`T09D-Pagamentos.dc.html` — T09.D Pagamentos — Pagamentos e retenções<br>`T09E-Impedimentos.dc.html` — T09.E Pagamentos — Impedimentos | 71 |
| T10 A·B·C e T10.01 | `Reajustes.dc.html` — T10.A Reajustes — Pedidos<br>`T10B-DatasBase.dc.html` — T10.B Reajustes — Datas-base<br>`T10C-Retroativos.dc.html` — T10.C Reajustes — Retroativos<br>`T1001-Simulacao.dc.html` — T10.01 Simulação e memória de cálculo | 63 |
| T11 A·B·C·D | `Providencias.dc.html` — T11.A Providências — Minhas<br>`T11B-Todas.dc.html` — T11.B Providências — Todas (com editor lateral)<br>`T11C-PorResponsavel.dc.html` — T11.C Providências — Por responsável<br>`T11D-Concluidas.dc.html` — T11.D Providências — Concluídas e canceladas | 39 |
| T12 A·B·C | `Notificacoes.dc.html` — T12.A Notificações — Não lidas<br>`T12B-Historico.dc.html` — T12.B Notificações — Histórico<br>`T12C-Resumos.dc.html` — T12.C Notificações — Resumos | 28 |
| T13 A·B e T13.01 | `Relatorios.dc.html` — T13.A Relatórios — Catálogo<br>`T13B-Emissoes.dc.html` — T13.B Relatórios — Emissões recentes<br>`T1301-Previa.dc.html` — T13.01 Prévia e exportação — RPT15 | 46 |
| T14.01 (3 abas) | `T1401-Usuarios.dc.html` — T14.01 Usuários<br>`T1401-Perfis.dc.html` — T14.01 Perfis e permissões<br>`T1401-Unidades.dc.html` — T14.01 Unidades | 20 |
| T14.02 (5 abas) | `T1402-Categorias.dc.html` — T14.02 Categorias e grupos<br>`T1402-Etapas.dc.html` — T14.02 Etapas e listas de verificação<br>`T1402-Parametros.dc.html` — T14.02 Parâmetros internos<br>`T1402-Regras.dc.html` — T14.02 Regras jurídicas<br>`T1402-Calendario.dc.html` — T14.02 Calendário e índices | 21 |
| T14.03 (3 abas) | `T1403-Regras.dc.html` — T14.03 Regras por evento<br>`T1403-Destinatarios.dc.html` — T14.03 Destinatários e canais<br>`T1403-Monitor.dc.html` — T14.03 Monitor do agendador | 29 |
| T14.04.01–07 | `Importacao.dc.html` — T14.04.01 Lotes<br>`T140402-Mapeamento.dc.html` — T14.04.02 Prévia e mapeamento<br>`T140403-Conciliacao.dc.html` — T14.04.03 Conciliação de contratos<br>`T140404-Designacao.dc.html` — T14.04.04 Divergências de designação<br>`T140405-Validacao.dc.html` — T14.04.05 Validação por domínio<br>`T140406-Qualidade.dc.html` — T14.04.06 Qualidade da carteira<br>`T140407-Recibo.dc.html` — T14.04.07 Recibo e reconciliação | 71 |
| T14.05 (3 abas) | `T1405-Trilha.dc.html` — T14.05 Trilha de auditoria<br>`T1405-Exportacoes.dc.html` — T14.05 Exportações<br>`T1405-Correcoes.dc.html` — T14.05 Correções | 12 |
| T14.06 | `T1406-Copias.dc.html` — T14.06 Cópias e recuperação | 4 |
| T14.07 (3 abas) | `T1407-Conectores.dc.html` — T14.07 Integrações — Conectores<br>`T1407-Execucoes.dc.html` — T14.07 Integrações — Execuções<br>`T1407-Divergencias.dc.html` — T14.07 Integrações — Divergências | 17 |
| 12.6 celular (3 visões) | `Celular.dc.html` — Celular — Ação agora<br>`CelularFicha.dc.html` — Celular — Ficha do contrato<br>`CelularNotificacao.dc.html` — Celular — Notificação | 15 |

O artboard `T03-Historico.dc.html` demonstra “Situação em uma data” e o modo de consulta histórica (CH01). O artboard `Padroes.dc.html` reúne os estados obrigatórios, os rótulos fixos e os padrões de formulário da seção 12.1.

## 3 Como a revisão foi feita

1. **Verificação estrutural (`gerador/build.py`).** Para cada artboard: links internos válidos, HTML bem formado, presença do `support.js`, ausência de `{{`, ausência de rolagem horizontal da página em 390 px (CO02) e existência de ao menos um link de entrada. A altura de cada quadro do canvas é medida no navegador.
2. **Verificação de conteúdo (`gerador/revisao.py`).** Lista de itens extraída da seção 12: regiões, colunas, campos, ações, validações e rótulos de cada tela e aba. Inclui a moldura comum da seção 12.1: unidade ativa, data de posição, consulta em outra data, busca global, notificações, menu do usuário, menu lateral e rodapé com as versões do sistema e das regras.
3. **Verificação de regras.** Datas calculadas pelo gerador (C01, C15 e C19) a partir da posição 10/11/2026. Também foram conferidos o piso de prioridade pelo risco (C17), o risco de cada contrato (C18) e a coerência dos totais entre telas: T01, T03.04, T08, T09 e T13.01.

## 4 Rodadas de revisão e correções

| Rodada | Resultado | Correções aplicadas |
| --- | --- | --- |
| 1 | 1 pendência automática e 8 inconsistências na revisão manual | Texto “autenticação institucional” em T00. Ações faltantes: “Validar” em T08.B, “Atualizar situação” em T08.D, “Estornar com motivo” em T09.A e “Ratear entre obrigações” em T09.B. Contagem de competências da conferência trabalhista em T03.11 (11 com registro + 1 sem). Universo do RPT15 coerente com as unidades filtradas (060/2024 incluído; 031/2023, 047/2024 e 041/2026 listados à parte). “Ver composição” nos totais de T07.B. Executado não liquidado unificado em R$ 338.400,00 (T01.B, T01.C e T09). |
| 2 | 0 pendências (3.343 verificações) | Revisão das regras de cálculo, que apontou dois desvios. |
| 3 | 2 desvios de regra corrigidos; 0 pendências | **C17, piso pelo risco:** providências de contratos com risco Alto passaram a ter prioridade sugerida Alta (endosso e suplentes do 012/2025; saneamento do 031/2023). O ajuste manual (sugerida Média → confirmada Alta, com motivo) passou a ser demonstrado no 038/2024. **C18, ordem 8:** o 025/2023, com sucessora assinada mas ainda não vigente, passou a risco Moderado; indicadores de risco recalculados. |
| Visual | Ajustes de leiaute | Tabela de cobertura de T08.A reorganizada para caber na tela. Colunas de T11.B sem largura mínima. Botões com quebra de linha. Rótulos curtos no calendário de T05.B. |

## 5 Decisões de interpretação (para validação)

- **Uma aba por artboard.** Cada aba, passo e subvisão é um artboard próprio. Assim, notificações e indicadores abrem diretamente a aba de destino (por exemplo, N01 → T03.02 e N15 → T05.D), como manda o catálogo da seção 9.1.
- **Contratos de exemplo.** A ficha detalhada é a do 012/2025, com término em 28/11/2026, o que reproduz CV07, CD01 e CD05. Os demais contratos levam à mesma ficha de exemplo.
- **Situação da C15.** “Em andamento” quando o procedimento foi aberto até a data interna; “em andamento após o prazo interno” quando foi aberto depois dela.
- **Piso da C17.** Aplicado a todas as providências do contrato, conforme o risco do contrato.
- **C18, ordem 4.** “Sucessor vigente” foi lido literalmente: sucessora assinada, mas ainda não iniciada, não afasta o risco Moderado da ordem 8.
- **Telas técnicas.** T14.01, T14.03 (monitor), T14.06 e T14.07 (conectores e execuções) aparecem no perfil de administrador técnico; as demais, no perfil de coordenador.
- **Massa fictícia.** Nenhum nome real de pessoa ou empresa é usado. Os CNPJs têm dígitos verificadores válidos, inclusive o exemplo alfanumérico 12.ABC.345/01DE-35, que é o mesmo dos testes. O contato do encarregado de dados ficou como lacuna marcada para a instituição preencher.

## 6 Como regenerar

```
cd prototipos/gerador
python3 build.py      # gera ../canvas/project/*.dc.html e canvas.json, mede as alturas e verifica links e HTML
python3 revisao.py    # confere o conteúdo contra a seção 12 e grava ../revisao_conformidade.json
```

Requer Python 3 e Node.js com Playwright (para medir as alturas). A publicação usa a pasta `canvas/` como raiz do artefato de design.
