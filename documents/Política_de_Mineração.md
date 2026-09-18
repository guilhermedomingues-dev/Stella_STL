# Política de Mineração — Stella

**Status:** Documento oficial  
**Projeto:** Stella (STL)

## 1. Objetivo

A Política de Mineração da Stella estabelece as regras para a produção de blocos, a emissão de novos STL e a remuneração dos mineradores.

Essas regras são determinadas pelo protocolo, de forma previsível e verificável, sem depender de decisões individuais de mineradores, usuários ou administradores.

## 2. Parâmetros da mineração

A Stella utilizará uma recompensa inicial de **50 STL por bloco**, com intervalo esperado de **10 minutos** entre blocos.

A recompensa será reduzida pela metade a cada **5 anos**, conforme o mecanismo de halving definido pelo protocolo.

A dificuldade inicial da Proof of Work será estabelecida em **4 zeros**.

A recompensa recebida pelo minerador ficará sujeita a um período de maturação de **6 blocos subsequentes** antes de poder ser utilizada.

A unidade monetária mínima será o **Saint**, sendo **1 STL equivalente a 100.000.000 Saints**.

O supply máximo definido para a Stella é de **20.000.000 STL**.

Durante o período de emissão, as transações não terão taxa protocolar. As taxas serão ativadas automaticamente quando o subsídio de mineração chegar ao fim, no **33º halving**.

## 3. Unidade monetária

A Stella utiliza o STL como unidade monetária principal e o Saint como sua menor unidade indivisível.

**1 STL = 100.000.000 Saints**  
**1 Saint = 0,00000001 STL**

Nenhum saldo, transação ou recompensa poderá representar uma quantidade inferior a **1 Saint**.

Essa limitação também determina o momento em que a emissão por recompensa de bloco deverá ser encerrada.

## 4. Criação de blocos

Cada bloco deverá conter, no mínimo:

- índice;
- timestamp;
- conjunto de transações;
- prova de trabalho;
- hash do bloco anterior.

A referência ao hash do bloco anterior estabelece a ligação entre os blocos e permite à rede verificar a continuidade e a integridade da cadeia.

O intervalo esperado entre blocos é de **10 minutos**. A dificuldade da Proof of Work deverá considerar o tempo efetivamente observado entre os blocos, conforme as regras de ajuste estabelecidas pelo protocolo.

## 5. Recompensa de mineração

O minerador responsável pela produção de um bloco válido receberá a recompensa determinada pelo protocolo para o período de emissão correspondente.

A recompensa inicial será de **50 STL por bloco**.

O valor da recompensa não pode ser definido ou aumentado livremente pelo minerador.

A quantidade de novos STL criada em cada bloco deve obedecer integralmente à política de emissão estabelecida pelo protocolo.

## 6. Maturação da recompensa

As recompensas provenientes da mineração não poderão ser utilizadas imediatamente após a criação do bloco.

O minerador deverá aguardar a confirmação de **6 blocos subsequentes na cadeia principal**.

Considerando o intervalo esperado de 10 minutos entre blocos, o período de maturação corresponde a aproximadamente uma hora.

Essa regra reduz o risco de que uma recompensa associada a um bloco posteriormente descartado seja utilizada antes que a posição daquele bloco na cadeia esteja suficientemente consolidada.

A recompensa continua pertencendo ao minerador durante esse período; apenas sua utilização permanece temporariamente restrita.

Por exemplo, uma recompensa obtida no bloco 100 poderá ser utilizada após a confirmação dos blocos 101, 102, 103, 104, 105 e 106 na cadeia principal.

## 7. Halving

A recompensa por bloco será reduzida pela metade a cada **5 anos**, independentemente de decisões externas ao protocolo.

A sequência inicial de emissão será:

**50 → 25 → 12,5 → 6,25 → 3,125 → ... STL**

O mecanismo permite recompensas fracionárias enquanto o valor calculado permanecer igual ou superior a **1 Saint**.

O número de blocos correspondente a cada período de cinco anos será de **262.800 blocos**, considerando o intervalo esperado de 10 minutos entre blocos.

## 8. Encerramento da emissão por mineração

A recompensa correspondente ao período após `n` halvings será calculada pela fórmula:

**50 / 2ⁿ STL**

Como o Saint é a menor unidade monetária possível, valores inferiores a 1 Saint não poderão ser emitidos nem arredondados.

No **32º halving**, a recompensa calculada será aproximadamente **0,00000001164 STL**, equivalente a cerca de **1,164 Saints**.

No **33º halving**, o valor cairá para aproximadamente **0,00000000582 STL**, equivalente a **0,582 Saint**.

Consequentemente, o **32º halving será o último período com uma recompensa representável em Saints**.

