# Política Econômica — Stella

**Status:** Documento oficial  
**Projeto:** Stella (STL)

## 1. Objetivo

A Política Econômica da Stella estabelece as regras relacionadas à circulação dos STL, às transações e aos mecanismos econômicos fundamentais do protocolo.

A política busca garantir que a emissão e a circulação da moeda ocorram de maneira previsível, controlada e compatível com o funcionamento da rede.

## 2. Oferta monetária

A Stella possui um **supply máximo definido de 20.000.000 STL**. A criação de novos STL ocorre exclusivamente de acordo com as regras de emissão estabelecidas pelo protocolo de mineração.

Não é permitida a criação arbitrária de STL por usuários, mineradores ou qualquer entidade externa ao protocolo.

A emissão segue uma recompensa inicial de **50 STL por bloco**, com novos blocos esperados a cada **10 minutos** e redução da recompensa pela metade a cada **5 anos**, conforme estabelecido na Política de Mineração.

## 3. Circulação

A Stella será estruturada para permitir a circulação direta de STL entre seus usuários.

Durante o período de emissão, **não haverá taxa protocolar de transação**. O objetivo dessa regra é evitar que custos de transferência constituam uma barreira à utilização e circulação da moeda.

A ausência de taxas não elimina a necessidade de mecanismos de controle do volume de transações. A rede deverá limitar a quantidade de transações que podem permanecer aguardando processamento, evitando que o sistema seja sobrecarregado por spam.

## 4. Controle de transações

As transações que ainda não foram incluídas em um bloco permanecerão na **mempool** da rede.

Como os blocos possuem intervalo esperado de 10 minutos, deverá existir um limite para a quantidade de transações que podem permanecer na mempool entre a produção de blocos.

Esse limite tem como finalidade impedir que um usuário ou grupo de usuários envie um volume excessivo de transações sem custo, comprometendo a capacidade da rede de processar transações legítimas.

O limite exato da mempool ainda deverá ser definido pelo protocolo. A definição desse parâmetro deve considerar a capacidade de processamento da rede e o intervalo esperado entre blocos.

## 5. Relação com a mineração

As regras econômicas relacionadas à emissão de STL seguem a Política de Mineração da Stella.

A recompensa inicial é de **50 STL por bloco**, com halving a cada 5 anos. A recompensa possui maturação de **6 blocos subsequentes** antes de poder ser utilizada.

Quando o subsídio de mineração chegar a zero, no **33º halving**, as taxas de transação serão ativadas automaticamente e passarão a constituir a remuneração dos mineradores.

Até esse momento, a taxa protocolar das transações permanecerá em **0 STL**.

## 6. Unidade monetária

A unidade mínima da Stella é o **Saint**.

**1 STL = 100.000.000 Saints**  
**1 Saint = 0,00000001 STL**

Nenhuma transação, saldo ou recompensa poderá representar uma quantidade inferior a 1 Saint.

## 7. Princípios econômicos

A economia da Stella é baseada em emissão determinada pelo protocolo, oferta limitada, previsibilidade monetária e circulação entre usuários.

A criação de moeda não pode ocorrer arbitrariamente, e as regras de emissão não dependem de decisões individuais.

Durante o período de emissão, a Stella prioriza a circulação sem taxas de transação. Após o encerramento do subsídio, o protocolo passa automaticamente para um modelo no qual as taxas de transação remuneram os mineradores.

## 8. Resumo

| Parâmetro | Regra |
|---|---|
| Supply máximo | 20.000.000 STL |
| Recompensa inicial | 50 STL por bloco |
| Intervalo esperado | 10 minutos |
| Halving | A cada 5 anos |
| Taxa durante a emissão | 0 STL |
| Controle de spam | Limite de transações na mempool |
| Unidade mínima | 1 Saint |
| 1 STL | 100.000.000 Saints |
| Maturação da recompensa | 6 blocos |
| Ativação das taxas | 33º halving |

As regras econômicas devem ser executadas de forma determinística pelo protocolo. Parâmetros ainda não definidos neste documento não devem ser presumidos ou implementados com valores arbitrários.