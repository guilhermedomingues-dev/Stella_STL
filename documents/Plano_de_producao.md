 Stella (STL) --- Plano de Produção

## Objetivo

Construir a Stella (STL), uma criptomoeda própria baseada nos princípios
tecnológicos fundamentais do Bitcoin, com finalidade educacional.

O projeto não tem como objetivo listagem em bolsa, investimento ou
especulação. O objetivo é construir e compreender a tecnologia por trás
de uma criptomoeda funcional.

## Princípio de desenvolvimento

Cada etapa deve produzir uma funcionalidade concreta e testável.

A prioridade é manter o código:

-   simples;
-   legível;
-   modular;
-   sem abstrações desnecessárias;
-   sem código repetitivo;
-   sem funcionalidades que não tenham uma finalidade real.

Uma abstração só deve ser criada quando resolver um problema concreto do
projeto.

------------------------------------------------------------------------

## FASE 0 --- Fundação

**Objetivo:** organizar o projeto antes de aumentar sua complexidade.

-   [x] Definir estrutura de pastas
-   [x] Separar a lógica da blockchain da API Flask
-   [x] Criar `Block`
-   [x] Criar `Transaction`
-   [x] Criar configuração central da STL
-   [x] Manter o código simples e documentado
-   [x] Criar testes básicos

**Resultado esperado:** o código atual continua funcionando, mas deixa
de concentrar todas as responsabilidades em um único arquivo.

------------------------------------------------------------------------

## FASE 1 --- Blocos

**Objetivo:** estabelecer definitivamente a estrutura de um bloco.

Estrutura inicial:

``` text
index
timestamp
transactions
proof
previous_hash
```

Implementar:

-   [x] Criação de blocos
-   [x] Hash SHA-256
-   [x] Referência ao bloco anterior
-   [x] Validação individual de blocos
-   [x] Validação da cadeia

**Resultado esperado:** blockchain estruturalmente consistente.

------------------------------------------------------------------------

## FASE 2 --- Transações e UTXO

**Objetivo:** substituir o modelo simplificado
`sender → recipient → amount`.

Estrutura:

``` text
Transaction
├── inputs
└── outputs
```

Implementar:

-   [x] UTXO
-   [x] Criação de outputs
-   [x] Consumo de UTXOs
-   [x] Troco
-   [x] Identificação única de transações
-   [x] Prevenção de gasto duplo
-   [x] Validação de valores
-   [x] Cálculo de saldo

Exemplo:

``` text
Alice possui 100 STL

        ↓ envia 30

Bob       30 STL
Alice     70 STL
```

**Resultado esperado:** a blockchain passa a controlar propriedade de
moedas, e não apenas registrar transferências.

------------------------------------------------------------------------

## FASE 3 --- Criptografia

**Objetivo:** fazer a blockchain exigir prova de propriedade.

Implementar:

-   [x] Geração de chave privada
-   [x] Geração de chave pública
-   [x] Assinatura digital
-   [x] Verificação de assinatura
-   [x] Associação entre assinatura e transação

Fluxo:

``` text
Private Key
     ↓
   assina
     ↓
Transaction
     ↓
Blockchain
     ↓
Public Key
     ↓
  verifica
```

**Resultado esperado:** uma pessoa não pode simplesmente declarar que é
o remetente de uma transação sem possuir a chave correspondente.

------------------------------------------------------------------------

## FASE 4 --- Carteiras

**Objetivo:** transformar as chaves criptográficas em uma carteira
utilizável.

Implementar:

-   [x] Criação de carteira
-   [x] Endereço
-   [x] Armazenamento da chave privada
-   [x] Recuperação da chave pública
-   [x] Consulta de saldo
-   [x] Criação de transação
-   [x] Assinatura de transação

Estrutura:

``` text
Carteira
   │
   ├── Private Key
   ├── Public Key
   └── Address
```

**Resultado esperado:** duas pessoas poderão possuir carteiras
diferentes e realizar transações autenticadas.

------------------------------------------------------------------------

## FASE 5 --- Persistência

**Objetivo:** garantir que os dados importantes da Stella sejam mantidos
mesmo após o encerramento da aplicação.

Implementar:

