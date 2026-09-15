Sistema semelhante ao Bitcoin: escassez rígida → segurança por mineração → emissão decrescente

Economia da Stella — roteiro de estudos
Objetivo da Fase 7

Definir as regras econômicas e monetárias da Stella de forma que a emissão e o controle da STL sejam determinísticos, verificáveis e resistentes à criação arbitrária de moedas.

# STELLA — FUNDAMENTOS MONETÁRIOS

## Finalidade

A STL será uma moeda digital destinada principalmente à circulação entre usuários, permitindo transações, formação de preços e observação de fenômenos econômicos.

## Funções

* Meio de troca
* Unidade de conta
* Reserva de valor secundária
* Instrumento de experimentação econômica

## Oferta

* Supply máximo limitado
* Emissão determinada pelo protocolo
* Impossibilidade de criação arbitrária
* Supply máximo proposto: **21.000.000 STL**

## Propriedades desejadas

* Escassez
* Previsibilidade
* Divisibilidade
* Fungibilidade
* Portabilidade
* Durabilidade
* Resistência à manipulação
* Política monetária determinística

## Estabilidade

A prioridade inicial será a previsibilidade da política monetária, e não a manutenção de uma cotação fixa em relação ao dólar.

## Emissão

A emissão de novas STL ocorrerá por meio da mineração e será vinculada à criação de novos blocos.

Cada bloco poderá gerar uma quantidade determinada de novas STL, denominada **recompensa de bloco**.

Como proposta inicial:

* Tempo médio de bloco: **1 minuto**
* Recompensa inicial: **50 STL por bloco**
* Intervalo de redução: **210.000 blocos**
* Redução da recompensa: **50% a cada intervalo**

A sequência proposta será:

```text
50 STL
↓
25 STL
↓
12,5 STL
↓
6,25 STL
↓
3,125 STL
↓
...
```

A emissão continuará seguindo essa política até se aproximar do `MAX_SUPPLY`, sem permitir que o limite máximo seja ultrapassado.

## Limitação da emissão

A Stella terá uma política de emissão progressivamente decrescente.

A proposta inicial é utilizar um mecanismo semelhante ao *halving* do Bitcoin, no qual a quantidade de novas STL emitidas por bloco é reduzida pela metade após um intervalo determinado de blocos.

O objetivo é tornar a emissão progressivamente menor à medida que o supply existente aumenta, preservando a escassez e a previsibilidade da política monetária.

A forma matemática definitiva da emissão, os intervalos, a recompensa inicial e seus efeitos sobre a economia da Stella ainda serão validados durante o desenvolvimento da política monetária.

## Taxas de transação

A política de taxas será orientada pela necessidade de manter a STL em circulação entre os usuários.

As taxas deverão ser suficientemente baixas para não desestimular transações pequenas e frequentes.

Ao mesmo tempo, deverá existir um mecanismo de proteção contra abuso e spam da rede.

Como princípio inicial:

* Taxas baixas
* Custo reduzido para transações pequenas
* Taxa relacionada principalmente ao uso de recursos da rede, e não ao valor transferido
* Mecanismo de aumento de taxas em situações de congestionamento
* Utilização das taxas como incentivo adicional aos mineradores

A política definitiva de taxas ainda será definida e testada.

## Segurança econômica

A emissão de novas STL deverá ocorrer exclusivamente pelas regras estabelecidas pelo protocolo.

Nenhum usuário, minerador ou entidade individual poderá criar STL arbitrariamente.

A combinação entre:

**supply máximo → emissão programada → mineração → redução periódica da recompensa → taxas de transação**

formará a base da política monetária da Stella.



2. Oferta monetária
Pergunta fundamental 1 — Oferta monetária

Quantas STL podem existir?

Estudar:

Supply máximo;
supply inicial;
supply circulante;
moedas ainda não emitidas;
emissão futura;
possibilidade ou impossibilidade de alterar o limite;
consequências econômicas de um supply fixo;
consequências de um supply variável.

Parâmetro futuro:

MAX_SUPPLY
3. Emissão
Pergunta fundamental 2 — Emissão

Como novas STL entram na economia?

Estudar:

emissão inicial;
emissão por mineração;
recompensa por bloco;
emissão programada;
emissão decrescente;
emissão contínua;
emissão extraordinária;
momento em que a emissão termina.

Parâmetro futuro:

BLOCK_REWARD
4. Inflação e deflação
Pergunta fundamental 3 — Inflação

Como a política de emissão afeta a quantidade de STL em circulação?

Estudar:

inflação monetária;
deflação;
inflação previsível;
inflação decrescente;
supply fixo;
perda de poder de compra;
crescimento econômico × emissão monetária;
efeitos de uma moeda escassa.

Aqui vamos comparar principalmente Bitcoin, Ethereum e Solana com economias nacionais.

