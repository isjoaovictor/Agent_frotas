# Frota Agentic — Design e comportamento da interface Streamlit

## 1. Objetivo da implementação

Atualizar a interface existente em `src/app/main.py` para o nome **Frota Agentic**. Usar a imagem de nome-base `site`, localizada em `src/utils/`, como referência da composição visual. A página combina cabeçalho preto, abertura com formulário à esquerda e fotografia grande de navio à direita, seguida por uma área clara com três cartões de consulta.

Aplicar o visual corporativo da identidade existente. A logo fornecida em `src/utils/logo.jpeg`, as transições do layout e a animação de navio fazem parte da entrega.

A implementação abrange a interface, seus recursos visuais, configuração do Streamlit e adaptação da chamada pública ao grafo assíncrono. As regras, prompts de negócio, extração, recuperação, servidor MCP e cálculos permanecem sob responsabilidade do backend. Usar o fluxo público disponível no repositório.

## 2. Referência visual e conteúdo da aplicação

Localizar `src/utils/site` pela extensão real do arquivo. Essa imagem orienta proporções, espaçamento, hierarquia tipográfica e distribuição das áreas. Todo o conteúdo visível será específico do Frota Agentic, incluindo marca, navegação, títulos, imagens, perguntas, ações e resultados. O arquivo `site` serve ao implementador e fica fora das imagens exibidas na página.

| Elemento da referência | Aplicação no Frota Agentic |
|---|---|
| Cabeçalho preto com marca à esquerda | Logo existente e nome Frota Agentic. |
| Navegação simples à direita | Âncoras “Consultar” e “Evidências”, ligadas a áreas reais da página. |
| Título grande e formulário na metade esquerda | Título “Consulte sua frota”, pergunta operacional e ação “Analisar frota”. |
| Foto principal na metade direita | Navio de `navio_1`, enquadrado em paisagem. |
| Seção clara com três cartões | “Consultas rápidas”, usando `navio_1`, `navio_2` e `navio_3`. |
| Cartões com título curto | Exemplos de perguntas sobre chegada, reserva e velocidade. |

As fotos ilustram o tema marítimo. Os navios reais fotografados não recebem os identificadores fictícios S1-FAROL a S4-ATLAS. O relatório é a origem dos dados operacionais apresentados.

## 3. Identidade e logo

O nome visível, o título da aba e o nome acessível da aplicação serão **Frota Agentic**. O nome técnico do repositório continua `Agent_frotas`.

Usar `src/utils/logo.jpeg` como logo principal, preservando proporção, cores e texto da marca. O arquivo tem símbolo e letras pretas e verdes sobre fundo branco. Para manter a leitura no cabeçalho escuro, colocá-lo em uma superfície branca discreta, com respiro, aproximadamente 100 a 120 px no desktop. Usar `object-fit: contain` e evitar mistura de cores que torne o desenho preto invisível.

Ao lado da logo, apresentar “Frota Agentic” em branco, com peso 700. Manter a silhueta de `src/app/ship.svg` associada à marca ou às transições quando já estiver presente no comportamento existente.

## 4. Paleta e tipografia

| Uso | Cor de referência |
|---|---|
| Cabeçalho e abertura | `#080A09` |
| Superfícies escuras secundárias | `#191C1B` |
| Texto sobre fundo escuro | `#F4F5F3` |
| Texto secundário sobre fundo escuro | `#BCC5BF` |
| Ação principal e foco | `#91DB80` |
| Fundo da seção inferior | `#F4F5F3` |
| Texto sobre fundo claro | `#111612` |
| Texto secundário sobre fundo claro | `#4A554E` |
| Bordas sobre fundo claro | `#D9DFD9` |
| Falha acompanhada de texto | `#F07878` |

Usar Inter, com fallback para fontes sans serif do sistema. No desktop, o título principal terá entre 56 e 72 px, conforme a largura. No celular, entre 34 e 42 px. Corpo entre 16 e 18 px e resposta entre 18 e 20 px. Priorizar legibilidade e espaçamento.

O verde existente orienta ações e foco. Status também precisam de texto ou símbolo, pois diferenças de cor sozinhas não são suficientes para todos os usuários.

## 5. Recursos de imagem

Os arquivos serão colocados em `src/utils/` com os nomes-base `navio_1`, `navio_2` e `navio_3`. Preservar a extensão real. Resolver os recursos pelo caminho relativo ao arquivo Python, independentemente do diretório do terminal.

Associação dos recursos do Frota Agentic, usando os nomes e extensões informados por João.

| Recurso | Fotografia | Uso |
|---|---|---|
| `navio_1.webp` | Vista lateral do Vale Minas Gerais, arquivo original `vale_valemax_navio.webp`. | Foto principal e cartão de chegada. |
| `navio_2.jfif` | Porta-contêineres em navegação sobre mar azul. | Cartão de reserva de combustível. |
| `navio_3.jfif` | Popa com inscrição Vale Brasil, arquivo original `images.jpg`. | Cartão de velocidade em tempestade. |