-   [x] Definir mecanismo de persistência
-   [x] Persistir a blockchain
-   [x] Persistir os blocos
-   [x] Persistir os UTXOs
-   [x] Persistir os dados das carteiras
-   [x] Persistir as chaves privadas de forma segura
-   [x] Recuperar a blockchain após reinicialização
-   [x] Recuperar as carteiras após reinicialização
-   [x] Recuperar os UTXOs após reinicialização
-   [x] Separar a camada de persistência da lógica da blockchain
-   [x] Testar gravação dos dados
-   [x] Testar recuperação dos dados
-   [x] Testar reinicialização da aplicação

**Resultado esperado:** a Stella não perde sua blockchain, carteiras e
estado dos UTXOs quando a aplicação é encerrada.

> A Fase 4 trata da carteira em memória. O armazenamento persistente e
> seguro da chave privada será tratado nesta fase.

------------------------------------------------------------------------

## FASE 6 --- Usuários e autenticação

**Objetivo:** criar a camada de usuários que utilizarão as carteiras da
Stella.

Implementar:

-   [ ] Criar o conceito de usuário
-   [ ] Criar identificação única para usuários
-   [ ] Associar usuário e carteira
-   [ ] Criar cadastro de usuários
-   [ ] Criar autenticação
-   [ ] Armazenar credenciais de forma segura
-   [ ] Permitir acesso do usuário à própria carteira
-   [ ] Impedir acesso à carteira de outro usuário
-   [ ] Associar operações ao usuário autenticado
-   [ ] Integrar usuário, carteira e endereço
-   [ ] Testar criação de usuários
-   [ ] Testar autenticação
-   [ ] Testar associação entre usuário e carteira
-   [ ] Testar acesso autorizado
-   [ ] Testar acesso não autorizado

Estrutura:

``` text
Usuário
   │
   └── Carteira
        │
        ├── Private Key
        ├── Public Key
        └── Address
```

**Resultado esperado:** cada usuário poderá acessar sua própria carteira
de forma autenticada, sem interferir nas carteiras de outros usuários.

------------------------------------------------------------------------

## FASE 7 --- Economia da STL

**Objetivo:** definir as regras monetárias da Stella.

Definir:

``` text
Nome: Stella
Símbolo: STL
Supply máximo: definido pelo projeto
```

Implementar:

-   [ ] Supply máximo
-   [ ] Emissão inicial
-   [ ] Recompensa de mineração
-   [ ] Controle do supply
-   [ ] Impossibilidade de criação arbitrária de moedas
-   [ ] Unidades e fracionamento da STL

Constantes poderão incluir, quando necessárias:

``` text
MAX_SUPPLY
BLOCK_REWARD
```

**Resultado esperado:** a STL possui uma política monetária
determinística.

------------------------------------------------------------------------

## FASE 8 --- Mineração / Proof of Work

A blockchain atual já possui uma versão inicial de Proof of Work. Nesta
fase, ela será integrada às regras monetárias da STL.

Implementar:

-   [ ] Proof of Work
-   [ ] Dificuldade
-   [ ] Validação da prova
-   [ ] Mineração de blocos
-   [ ] Recompensa
-   [ ] Coinbase transaction
-   [ ] Regras de emissão
-   [ ] Ajuste de dificuldade, caso adotado pelo protocolo

**Resultado esperado:**

``` text
Minerador
   ↓
encontra Proof
   ↓
bloco válido
   ↓
recebe STL
```

------------------------------------------------------------------------

## FASE 9 --- Rede P2P

**Objetivo:** transformar os nós isolados em uma rede de blockchain.

Implementar:

-   [ ] Nós
-   [ ] Descoberta/registro de nós
-   [ ] Propagação de transações
-   [ ] Propagação de blocos
-   [ ] Comunicação entre nós
-   [ ] Sincronização da blockchain

Arquitetura conceitual:

``` text
        Nó A
       /          /         Nó B ---- Nó C
      \      /
       \    /
        Nó D
```

**Resultado esperado:** cada nó mantém sua própria cópia da blockchain e
consegue se comunicar com os demais.

------------------------------------------------------------------------

## FASE 10 --- Consenso

A blockchain atual já possui o início de um mecanismo de consenso. Nesta
fase, ele será transformado em regras completas do protocolo.