5. Distribuição da STL
Pergunta fundamental 4 — Distribuição

Quem recebe as STL e em que momento?

Estudar:

distribuição inicial;
mineração;
recompensas;
concentração de moedas;
distribuição entre participantes;
moedas perdidas;
moedas não movimentadas;
possíveis mecanismos de distribuição.

Essa pergunta é importante porque ter um supply limitado não significa automaticamente ter uma distribuição saudável.

6. Incentivos econômicos
Pergunta fundamental 5 — Incentivos

Por que alguém deveria participar da rede?

Estudar:

recompensa de mineração;
taxas;
incentivo para mineradores;
incentivo para nós;
custo de participação;
relação entre recompensa e segurança;
sustentabilidade dos incentivos quando a emissão diminuir;
o que acontece quando o BLOCK_REWARD chegar a zero.

Aqui entra diretamente a relação:

Economia → Incentivos → Segurança da rede

7. Taxas de transação
Pergunta fundamental 6 — Taxas

Como as transações serão economicamente tratadas?

Estudar:

existência de taxas;
cálculo das taxas;
quem recebe;
taxas mínimas;
taxas como incentivo;
taxas como mecanismo anti-spam;
possibilidade de queima;
relação entre taxas e segurança.

Precisamos comparar especialmente:

Bitcoin;
Ethereum;
outros modelos relevantes.
8. Segurança econômica
Pergunta fundamental 7 — Segurança

Quanto custa atacar ou manipular economicamente a Stella?

Estudar:

relação entre emissão e segurança;
recompensa dos mineradores;
custo de mineração;
ataques de 51%;
poder computacional;
concentração de mineração;
incentivo para comportamento honesto;
consequências econômicas de uma recompensa insuficiente.

Isso conecta a economia diretamente à arquitetura que estamos construindo.

9. Controle do supply
Pergunta fundamental 8 — Controle do supply

Como o protocolo garante que a quantidade de STL existente está correta?

Estudar:

validação da emissão;
soma das moedas emitidas;
validação das recompensas;
limite de MAX_SUPPLY;
prevenção de emissão duplicada;
prevenção de overflow;
validação dos blocos;
consenso sobre a emissão.

Aqui começamos a transformar a política econômica em regra de software.

10. Criação arbitrária de moedas
Pergunta fundamental 9 — Imutabilidade da emissão

Como impedir que alguém simplesmente crie STL?

Estudar:

regras de consenso;
emissão exclusivamente autorizada pelo protocolo;
validação da recompensa;
rejeição de blocos inválidos;
impossibilidade de alterar o supply unilateralmente;
diferença entre criar STL legitimamente e falsificar STL.

O resultado esperado é:

Nenhum participante consegue criar STL fora das regras determinadas pelo protocolo.

11. Unidades e fracionamento
Pergunta fundamental 10 — Unidade monetária

Qual é a menor unidade da Stella?

Estudar:

unidade principal: STL;
casas decimais;
menor unidade;
representação interna;
precisão;
arredondamento;
possibilidade de transações fracionadas.

Precisamos definir algo conceitualmente equivalente ao:

BTC → satoshi

Mas não devemos simplesmente copiar o número de casas do Bitcoin. Primeiro precisamos entender por que o fracionamento existe e qual precisão faz sentido para a Stella.

12. Sustentabilidade da economia
Pergunta fundamental 11 — Sustentabilidade

A economia continua funcionando quando a emissão mudar ou terminar?

Estudar:

redução das recompensas;
fim da emissão;
dependência da mineração;
transição de recompensa → taxas;
sustentabilidade da segurança;
comportamento econômico dos participantes.

Essa é uma questão que considero essencial para não criarmos uma economia que funciona apenas enquanto existe emissão.

13. Política monetária
Pergunta fundamental 12 — Política monetária

Quais regras governam a STL ao longo de sua existência?

Estudar:

previsibilidade;
regras fixas;
possibilidade de alteração;
governança;
parâmetros econômicos;
condições para mudanças;
consequências de mudanças.

Aqui vamos comparar especialmente:

Bitcoin → regras extremamente rígidas

versus

Ethereum → política monetária parcialmente adaptativa

versus

economias nacionais → política monetária administrada por instituições.

14. Modelo econômico completo

Depois de estudar tudo isso, finalmente poderemos responder:

Quanto existe?
        ↓
Como novas moedas surgem?
        ↓
Quem recebe?
        ↓
Por que recebe?
        ↓
Como as transações são cobradas?
        ↓
Como o supply é controlado?
        ↓
Como impedimos criação arbitrária?
        ↓
Como a rede permanece segura?
        ↓
O que acontece quando a emissão diminui?
        ↓
Como a economia permanece sustentável?

Esse será o modelo econômico da Stella.