Conferir as imagens existentes pelo conteúdo no momento da implementação e ajustar o enquadramento ao arquivo real. Confirmar os arquivos existentes no momento da implementação e aceitar `.jpg`, `.jpeg`, `.jfif`, `.png` ou `.webp` para esses nomes-base. Se houver mais de um arquivo para o mesmo nome-base, usar um mapeamento explícito. Se faltar uma imagem, manter o formulário utilizável e informar a pendência na entrega.

A imagem principal deve ter proporção próxima de 16:10 e altura de 360 a 450 px no desktop. Aplicar `object-fit: cover` com foco no navio. Um gradiente sutil na borda esquerda pode integrar a fotografia ao fundo escuro. As fotos conservam o mar e a luz originais.

Nos cartões, usar proporção uniforme próxima de 16:9 e cortes que preservem o navio. Para a foto mais fechada da popa, ajustar `object-position` individualmente.

## 6. Estrutura da página

### Cabeçalho

Altura aproximada entre 110 e 140 px no desktop. Logo e nome alinhados à esquerda. Navegação à direita com até dois destinos existentes. Separação inferior por uma linha discreta.

“Consultar” leva ao formulário. “Evidências” leva ao resultado quando disponível. Antes da primeira consulta, ocultar esse segundo destino ou apresentá-lo desabilitado de forma acessível.

### Abertura e formulário

Container central com largura máxima entre 1280 e 1440 px, margens laterais de 48 a 64 px e espaçamento vertical generoso. Duas colunas próximas de 50/50, com intervalo entre 40 e 64 px.

A coluna esquerda contém, nesta ordem.

1. Título “Consulte sua frota”.
2. Linha de contexto “Manual e relatório operacional do Porto Alfa”.
3. Rótulo “Sua pergunta”.
4. Campo multilinha com placeholder “Qual navio chega primeiro ao porto?”.
5. Botão “Analisar frota”.

O campo deve ter superfície clara e texto escuro, como na referência, com altura entre 130 e 160 px. O botão usa verde e texto quase preto, altura mínima de 48 px e largura proporcional ao texto.

A coluna direita contém a foto principal. Manter o foco da primeira dobra na pergunta e no navio. A área de resultado começa vazia.

### Consultas rápidas

Abaixo da abertura, criar uma seção de fundo claro, título “Consultas rápidas” e três cartões na mesma linha no desktop. Cada cartão contém uma fotografia, um título e uma ação acessível.

| Cartão | Imagem | Pergunta preenchida no formulário |
|---|---|---|
| “Previsão de chegada” | `navio_1` | “Qual navio chega primeiro ao porto?” |
| “Reserva de combustível” | `navio_2` | “Algum navio está impedido de zarpar? Qual e por quê?” |
| “Velocidade em tempestade” | `navio_3` | “Qual velocidade deve ser usada para o S2-MARE durante a tempestade?” |

Selecionar um cartão preenche a pergunta e leva o foco ao formulário. A análise começa quando o usuário seleciona “Analisar frota”. Atualizar o widget pela lógica de sessão ou callback do Streamlit antes de sua instanciação no rerun, evitando modificar a chave depois de desenhar o campo.

Os cartões são atalhos operacionais. Resultados, ETAs e status só aparecem após retorno do grafo.

## 7. Transições existentes e carregamento

Inspecionar `src/app/style.css` e `src/app/main.py` antes de alterar a composição. A versão atual usa transição de largura e grade em cerca de 550 ms, redução de título e revelação do resultado em cerca de 650 ms, além da órbita do navio durante o carregamento.

Conservar a sequência de envio, carregamento e revelação. Adaptar os seletores ao novo layout com chaves estáveis nos containers e widgets.

Durante a análise, mostrar o overlay escuro e o modal central com “Gerando resposta”. Reutilizar `ship.svg`, a animação `sail` e o anel `spin-ring`. O navio percorre a trajetória circular e permanece reconhecível. O texto permanece parado.

Mostrar o modal antes de aguardar a chamada. Fechá-lo no sucesso e na falha. Desabilitar formulário e atalhos enquanto a execução estiver em andamento.

Quando a resposta chegar, a foto principal cede espaço ao painel de resultado à direita, com transição suave de largura e opacidade. O formulário permanece na coluna esquerda com título reduzido. Preservar a pergunta enviada. A seção de cartões permanece abaixo.

Um novo resultado substitui o anterior. A animação completa de abertura do resultado acontece na primeira transição para o estado de resposta. Expandir evidências ou detalhes mantém a composição estável.

Respeitar `prefers-reduced-motion`, removendo órbita e deslocamentos e mantendo a silhueta estática. A preferência deve valer para todos os efeitos novos e herdados.

## 8. Resposta e evidências

O painel de resultado apresenta “Resposta”, a conclusão recebida, “Evidências” e uma área expansível de detalhes. Usar superfície com contraste próprio, sem texto escuro herdado da seção de cartões.