Implementar:

-   [ ] Validação de blocos recebidos
-   [ ] Validação de transações recebidas
-   [ ] Escolha da cadeia válida
-   [ ] Resolução de conflitos
-   [ ] Sincronização de nós
-   [ ] Rejeição de blocos inválidos
-   [ ] Rejeição de transações inválidas

**Resultado esperado:** os nós conseguem manter um estado comum da rede.

------------------------------------------------------------------------

## FASE 11 --- Segurança do protocolo

**Objetivo:** tentar quebrar o próprio sistema.

Testar:

-   [ ] Alteração de bloco antigo
-   [ ] Alteração de transação
-   [ ] Gasto duplo
-   [ ] Criação arbitrária de moedas
-   [ ] Gasto sem chave privada
-   [ ] Envio de valor inválido
-   [ ] Bloco com Proof of Work inválida
-   [ ] Bloco com hash anterior incorreto
-   [ ] Tentativas de manipulação de saldo
-   [ ] Transações inválidas propagadas pela rede

Pergunta principal:

> Como eu consigo quebrar isso?

**Resultado esperado:** identificar e corrigir vulnerabilidades antes da
versão final.

------------------------------------------------------------------------

## FASE 12 --- API e interface

**Objetivo:** disponibilizar o protocolo por meio de uma API.

Os endpoints atuais serão adaptados ao novo protocolo:

``` text
/transactions/new
/mine
/chain
/nodes/register
/nodes/resolve
```

Podem ser adicionados, quando necessários:

-   [ ] API para usuários
-   [ ] API para autenticação
-   [ ] API para carteiras
-   [ ] Consulta de saldo
-   [ ] Consulta de transação
-   [ ] Consulta de bloco
-   [ ] Envio de STL

**Regra:** a API não deve conter as regras fundamentais da blockchain.
Ela deve apenas se comunicar com o núcleo do protocolo.

------------------------------------------------------------------------

## FASE 13 --- Teste de rede

**Objetivo:** testar a Stella como uma rede distribuída.

Exemplo:

``` text
PC 1 → Nó 1
PC 2 → Nó 2
PC 3 → Nó 3
```

Teste de transação:

``` text
Carteira A
     ↓
  10 STL
     ↓
Carteira B
```

Testar:

-   [ ] Mineração
-   [ ] Transações
-   [ ] Sincronização
-   [ ] Conflitos
-   [ ] Validação
-   [ ] Comunicação entre nós
-   [ ] Segurança
-   [ ] Persistência

------------------------------------------------------------------------

# Arquitetura inicial

A estrutura inicial esperada é:

``` text
stella/
│
├── core/
│   ├── block.py
│   ├── blockchain.py
│   ├── transaction.py
│   ├── utxo.py
│   ├── wallet.py
│   ├── crypto.py
│   └── mining.py
│
├── network/
│   ├── node.py
│   └── consensus.py
│
├── api/
│   └── app.py
│
├── tests/
│
├── config.py
├── main.py
└── requirements.txt
```

Essa estrutura é inicial e pode ser alterada durante o desenvolvimento.
Arquivos ou abstrações que não resolvam problemas reais não devem ser
criados apenas por organização estética.

------------------------------------------------------------------------

# Regra de desenvolvimento

A Stella será construída seguindo:

``` text
Conceito
   ↓
Estrutura
   ↓
Implementação
   ↓
Teste
   ↓
Integração
```

Não será adotada a abordagem de simplesmente adicionar código e corrigir
os problemas posteriormente.

Cada componente importante deve ser compreensível e testável
isoladamente antes de ser integrado ao restante do protocolo.

------------------------------------------------------------------------

# Próximo passo

**Fase atual: FASE 4 --- Carteiras**

As Fases 0, 1, 2 e 3 foram concluídas.

A Fase 4 será concluída com a implementação e os testes das
funcionalidades de carteira. A persistência dos dados e das chaves
privadas será tratada posteriormente na **Fase 5 --- Persistência**.

------------------------------------------------------------------------

Utilzar a VENV:
- Criar: python -m venv venv
- Ligar: .\venv\Scripts\Activate.ps1
- Desligar: deactivate
- Deletar: Remove-Item -Recurse -Force venv