No **33º halving**, o subsídio de mineração será encerrado e nenhum novo STL será criado como recompensa de bloco.

Considerando um intervalo de cinco anos entre halvings, esse encerramento ocorrerá aproximadamente **165 anos após o início da emissão**, caso os períodos sejam completos.

O encerramento do subsídio não implica o encerramento da mineração. Os mineradores poderão continuar produzindo blocos e contribuindo para a segurança e continuidade da rede.

## 9. Taxas de transação

Durante todo o período em que existir subsídio de mineração, a taxa protocolar das transações será de **0 STL**.

A ausência de taxas nesse período tem como objetivo favorecer a circulação dos STL entre os usuários.

Quando o subsídio chegar a zero, no **33º halving**, o protocolo ativará automaticamente o regime de taxas.

A partir desse momento, cada transação estará sujeita a uma taxa equivalente a **0,1% do valor transferido**, limitada ao máximo de **1 STL por transação**.

A fórmula da taxa será:

**taxa = min(valor da transação × 0,001, 1 STL)**

A taxa deverá respeitar a unidade mínima de **1 Saint** e não poderá resultar em valor inferior a 1 Saint quando houver necessidade de cobrança.

As taxas serão destinadas ao **minerador do bloco que incluir a transação** e constituirão a remuneração dos mineradores após o encerramento do subsídio.

A transição para o regime de taxas será determinada pelo próprio protocolo e não dependerá de votação, decisão administrativa ou alteração manual.

## 10. Conflito entre blocos

É possível que dois mineradores encontrem blocos válidos quase simultaneamente, ambos referenciando o mesmo bloco anterior.

Nessa situação, a rede poderá manter temporariamente duas versões concorrentes da cadeia.

A cadeia principal será aquela que apresentar o **maior Proof of Work acumulado**.

O bloco pertencente à cadeia descartada será considerado órfão e não permanecerá como parte da cadeia principal.

A recompensa associada a um bloco órfão não será válida como recompensa da cadeia principal.

Já as transações contidas nesse bloco poderão voltar a ser consideradas para inclusão em blocos futuros, desde que continuem válidas e ainda não tenham sido incluídas na cadeia principal.

## 11. Regras para os mineradores

Para produzir um bloco válido, o minerador deverá:

1. construir o bloco de acordo com as regras do protocolo;
2. incluir apenas transações válidas;
3. referenciar corretamente o bloco anterior;
4. realizar a Proof of Work exigida;
5. respeitar a recompensa determinada pelo protocolo;
6. transmitir o bloco à rede.

A produção de um bloco não concede ao minerador liberdade para criar uma quantidade arbitrária de STL.

Tanto a recompensa quanto as demais condições de emissão são determinadas pelo protocolo.

Após receber uma recompensa, o minerador deverá respeitar o período de maturação de **6 blocos** antes de utilizá-la.

Após o encerramento do subsídio, o minerador será remunerado pelas taxas das transações incluídas nos blocos que produzir.

## 12. Princípios da política

A política de mineração da Stella busca estabelecer uma emissão previsível, limitada e verificável.

A criação de novos STL ocorre exclusivamente de acordo com regras previamente definidas pelo protocolo, enquanto a remuneração dos mineradores acompanha a evolução do sistema:

- inicialmente, por meio da emissão de novas moedas;
- posteriormente, por meio das taxas de transação.

A política também estabelece uma unidade monetária indivisível, impede a criação arbitrária de recompensas e mantém a mineração como atividade necessária à continuidade da rede mesmo após o fim da emissão.

As taxas, quando ativadas, possuem uma regra determinística e previsível, limitada a **0,1% do valor transferido ou 1 STL, prevalecendo o menor valor**.

## 13. Resumo dos parâmetros

| Parâmetro | Regra |
|---|---|
| Supply máximo | 20.000.000 STL |
| Recompensa inicial | 50 STL por bloco |
| Intervalo esperado | 10 minutos |
| Halving | A cada 5 anos |
| Blocos por período | 262.800 blocos |
| Dificuldade inicial | 4 zeros |
| Maturação da recompensa | 6 blocos |
| Unidade mínima | 1 Saint |
| Conversão | 1 STL = 100.000.000 Saints |
| Taxa durante a emissão | 0 STL |
| Taxa após ativação | 0,1% do valor transferido |
| Teto da taxa | 1 STL por transação |
| Destino das taxas | Minerador do bloco |
| Ativação das taxas | 33º halving |
| Encerramento do subsídio | 33º halving |
| Critério para conflitos | Maior Proof of Work acumulado |

As regras estabelecidas neste documento fazem parte da política oficial de mineração da Stella.

Sua execução deve ocorrer de forma determinística pelo protocolo, sem depender de intervenção manual.