Preservar números, unidades, motivos de bloqueio e ressalvas retornados. No caminho atual, priorizar `resposta` para a conclusão, com fallback para `resultado` se esse for o único campo disponibilizado. Evitar duplicar as fontes já concatenadas em `resultado`.

Para evidências, reunir `contextos`, `documentos` e `contextos_regras`, eliminando repetições por origem, posição e conteúdo. Exibir documento, seção, posição quando disponível e texto literal. Separar visualmente as origens “Relatório da frota” e “Manual de operações”.

As referências listadas em `fontes` podem ser apresentadas de forma compacta. O rótulo dos trechos deve ser “Contexto consultado” quando o backend apenas os recuperou. Um vínculo por afirmação só pode aparecer se for fornecido pelo backend.

Em “Detalhes da análise”, mostrar os campos realmente disponíveis, como intenção, identificadores esperados e extraídos, ferramentas chamadas, argumentos e resultados. As ToolMessages são associadas às solicitações por `tool_call_id`. Tratar tanto texto simples quanto blocos textuais no conteúdo.

Campos antigos como quantidade de buscas e expansão só aparecem quando o fluxo os devolver com significado para a consulta. Dados ausentes não devem receber números presumidos. A interface registra limitações na entrega técnica.

## 9. Integração assíncrona e sessão

O grafo publicado usa nós assíncronos. A interface precisa chamar a operação pública `graph.ainvoke`, encaminhando `run_config()` para manter o rastreamento Langfuse. A ponte síncrona do script Streamlit deve ser pequena e executada uma vez por envio. Resolver a chamada dentro do ciclo efetivo do Streamlit e administrar o envio pendente de telemetria conforme o cliente existente.

Manter no estado da sessão a pergunta em edição, a pergunta enviada, o resultado, o indicador de processamento, o erro e a indicação da primeira revelação. Consumir o sinal de envio uma única vez e guardar o retorno para os reruns seguintes.

O servidor MCP precisa estar acessível no endereço configurado. A interface não inicia um novo servidor a cada interação e não duplica a lógica de ferramentas.

Os caminhos de regras e fora do escopo podem ser concluídos depois desta especificação. Ler o builder disponível e apresentar os estados que ele efetivamente retornar. As mensagens finais desses caminhos devem aparecer na mesma área de resposta quando estiverem implementados.

## 10. Validações e falhas

Pergunta vazia mantém o foco no campo e exibe “Digite uma pergunta para analisar a frota”.

Falha técnica encerra o modal, preserva a pergunta para reenvio manual e apresenta “Houve um problema interno no servidor da Vale. Tente novamente.” O diagnóstico completo fica nos logs e no trace disponível.

Ao iniciar uma nova consulta, invalidar o resultado anterior para que uma falha não mostre uma resposta antiga associada à pergunta nova. Em encerramento por ausência de informação ou fora do escopo, usar a mensagem recebida do backend.

## 11. Responsividade e acessibilidade

Abaixo de aproximadamente 900 px, empilhar formulário, foto ou resultado e cartões. No celular, manter 16 a 20 px de margem, título legível e botão ocupando a largura disponível. A fotografia ocupa menos altura e os três cartões aparecem em coluna.

Garantir rótulos visíveis, navegação por teclado, foco verde perceptível e ordem de leitura coerente. O modal recebe semântica de diálogo e estado de processamento. Fotografias decorativas usam texto alternativo vazio. A logo recebe identificação de marca. Atalhos recebem nomes que descrevem a pergunta que preenchem.

Evitar dimensões rígidas que cortem texto. Conferir a leitura em 390 px, 768 px e desktop, sem rolagem horizontal.

## 12. Entrega esperada ao implementar este documento

Alterações previstas em `src/app/main.py`, `src/app/style.css`, configuração visual do Streamlit se necessária e recursos visuais da interface. Usar caminhos robustos para os arquivos de utils. Entregar a interface no ponto de entrada existente.

Conferência mínima de conclusão.

1. A abertura segue a referência com marca, formulário, foto e três cartões.
2. “Frota Agentic” aparece no cabeçalho e no título da aba.
3. A logo de utils permanece legível e os três navios são utilizados.
4. A seleção de um cartão preenche a pergunta sem disparar análise automática.
5. Um envio válido chama o grafo uma vez, mostra o navio em órbita e revela o resultado.
6. Evidências mostram manual e relatório quando ambos estiverem presentes.
7. Uma falha fecha o modal e permite tentar novamente.
8. Reruns de apresentação preservam o resultado e não repetem chamadas.
9. Movimento reduzido, teclado e tela estreita permanecem utilizáveis.
10. Informar arquivos alterados, comando de execução e cenários efetivamente verificados.

Comando de execução a partir da raiz.

```powershell
python -m streamlit run src/app/main.py
```

Esta especificação descreve a próxima implementação visual. O README distingue a interface herdada da integração ainda pendente.
