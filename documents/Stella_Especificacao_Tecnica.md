# Stella (STL)
## Especificação Técnica do Projeto

Versão da documentação: 1.0
Data: 11 de setembro de 2026
Estado do projeto: FASE 0 — Fundação (conforme `Plano_de_producao.md`)

> Este documento representa **exclusivamente** o estado do código-fonte fornecido no momento desta análise (os arquivos `app.py`, `wallet.py`, `block.py`, `blockchain.py`, `crypto.py`, `mining.py`, `transaction.py`, `utxo.py`, `consensus.py`, `node.py`, `test_transaction.py`, `requirements.txt`, `config.py`, `main.py` e `Plano_de_producao.md`). Nenhuma informação foi inferida além do que os arquivos permitem concluir. Onde o código não permite determinar algo com segurança, isso é declarado explicitamente como *"Não especificado na implementação atual"*.

---

# 1. Visão Geral do Projeto

**Nome:** Stella
**Ticker/Símbolo:** STL
**Natureza:** projeto educacional. O próprio `Plano_de_producao.md` declara que o projeto não tem como objetivo listagem em bolsa, investimento ou especulação, e sim construir e compreender a tecnologia por trás de uma criptomoeda funcional.

**Objetivo técnico:** implementar, de forma incremental e testável, os componentes fundamentais de uma criptomoeda inspirada no Bitcoin: blocos encadeados por hash, um mecanismo de Proof of Work, um modelo de transações baseado em UTXO, e (em fases futuras, ainda não implementadas) criptografia de chave pública, carteiras, política monetária, rede P2P e consenso distribuído.

**Estágio atual de desenvolvimento:** de acordo com o `Plano_de_producao.md`, o projeto está na **FASE 0 — Fundação**, com a FASE 1 (Blocos) e parte da FASE 2 (Transações/UTXO) já implementadas no código, ainda que o checklist do documento de planejamento marque a FASE 2 como pendente (`[ ]`). Isso configura uma divergência entre o planejamento e o código, detalhada na Seção 18.

**Linguagem de programação:** Python.

**Frameworks e bibliotecas (conforme `requirements.txt`):**
- `flask>=3.0` — framework web usado para expor a API HTTP do nó (`app.py`).
- `requests>=2.31` — biblioteca HTTP cliente, usada em `consensus.py` para um nó consultar outros nós da rede.

**Bibliotecas da biblioteca padrão utilizadas:** `hashlib` (hash SHA-256), `json` (serialização determinística para hash), `time` (timestamp dos blocos), `uuid` (geração de identificadores de nó), `urllib.parse` (interpretação de endereços de nós em `consensus.py`).

**Estrutura de diretórios:** o `Plano_de_producao.md` propõe explicitamente a seguinte árvore de diretórios:

```text
mariacoin/
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

Os arquivos enviados para esta análise foram entregues em uma estrutura **plana** (sem as pastas `core/`, `network/`, `api/` e `tests/` explicitadas). No entanto, os próprios imports do código confirmam essa organização pretendida:

- `app.py` importa `from core.block import ...`, `from core.transaction import ...`, `from core.blockchain import Blockchain`, `from network.node import generate_node_id` — ou seja, `app.py` se comporta como se estivesse fisicamente localizado em `api/app.py`.
- `main.py` importa `from api.app import app`, confirmando que `app.py` deve residir em `api/`.
- `blockchain.py` importa `from core.block import ...`, `from core.transaction import ...`, `from core.mining import valid_proof`, confirmando que deve residir em `core/`.

Este documento assume essa estrutura de pastas (`core/`, `network/`, `api/`) como a organização pretendida do projeto, por ser a única suportada tanto pelo planejamento quanto pelos imports reais do código. **Não é possível confirmar, apenas pelos arquivos enviados, que essa estrutura de pastas já exista fisicamente no disco** — essa é uma inferência baseada nos imports, não uma constatação direta de um `tree` de diretórios.

**Principais componentes atuais:**
- Um modelo de **bloco** (`core/block.py`) com hash SHA-256 e validação estrutural.
- Uma **blockchain** (`core/blockchain.py`) que encadeia blocos, valida a cadeia e executa Proof of Work.
- Um modelo de **transação baseada em UTXO** (`core/transaction.py`, `core/utxo.py`).
- Um algoritmo de **Proof of Work** duplicado em dois lugares (`core/mining.py` e um método idêntico dentro de `Blockchain`, ver Seção 19).
- Uma **API HTTP** (`api/app.py`) com cinco endpoints, dois dos quais dependem de funcionalidade não conectada (`consensus.py`, ver Seção 19).
- Um **ponto de entrada** (`main.py`) que usa configurações centralizadas (`config.py`).
- **Testes** (`test_transaction.py`) cobrindo apenas o módulo de transações/UTXO.
- **Stubs vazios** para fases futuras: `wallet.py` (FASE 4, carteiras) e `crypto.py` (FASE 3, criptografia), ambos ainda não implementados — contêm apenas comentários.

**O que a Stella não é (importante para não gerar expectativas incorretas):**
- Não é uma rede P2P funcional: não há descoberta de nós, propagação de blocos/transações, nem sincronização automática entre nós (FASE 7, não implementada).
- Não possui criptografia de assinatura: qualquer um pode declarar ser o dono de um UTXO nos dados enviados à API, pois não há verificação de chave pública/privada (FASE 3, não implementada — `crypto.py` está vazio).
- Não possui carteiras (FASE 4, não implementada — `wallet.py` está vazio).
- Não possui uma política monetária definida (supply máximo, recompensa de mineração efetiva) — a recompensa de mineração está fisicamente presente no código de `app.py`, mas **desativada** (comentada), conforme detalhado na Seção 11.
- Não deve ser usada como um sistema de valor real: é um projeto de estudo.

---

# 2. Arquitetura Completa

## 2.1 Responsabilidade de cada arquivo

| Arquivo (caminho lógico) | Responsabilidade |
|---|---|
| `core/block.py` | Estrutura de um bloco: criação, hash SHA-256, validação estrutural. |
| `core/blockchain.py` | Classe `Blockchain`: cadeia de blocos, bloco gênese, adição de blocos, validação da cadeia, Proof of Work, acesso ao último bloco. |
| `core/transaction.py` | Criação de outputs e de transações completas no modelo UTXO (inputs/outputs, troco, transaction ID). |
| `core/utxo.py` | Estrutura de um UTXO, verificação de disponibilidade, consumo, e cálculo de saldo. |
| `core/mining.py` | Algoritmo de Proof of Work (busca de prova e validação de prova). |
| `core/wallet.py` | Reservado para a FASE 4 (carteiras). Vazio. |
| `core/crypto.py` | Reservado para a FASE 3 (criptografia). Vazio. |
| `network/node.py` | Geração do identificador único do nó atual. |
| `network/consensus.py` | Registro de nós conhecidos e algoritmo de resolução de conflitos entre cadeias (consenso "cadeia mais longa"). |
| `api/app.py` | Aplicação Flask: expõe os endpoints HTTP do nó e mantém o estado de UTXOs disponíveis/gastos no nível da API. |
| `config.py` | Constantes centrais: dificuldade da PoW, host/porta padrão do servidor. |
| `main.py` | Ponto de entrada do projeto: importa a aplicação Flask e a executa com as configurações de `config.py`. |
| `tests/test_transaction.py` | Testes automatizados de `core/transaction.py` e `core/utxo.py`. |
| `requirements.txt` | Dependências externas do projeto (`flask`, `requests`). |
| `Plano_de_producao.md` | Documento de planejamento e roteiro de fases do projeto (não é código executável). |

## 2.2 Dependências entre módulos (mapa construído a partir dos imports reais)

```text
main.py
   ↓ importa app, DEFAULT_HOST, DEFAULT_PORT
api/app.py
   ↓ importa
core/block.py         (new_block, hash)
core/transaction.py   (new_transaction, como create_transaction)
core/blockchain.py    (Blockchain)
network/node.py       (generate_node_id)

core/blockchain.py
   ↓ importa
core/block.py         (new_block, hash, valid_block)
core/transaction.py   (new_transaction)  ←  IMPORTADO MAS NÃO UTILIZADO em blockchain.py
core/mining.py        (valid_proof)

core/transaction.py
   ↓ importa
core/utxo.py          (valid_utxo, consume_utxo, create_utxo)

core/mining.py
   → não importa nada do projeto (usa apenas hashlib)

core/utxo.py
   → não importa nada do projeto

network/node.py
   → não importa nada do projeto (usa apenas uuid)

network/consensus.py
   ↓ importa requests, urllib.parse
   → NÃO é importado por nenhum outro arquivo do projeto (ver Seção 19)

tests/test_transaction.py
   ↓ importa
core/transaction.py   (create_output, new_transaction)
core/utxo.py          (create_utxo, get_balance)
```

Este mapa foi construído **apenas** a partir das instruções `import`/`from ... import` presentes nos arquivos. Note que `network/consensus.py` não aparece como destino de nenhuma seta de importação — nenhum arquivo do projeto o importa, apesar de `api/app.py` chamar métodos (`register_node`, `resolve_conflicts`) que só existem, como funções soltas, dentro de `consensus.py`. Essa desconexão está detalhada na Seção 19.

## 2.3 Quem importa quem (visão inversa)

- `core/block.py` é importado por: `api/app.py`, `core/blockchain.py`.
- `core/transaction.py` é importado por: `api/app.py` (como `create_transaction`), `core/blockchain.py` (import não utilizado), `tests/test_transaction.py`.
- `core/blockchain.py` é importado por: `api/app.py`.
- `core/mining.py` é importado por: `core/blockchain.py` (apenas a função `valid_proof`; a função `proof_of_work` de `mining.py` não é importada por ninguém, ver Seção 19).
- `core/utxo.py` é importado por: `core/transaction.py`, `tests/test_transaction.py`.
- `network/node.py` é importado por: `api/app.py` (mas a função importada, `generate_node_id`, não chega a ser chamada — ver Seção 19).
- `network/consensus.py`: não é importado por nenhum arquivo.
- `core/wallet.py`, `core/crypto.py`: não são importados por nenhum arquivo (consistente com serem stubs de fases futuras).

---

# 3. Explicação Arquivo por Arquivo

## 3.1 `core/block.py`

### Responsabilidade
Define a estrutura de dados de um bloco da blockchain e as funções puras para criá-lo, calcular seu hash e validar sua forma estrutural.

### Imports
- `hashlib`: usado para calcular o hash SHA-256 do bloco em `hash()`.
- `json`: usado em `hash()` para serializar o bloco de forma determinística (`json.dumps(..., sort_keys=True)`) antes de gerar o hash. `sort_keys=True` garante que a ordem das chaves no dicionário Python não influencie o hash resultante.
- `from time import time`: usado em `new_block()` para registrar o instante de criação do bloco.

### Classes
Não há classes neste arquivo.

### Funções

**`new_block(index, transactions, proof, previous_hash=None)`**
- Finalidade: construir o dicionário que representa um bloco.
- Parâmetros: `index` (esperado `int`), `transactions` (esperado `list`), `proof` (esperado `int`), `previous_hash` (opcional, `str` ou `int`, padrão `None`).
- Retorno: `dict` com as chaves `index`, `timestamp`, `transactions`, `proof`, `previous_hash`.
- Efeitos colaterais: nenhum (não modifica estado externo); `time()` produz um valor diferente a cada chamada.
- Fluxo interno: monta e retorna diretamente o dicionário; não há validação de tipos dentro da própria função — a validação de tipos só ocorre depois, e apenas se `valid_block()` for chamada explicitamente sobre o resultado.
- Quem chama: `Blockchain.__init__` (bloco gênese) e `Blockchain.add_block` (blocos subsequentes).
- Quem depende dela: toda a cadeia de blocos depende da forma produzida por esta função, já que `hash()` e `valid_block()` assumem essa mesma estrutura de chaves.

**`hash(block)`**
- Finalidade: calcular o hash SHA-256 de um bloco, usado como `previous_hash` do próximo bloco e como critério de integridade da cadeia.
- Parâmetros: `block` (`dict`).
- Retorno: `str` (hexadecimal de 64 caracteres).
- Fluxo interno: `json.dumps(block, sort_keys=True)` converte o dicionário em uma string JSON com chaves ordenadas alfabeticamente; `.encode()` converte essa string em bytes (UTF-8 por padrão); `hashlib.sha256(...).hexdigest()` calcula o hash e o retorna em formato hexadecimal.
- Observação de nomenclatura: esta função é nomeada `hash`, o que **sobrescreve o nome da função embutida `hash()` do Python** dentro de qualquer módulo que a importe dessa forma (`from core.block import hash`). Isso é tecnicamente válido em Python, mas é um ponto de atenção documentado na Seção 19, pois qualquer uso posterior de `hash(...)` embutido nesses módulos passará a chamar esta função em vez da função nativa.
- Quem chama: `Blockchain.valid_chain` (para comparar com `previous_hash` do próximo bloco) e `api/app.py` na rota `/mine` (para calcular o `previous_hash` do novo bloco a partir do último bloco).

**`valid_block(block)`**
- Finalidade: verificar se um dicionário possui a forma esperada de um bloco válido (existência dos campos e tipos corretos).
- Parâmetros: `block` (`dict`).
- Retorno: `bool`.
- Fluxo interno:
  1. Verifica se todos os campos `['index', 'timestamp', 'transactions', 'proof', 'previous_hash']` estão presentes; se não, retorna `False` imediatamente.
  2. Verifica `isinstance(block['index'], int)`.
  3. Verifica `isinstance(block['timestamp'], (int, float))`.
  4. Verifica `isinstance(block['transactions'], list)`.
  5. Verifica `isinstance(block['proof'], int)`.
  6. Verifica `isinstance(block['previous_hash'], (int, str))`.
  7. Se todas as verificações passarem, retorna `True`.
- Importante: esta função valida apenas a **forma** do bloco (presença de campos e tipos), não valida o **conteúdo** semântico (por exemplo, não verifica se o hash do bloco anterior está correto nem se a prova é válida — essas verificações ficam a cargo de `Blockchain.valid_chain`).
- Quem chama: `Blockchain.valid_chain`, para cada bloco a partir do segundo.
- Observação: o bloco gênese (índice 0 da lista `chain`) **nunca** é validado por `valid_block` em `valid_chain`, pois a verificação começa em `current_index = 1`.

## 3.2 `core/blockchain.py`

### Responsabilidade
Gerenciar o ciclo de vida da cadeia de blocos: criação do bloco gênese, adição de novos blocos, validação de uma cadeia recebida, e busca de Proof of Work.

### Imports
- `from core.block import new_block, hash, valid_block`: usados, respectivamente, em `add_block`/`__init__`, em `valid_chain` (comparação de hash), e em `valid_chain` (validação estrutural de cada bloco).
- `from core.transaction import new_transaction`: **importado mas nunca utilizado** dentro deste arquivo — nenhuma função ou método de `Blockchain` chama `new_transaction`. É um import morto.
- `from core.mining import valid_proof`: usado em `valid_chain` e em `proof_of_work`.

### Classes

**`Blockchain`**
- Finalidade: representar o estado da cadeia de um nó: os blocos confirmados, as transações pendentes ainda não mineradas, e o conjunto de nós conhecidos na rede.
- Atributos de instância:
  - `current_transactions` (`list`): transações pendentes, aguardando serem incluídas no próximo bloco minerado.
  - `chain` (`list` de `dict`): a sequência de blocos, começando pelo bloco gênese.
  - `nodes` (`set`): conjunto de endereços de nós conhecidos (netlocs). É criado vazio e **nunca é populado por nenhum método definido nesta classe** — nenhum método de `Blockchain` (como aparece neste arquivo) adiciona itens a `self.nodes` (ver Seção 19 sobre `register_node`).
- Ciclo de vida: instanciado uma única vez em `api/app.py` (`blockchain = Blockchain()`), como estado global do processo Flask. Não há persistência em disco — o estado é perdido ao reiniciar o processo.
- Relação com outras classes: não há herança nem composição com outras classes no projeto; é uma classe autocontida que utiliza funções puras de outros módulos (`core.block`, `core.mining`).

### Métodos

**`__init__(self)`**
- Parâmetros: nenhum (além de `self`).
- Retorno: `None` (construtor).
- Fluxo interno: inicializa `current_transactions=[]`, `chain=[]`, `nodes=set()`, e então cria o bloco gênese chamando `new_block(index=1, transactions=[], proof=100, previous_hash=1)`, anexando-o a `self.chain`.
- Observação técnica: o bloco gênese recebe `index=1` (não `0`, como é comum em outras implementações), `proof=100` (valor arbitrário, não resultante de um cálculo real de Proof of Work) e `previous_hash=1` (um inteiro, não uma string de zeros como é comum em outras implementações de referência). Essas escolhas são válidas dentro da lógica interna do projeto (nada as invalida), mas são particularidades específicas da Stella que diferem de convenções mais comuns — não há, porém, nada no código que exija um valor diferente.

**`add_block(self, proof, previous_hash=None)`**
- Parâmetros: `proof` (esperado `int`, resultado de `proof_of_work`), `previous_hash` (opcional).
- Retorno: o `dict` do bloco recém-criado.
- Efeitos colaterais: esvazia `self.current_transactions` (definindo-a como `[]`) e adiciona o novo bloco a `self.chain`.
- Fluxo interno:
  1. Cria o bloco com `new_block(index=len(self.chain) + 1, transactions=self.current_transactions, proof=proof, previous_hash=previous_hash)`.
  2. Reatribui `self.current_transactions = []`, esvaziando a fila de transações pendentes.
  3. Anexa o bloco a `self.chain`.
  4. Retorna o bloco.
- Observação: o índice do novo bloco é `len(self.chain) + 1`. Como o bloco gênese já ocupa `index=1` e está na posição `chain[0]`, o segundo bloco (primeiro minerado) recebe `index=2`. Não há relação direta entre `index` e a posição na lista Python (posição 0-based vs. índice 1-based do campo `index`), o que é consistente internamente, mas deve ser observado ao ler o código.
- Quem chama: a rota `/mine` de `api/app.py`.

**`valid_chain(self, chain)`**
- Parâmetros: `chain` (`list` de blocos, tipicamente vinda de outro nó via HTTP).
- Retorno: `bool` — `True` se toda a cadeia (a partir do segundo bloco) for estruturalmente válida, tiver hashes encadeados corretamente e provas de trabalho válidas; `False` caso qualquer verificação falhe.
- Fluxo interno (loop `while current_index < len(chain)`, começando em `current_index = 1`):
  1. Obtém `block = chain[current_index]`.
  2. Se `not valid_block(block)`, retorna `False` imediatamente (estrutura inválida).
  3. Se `block['previous_hash'] != hash(last_block)`, retorna `False` (hash do bloco anterior não confere).
  4. Se `not valid_proof(last_block['proof'], block['proof'])`, retorna `False` (prova de trabalho não é uma continuação válida da prova anterior).
  5. Atualiza `last_block = block` e incrementa `current_index`.
  6. Ao final do loop (sem `return False` prematuro), retorna `True`.
- Observação de cobertura: o **bloco gênese (`chain[0]`) nunca é validado** por esta função — nem sua estrutura via `valid_block`, nem seu conteúdo. A validação assume implicitamente que o primeiro elemento da cadeia recebida é confiável.
- Quem chama: `resolve_conflicts` em `network/consensus.py` chamaria `self.valid_chain(chain)` **se estivesse conectada à classe `Blockchain`** — ver Seção 19 sobre essa desconexão.

**`proof_of_work(self, last_proof)`**
- Parâmetros: `last_proof` (`int`, a prova do último bloco confirmado).
- Retorno: `int`, a primeira prova (começando de `0` e incrementando) para a qual `valid_proof(last_proof, proof)` é `True`.
- Fluxo interno: laço `while valid_proof(last_proof, proof) is False: proof += 1`; ao sair do laço, retorna `proof`.
- Observação de duplicação: esta lógica é **idêntica** à função `proof_of_work` definida em `core/mining.py` (mesmo algoritmo, mesma dependência de `valid_proof`). A função de `mining.py` nunca é chamada por nenhum outro arquivo — apenas este método de `Blockchain` é efetivamente usado (via `api/app.py`). Ver Seção 19.
- Quem chama: a rota `/mine` de `api/app.py`, via `blockchain.proof_of_work(last_proof)`.

**`last_block` (property)**
- Parâmetros: nenhum (além de `self`).
- Retorno: o último elemento de `self.chain` (`dict`).
- Uso: acessado como atributo (`blockchain.last_block`), não como método chamado (`blockchain.last_block()`), pois é decorado com `@property`.
- Quem chama: a rota `/mine` (para obter a prova e o hash do bloco anterior) e a rota `/transactions/new` (para calcular em qual índice de bloco a transação será incluída, apenas informativamente).

## 3.3 `core/transaction.py`

### Responsabilidade
Implementar a criação de transações no modelo de inputs/outputs (UTXO), incluindo a validação dos UTXOs usados como entrada, o cálculo do troco, a geração do identificador único da transação e a atualização dos conjuntos de UTXOs disponíveis/gastos.

### Imports
- `hashlib`: usado para gerar o `transaction_id`.
- `from core.utxo import valid_utxo, consume_utxo, create_utxo`: usados dentro de `new_transaction` para, respectivamente, validar cada input, marcar um UTXO usado como gasto, e criar os novos UTXOs resultantes dos outputs.

### Funções

**`create_output(owner, amount)`**
- Finalidade: construir a estrutura de um output de transação.
- Parâmetros: `owner` (esperado `str`, identificador do proprietário — não há verificação de tipo, apenas uso), `amount` (esperado numérico).
- Retorno: `dict` `{'owner': owner, 'amount': amount}`.
- Efeitos colaterais: nenhum.
- Quem chama: `new_transaction` (para o output de troco), `test_transaction.py` (para criar outputs de teste).

**`new_transaction(inputs, outputs, available_utxos, spent_utxos)`**
- Finalidade: validar e construir uma transação completa a partir de uma lista de UTXOs de entrada e uma lista de outputs desejados, atualizando os conjuntos de UTXOs disponíveis e gastos.
- Parâmetros:
  - `inputs` (`list` de UTXOs, cada um um `dict` no formato produzido por `create_utxo`).
  - `outputs` (`list` de `dict` no formato produzido por `create_output`).
  - `available_utxos` (`list`, mutável, representando os UTXOs ainda não gastos, conhecidos pelo chamador).
  - `spent_utxos` (`list`, mutável, representando os UTXOs já consumidos).
- Retorno: o `dict` da transação criada, ou `None` se a transação for inválida.
- Efeitos colaterais (muito relevantes):
  1. Pode **modificar a lista `outputs` recebida como parâmetro**, adicionando a ela um output de troco (`outputs.append(...)`), via mutação do objeto passado pelo chamador — isto é, a lista `outputs` original do chamador é alterada mesmo quando a função retorna com sucesso.
  2. Remove itens de `available_utxos` (`available_utxos.remove(utxo)` para cada input consumido).
  3. Adiciona itens a `spent_utxos` (via `consume_utxo`).
  4. Adiciona novos UTXOs a `available_utxos` (um para cada output, incluindo o de troco, se houver).
- Fluxo interno, passo a passo:
  1. **Validação dos inputs:** para cada `utxo` em `inputs`, chama `valid_utxo(utxo, available_utxos)`. Se algum for inválido (não estiver em `available_utxos`), a função retorna `None` **imediatamente**, sem reverter nada (pois nada ainda foi alterado neste ponto — a validação ocorre antes de qualquer mutação de estado).
  2. **Cálculo dos totais:** `input_amount = sum(utxo['amount'] for utxo in inputs)`; `output_amount = sum(output['amount'] for output in outputs)`.
  3. **Validação de saldo:** se `output_amount > input_amount`, retorna `None` (a transação tentaria gastar mais do que os inputs fornecem).
  4. **Cálculo do troco:** `change = input_amount - output_amount`. Se `change > 0`, cria um output de troco com `create_output(inputs[0]['owner'], change)` e o adiciona à lista `outputs` (mutando-a). O troco é sempre devolvido ao proprietário do **primeiro** input (`inputs[0]['owner']`) — não há suporte a múltiplos remetentes com troco dividido proporcionalmente.
  5. **Montagem da transação:** cria o dicionário `{'inputs': inputs, 'outputs': outputs}`.
  6. **Geração do ID:** `transaction['transaction_id'] = hashlib.sha256(str(transaction).encode()).hexdigest()`. Note que aqui é usada a representação Python padrão do dicionário (`str(transaction)`, equivalente a `repr`), **não** `json.dumps` com `sort_keys=True` como é feito em `core/block.py` para o hash de blocos. Isso é uma diferença metodológica entre o hash de blocos e o ID de transações, documentada como ponto de atenção na Seção 19.
  7. **Consumo dos UTXOs de entrada:** para cada `utxo` em `inputs`: remove-o de `available_utxos` (`available_utxos.remove(utxo)`) e o registra como gasto (`consume_utxo(utxo, spent_utxos)`, que apenas faz `spent_utxos.append(utxo)`).
  8. **Criação dos novos UTXOs:** para cada `(index, output)` em `enumerate(outputs)` (já incluindo o output de troco, se existir), cria um novo UTXO via `create_utxo(transaction['transaction_id'], index, output['owner'], output['amount'])` e o adiciona a `available_utxos`.
  9. Retorna o dicionário `transaction` (agora contendo `inputs`, `outputs` e `transaction_id`).
- Condições de falha (retorno `None`): (a) qualquer UTXO de input não presente em `available_utxos`; (b) soma dos outputs maior que a soma dos inputs.
- Caminho de sucesso: todas as validações passam; `available_utxos` e `spent_utxos` (ambos passados por referência) são atualizados; a transação é retornada com um `transaction_id`.
- Quem chama: `api/app.py` (rota `/transactions/new`, importada como `create_transaction`), `tests/test_transaction.py`.

## 3.4 `core/utxo.py`

### Responsabilidade
Definir a estrutura de um UTXO ("Unspent Transaction Output") e as operações básicas sobre conjuntos de UTXOs: criação, verificação de disponibilidade, marcação como gasto e cálculo de saldo.

### Funções

**`create_utxo(transaction_id, output_index, owner, amount)`**
- Finalidade: construir o dicionário que representa um UTXO.
- Parâmetros: `transaction_id` (`str`, hash da transação que originou este UTXO), `output_index` (`int`, posição do output dentro da lista `outputs` daquela transação), `owner` (identificador do proprietário), `amount` (valor numérico).
- Retorno: `dict` `{'transaction_id':..., 'output_index':..., 'owner':..., 'amount':...}`.
- Quem chama: `new_transaction` (para cada output gerado), `tests/test_transaction.py` (para simular UTXOs iniciais em testes).

**`consume_utxo(utxo, spent_utxos)`**
- Finalidade: registrar um UTXO como gasto.
- Parâmetros: `utxo` (`dict`), `spent_utxos` (`list`, mutável).
- Retorno: `None` (efeito colateral apenas).
- Fluxo interno: `spent_utxos.append(utxo)`. Não verifica se o UTXO já estava presente em `spent_utxos` antes de adicioná-lo novamente (não há checagem de duplicidade dentro desta função isoladamente — a proteção contra reuso vem de `valid_utxo`/remoção de `available_utxos`, não de uma checagem em `spent_utxos`).
- Quem chama: `new_transaction`, para cada input consumido.

**`valid_utxo(utxo, available_utxos)`**
- Finalidade: verificar se um UTXO ainda está disponível para ser gasto.
- Parâmetros: `utxo` (`dict`), `available_utxos` (`list`).
- Retorno: `bool`, resultado de `utxo in available_utxos`.
- Observação técnica: a comparação `in` sobre uma lista de dicionários em Python usa **igualdade estrutural** (`==`), não identidade de objeto (`is`). Isso significa que dois dicionários com os mesmos pares chave-valor são considerados iguais para este teste, mesmo que sejam objetos Python distintos. É esse comportamento que permite que o teste `test_double_spend` funcione corretamente mesmo criando um novo dicionário idêntico para a segunda tentativa de gasto (ver Seção 16).
- Quem chama: `new_transaction`, para cada input.

**`get_balance(owner, available_utxos)`**
- Finalidade: calcular o saldo de um proprietário somando os valores de todos os UTXOs disponíveis que lhe pertencem.
- Parâmetros: `owner`, `available_utxos` (`list`).
- Retorno: número (soma de `amount`), ou `0` se não houver UTXOs daquele proprietário (comportamento padrão de `sum` sobre um gerador vazio).
- Fluxo interno: `sum(utxo['amount'] for utxo in available_utxos if utxo['owner'] == owner)`.
- Quem chama: `tests/test_transaction.py` (`test_balance`). **Não é chamada por nenhuma rota de `api/app.py`** — atualmente não existe um endpoint HTTP para consultar saldo (consistente com o planejamento, que lista "Consulta de saldo" como item pendente da FASE 10).

## 3.5 `core/mining.py`

### Responsabilidade
Implementar o algoritmo de Proof of Work: a busca por uma prova válida e a verificação de que uma prova é válida em relação à prova anterior.

### Imports
- `hashlib`: usado para calcular o hash da tentativa de prova.

### Funções

**`proof_of_work(last_proof)`**
- Finalidade: buscar uma nova prova válida a partir da prova anterior.
- Parâmetros: `last_proof` (`int`).
- Retorno: `int`, a primeira prova válida encontrada.
- Fluxo interno: idêntico ao método `Blockchain.proof_of_work` descrito na Seção 3.2 — laço incremental a partir de `0` até `valid_proof` retornar `True`.
- Observação: **esta função não é chamada por nenhum outro arquivo do projeto.** A única busca de Proof of Work efetivamente utilizada é o método de mesmo nome dentro da classe `Blockchain`. Esta função de módulo é, portanto, código morto (duplicado). Ver Seção 19.

**`valid_proof(last_proof, proof)`**
- Finalidade: verificar se uma prova `proof`, combinada com a prova anterior `last_proof`, produz um hash que satisfaz a dificuldade exigida.
- Parâmetros: `last_proof` (`int`), `proof` (`int`).
- Retorno: `bool`.
- Fluxo interno: `guess = f'{last_proof}{proof}'.encode()` concatena as duas provas como string e as codifica em bytes; `guess_hash = hashlib.sha256(guess).hexdigest()` calcula o hash SHA-256; a função retorna `guess_hash[:4] == "0000"`, ou seja, exige que os quatro primeiros caracteres hexadecimais do hash sejam `"0000"`.
- Observação sobre dificuldade: o valor `"0000"` está **hardcoded** diretamente nesta função. O arquivo `config.py` define uma constante `POW_DIFFICULTY = "0000"` com o propósito aparente de centralizar esse valor, mas `mining.py` **não importa nem usa `config.POW_DIFFICULTY`** — o valor é duplicado manualmente. Isso é documentado como inconsistência na Seção 19.
- Quem chama: `Blockchain.proof_of_work`, `Blockchain.valid_chain`, e a função (não utilizada) `mining.proof_of_work`.

## 3.6 `network/node.py`

### Responsabilidade
Gerar um identificador único para o nó atual (destinado a identificar, por exemplo, o destinatário de uma futura recompensa de mineração).

### Funções

**`generate_node_id()`**
- Finalidade: gerar um identificador aleatório único para o nó.
- Parâmetros: nenhum.
- Retorno: `str`, um UUID v4 sem hífens (`str(uuid4()).replace('-', '')`).
- Observação: esta função é importada em `api/app.py` (`from network.node import generate_node_id`), mas **nunca é chamada**. Em vez disso, `api/app.py` gera seu próprio identificador de nó de forma independente e duplicada, usando exatamente a mesma expressão (`str(uuid4()).replace('-', '')`) diretamente inline. Isso é documentado na Seção 19.

## 3.7 `network/consensus.py`

### Responsabilidade
Implementar o registro de nós conhecidos e o algoritmo de resolução de conflitos entre cadeias concorrentes (consenso do tipo "a cadeia válida mais longa vence").

### Imports
- `requests`: usado em `resolve_conflicts` para consultar o endpoint `/chain` de outros nós via HTTP GET.
- `from urllib.parse import urlparse`: usado em `register_node` para extrair o `netloc` (host:porta) de uma URL completa de nó.

### Funções

**`register_node(self, address)`**
- Finalidade: adicionar um novo endereço de nó ao conjunto de nós conhecidos.
- Parâmetros: `self` (esperado ser uma instância de `Blockchain`, contendo um atributo `nodes`), `address` (`str`, ex.: `'http://192.168.0.5:5000'`).
- Retorno: `None`.
- Fluxo interno: `parsed_url = urlparse(address)`; `self.nodes.add(parsed_url.netloc)` adiciona apenas a parte `host:porta` da URL ao conjunto `nodes`.
- **Ponto crítico:** esta função é escrita como se fosse um método de instância (usa `self` como primeiro parâmetro e acessa `self.nodes`), mas está definida como uma função de módulo solta dentro de `consensus.py`, e **não há, em nenhum arquivo do projeto, nenhuma linha que importe esta função para dentro da classe `Blockchain`** (nem como `import`, nem via atribuição do tipo `Blockchain.register_node = register_node`, nem via herança/mixin). Ver análise completa na Seção 19.

**`resolve_conflicts(self)`**
- Finalidade: implementar o algoritmo de consenso "cadeia válida mais longa", substituindo a cadeia local por uma cadeia mais longa e válida encontrada em algum nó conhecido.
- Parâmetros: `self` (esperado ser uma instância de `Blockchain`, com atributos `nodes` e `chain`, e método `valid_chain`).
- Retorno: `bool` — `True` se a cadeia local foi substituída, `False` caso contrário.
- Fluxo interno:
  1. `neighbours = self.nodes`.
  2. `max_length = len(self.chain)` — o tamanho da cadeia atual, usado como limiar mínimo que uma cadeia concorrente precisa superar.
  3. Para cada `node` em `neighbours`: faz `requests.get(f'http://{node}/chain')`.
  4. Se a resposta tiver `status_code == 200`: extrai `length` e `chain` do corpo JSON da resposta.
  5. Se `length > max_length` **e** `self.valid_chain(chain)` for verdadeiro: atualiza `max_length` e guarda essa cadeia em `new_chain`.
  6. Após percorrer todos os vizinhos, se `new_chain` não for `None`: substitui `self.chain = new_chain` e retorna `True`.
  7. Caso contrário, retorna `False`.
- Observações: (a) esta função depende inteiramente de `self.valid_chain`, que é um método definido em `Blockchain` (ver Seção 3.2) — portanto, mesmo que fosse corretamente vinculada, dependeria de uma chamada de método cruzando os dois arquivos; (b) não há tratamento de exceções para falhas de rede (`requests.get` pode lançar exceções como `ConnectionError` ou `Timeout`, que não são capturadas — uma falha de rede ao consultar um único vizinho interromperia toda a função com uma exceção não tratada); (c) a mesma desconexão crítica de `register_node` se aplica aqui: esta função nunca é conectada à classe `Blockchain`.

## 3.8 `api/app.py`

### Responsabilidade
Expor a blockchain e o sistema de transações do nó através de uma API HTTP construída com Flask, mantendo o estado do processo (a instância de `Blockchain` e as listas de UTXOs disponíveis/gastos).

### Imports
- `from core.block import new_block, hash`: `hash` é usado na rota `/mine` para calcular o hash do último bloco; **`new_block` é importado mas nunca utilizado diretamente neste arquivo** (a criação de blocos ocorre indiretamente, dentro de `Blockchain.add_block`).
- `from core.transaction import new_transaction as create_transaction`: usado na rota `/transactions/new`.
- `from core.blockchain import Blockchain`: usado para instanciar o estado global da blockchain do nó.
- `from network.node import generate_node_id`: importado mas **nunca chamado** (ver Seção 19).
- `from uuid import uuid4`: usado para gerar `node_identifier` diretamente, de forma independente da função `generate_node_id` importada.
- `from flask import Flask, jsonify, request`: framework web e utilitários de resposta/requisição.

### Variáveis de módulo (estado global do processo)
- `app`: instância da aplicação Flask.
- `node_identifier` (`str`): UUID gerado uma vez, na inicialização do módulo. **Atualmente não é utilizado em nenhuma rota**, pois o único trecho que o utilizaria — a criação de uma transação de recompensa de mineração (`create_transaction("0", node_identifier, 1)`) — está comentado dentro da rota `/mine`.
- `blockchain` (`Blockchain`): a única instância da blockchain do nó, compartilhada por todas as requisições enquanto o processo estiver ativo.
- `available_utxos` (`list`): lista de UTXOs disponíveis, mantida **no nível da API**, fora da classe `Blockchain`.
- `spent_utxos` (`list`): lista de UTXOs já gastos, também mantida no nível da API.

### Rotas (funções de view)

**`GET /mine`** — função `mine()`
- Finalidade: executar a mineração de um novo bloco.
- Fluxo interno:
  1. Obtém `last_block = blockchain.last_block` e `last_proof = last_block['proof']`.
  2. Calcula `proof = blockchain.proof_of_work(last_proof)`.
  3. Um trecho de código destinado a criar uma transação de recompensa (`create_transaction("0", node_identifier, 1)`) está **comentado (desativado)** via docstrings de string tripla, portanto não é executado. Note também que, mesmo se fosse descomentado, a chamada `create_transaction("0", node_identifier, 1)` não corresponde à assinatura real de `new_transaction(inputs, outputs, available_utxos, spent_utxos)` — os parâmetros passados (`"0"`, `node_identifier`, `1`) não são compatíveis com o formato esperado (`inputs`/`outputs` como listas de dicionários UTXO/output, mais as listas `available_utxos`/`spent_utxos`). Ou seja, mesmo reativando essa linha tal como está escrita, ela geraria um erro ou comportamento incorreto — é resquício de um modelo anterior mais simples (`sender → recipient → amount`), anterior à adoção do modelo UTXO.
  4. Calcula `previous_hash = hash(last_block)`.
  5. Chama `block = blockchain.add_block(proof, previous_hash)`, que efetivamente cria e anexa o novo bloco (contendo qualquer transação que já estivesse em `blockchain.current_transactions`, mas nenhuma recompensa de mineração, já que essa parte está desativada).
  6. Retorna um JSON com `message`, `index`, `transactions`, `proof`, `previous_hash`, com status HTTP `200`.
- Efeito no estado: incrementa `blockchain.chain`, esvazia `blockchain.current_transactions`.
- **Não movimenta `available_utxos`/`spent_utxos`**, pois nenhuma transação de recompensa é de fato criada.

**`POST /transactions/new`** — função `new_transaction()`
- Finalidade: receber uma transação via HTTP e, se válida, colocá-la na fila de transações pendentes.
- Corpo esperado (JSON): objeto com as chaves `inputs` e `outputs`.
- Fluxo interno:
  1. `values = request.get_json()`.
  2. Verifica se `'inputs'` e `'outputs'` estão presentes em `values`; se não, retorna `'Missing values', 400` (texto simples, não JSON).
  3. Chama `create_transaction(values['inputs'], values['outputs'], available_utxos, spent_utxos)` (esta é a função `new_transaction` de `core/transaction.py`, importada com alias).
  4. Se o retorno for `None`, retorna `'Invalid transaction', 400` (texto simples).
  5. Caso contrário, adiciona a transação a `blockchain.current_transactions`.
  6. Calcula `index = blockchain.last_block['index'] + 1` apenas para fins informativos na mensagem de resposta (não há garantia de que a transação será, de fato, incluída exatamente nesse índice, já que outras transações podem ser adicionadas ou um bloco pode ser minerado antes).
  7. Retorna JSON `{'message': f'Transaction will be added to Block {index}'}` com status `201`.
- Efeito no estado: pode modificar `available_utxos`, `spent_utxos` (via `create_transaction`) e `blockchain.current_transactions`.
- Observação: não há validação de tipos dos campos `inputs`/`outputs` (por exemplo, não se verifica se são realmente listas de dicionários bem formados) além da validação implícita feita dentro de `new_transaction`/`valid_utxo`, que pode gerar exceções não tratadas (por exemplo, `KeyError` se um item de `inputs` não tiver a chave `'amount'`) caso o JSON recebido esteja malformado.

**`GET /chain`** — função `full_chain()`
- Finalidade: retornar a cadeia completa de blocos do nó.
- Retorno: JSON `{'chain': blockchain.chain, 'length': len(blockchain.chain)}`, status `200`.
- Efeito no estado: nenhum (somente leitura).

**`POST /nodes/register`** — função `register_nodes()`
- Finalidade: registrar um ou mais endereços de nós vizinhos.
- Corpo esperado (JSON): `{'nodes': [...]}`.
- Fluxo interno:
  1. `values = request.get_json()`; `nodes = values.get('nodes')`.
  2. Se `nodes` for `None`, retorna `"Error: Please supply a valid list of nodes", 400`.
  3. Para cada `node` em `nodes`, chama `blockchain.register_node(node)`.
  4. Retorna JSON com mensagem e `list(blockchain.nodes)`, status `201`.
- **Este endpoint está quebrado na implementação atual**: `Blockchain` (definida em `core/blockchain.py`) não possui um método `register_node`. Chamar esta rota resultaria em uma exceção `AttributeError: 'Blockchain' object has no attribute 'register_node'`. Detalhes completos na Seção 19.

**`GET /nodes/resolve`** — função `consensus()`
- Finalidade: disparar o algoritmo de resolução de conflitos.
- Fluxo interno: `replaced = blockchain.resolve_conflicts()`; monta uma resposta diferente conforme `replaced` seja `True` ou `False`; retorna JSON com status `200`.
- **Este endpoint também está quebrado pelo mesmo motivo**: `Blockchain` não possui o método `resolve_conflicts`. Ver Seção 19.

**Bloco `if __name__ == '__main__':`**
- `app.run(host='0.0.0.0', port=5000)` — executa o servidor Flask com host/porta **hardcoded**, sem usar as constantes `DEFAULT_HOST`/`DEFAULT_PORT` de `config.py`. Isso só é relevante se `app.py` for executado diretamente (`python app.py`); quando o projeto é executado via `main.py`, este bloco não é atingido, pois `main.py` importa apenas o objeto `app` (a execução do módulo `app.py` como script, e portanto seu próprio `if __name__ == '__main__':`, só ocorre quando ele é o módulo executado diretamente, não quando é importado).

## 3.9 `config.py`

### Responsabilidade
Centralizar constantes de configuração do projeto.

### Conteúdo
- `POW_DIFFICULTY = "0000"`: destinada a representar o prefixo exigido para uma prova de trabalho válida. **Não é referenciada em nenhum outro arquivo** — `core/mining.py` usa o mesmo valor `"0000"`, mas hardcoded diretamente, sem importar esta constante.
- `DEFAULT_HOST = "0.0.0.0"`, `DEFAULT_PORT = 5000`: usadas por `main.py` ao iniciar o servidor Flask.

## 3.10 `main.py`

### Responsabilidade
Servir como ponto de entrada padrão do projeto.

### Fluxo
- Importa `app` de `api.app` e `DEFAULT_HOST`, `DEFAULT_PORT` de `config`.
- Sob `if __name__ == '__main__':`, executa `app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)`.
- Observação: como a simples importação de `api.app` já teria efeitos colaterais (criação da instância `Flask`, da `Blockchain`, das listas de UTXOs, e a definição de todas as rotas via decoradores `@app.route`), o ato de importar `app.py` já é suficiente para montar toda a aplicação; o `if __name__ == '__main__':` dentro do próprio `app.py` só será executado se `app.py` for rodado diretamente como script (o que não é o caso quando ele é importado por `main.py`), evitando duplicidade de chamadas a `app.run()`.

## 3.11 `core/wallet.py`
Contém apenas um comentário indicando que a implementação de endereço, saldo e criação/assinatura de transações a partir de uma carteira está reservada para a FASE 4, e que **ainda não foi implementada**. Não há código executável.

## 3.12 `core/crypto.py`
Contém apenas um comentário indicando que a geração de chaves, assinatura e verificação de transações está reservada para a FASE 3, e que **ainda não foi implementada**. Não há código executável.

## 3.13 `tests/test_transaction.py`
Ver análise detalhada na Seção 16.

## 3.14 `requirements.txt`
Lista as dependências externas: `flask>=3.0` e `requests>=2.31`. Não especifica versões exatas travadas (apenas mínimas), nem inclui uma ferramenta de testes como `pytest` explicitamente — **não é possível determinar, apenas pelos arquivos enviados, qual executor de testes é utilizado para rodar `test_transaction.py`** (o arquivo usa `assert` simples, compatível tanto com `pytest` quanto com execução manual, mas nenhuma dependência de teste está listada em `requirements.txt`).

---

# 4. Explicação Linha por Linha (trechos centrais)

## 4.1 `core/block.py` — `hash(block)`

```python
block_string = json.dumps(block, sort_keys=True).encode()
return hashlib.sha256(block_string).hexdigest()
```
- `json.dumps(block, sort_keys=True)`: serializa o dicionário `block` como uma string JSON, ordenando as chaves alfabeticamente antes de serializar. **Por que existe:** um dicionário Python não garante, por si só, uma ordem de iteração previsível entre diferentes execuções/máquinas caso fosse serializado sem ordenação; ordenar as chaves garante que o mesmo conteúdo lógico sempre produza a mesma string, e portanto o mesmo hash — isso é essencial, pois o hash é usado para verificar integridade encadeada entre blocos.
- `.encode()`: converte a string JSON (texto) em uma sequência de bytes, pré-requisito para a função `hashlib.sha256`, que opera sobre bytes, não sobre `str`.
- `hashlib.sha256(block_string).hexdigest()`: calcula o resumo criptográfico SHA-256 dos bytes e o converte para uma representação legível em hexadecimal (64 caracteres). **Conceito de blockchain envolvido:** este é o mecanismo de encadeamento de blocos — o hash de um bloco depende de todo o seu conteúdo, incluindo (indiretamente, no próximo bloco) o `previous_hash`, de modo que qualquer alteração retroativa em um bloco antigo mudaria seu hash e quebraria a referência armazenada no bloco seguinte.

## 4.2 `core/blockchain.py` — `__init__`

```python
self.chain.append(new_block(index=1, transactions=[], proof=100, previous_hash=1))
```
- Cria o bloco gênese (o primeiro bloco da cadeia) com valores fixos: nenhuma transação, uma prova arbitrária (`100`, não calculada por Proof of Work real) e um `previous_hash` também arbitrário (`1`, um inteiro, já que não existe um bloco anterior real). **Por que existe:** toda blockchain baseada em encadeamento de hashes precisa de um ponto de partida que não depende de um bloco anterior; esse bloco inicial é convencionalmente chamado de "bloco gênese". **Efeito no estado:** é o único bloco presente na cadeia até que `/mine` seja chamado pela primeira vez.

## 4.3 `core/blockchain.py` — `valid_chain`

```python
if block['previous_hash'] != hash(last_block):
    return False
```
- Compara o campo `previous_hash` do bloco atual com o hash recalculado do bloco anterior. **Por que existe:** é a verificação central que garante que a cadeia não foi adulterada — se alguém alterasse qualquer campo de um bloco já confirmado, o hash recalculado desse bloco mudaria, e o `previous_hash` armazenado no bloco seguinte deixaria de corresponder, fazendo a validação falhar. **Conceito envolvido:** integridade encadeada (tamper-evidence) via função de hash criptográfica.

```python
if not valid_proof(last_block['proof'], block['proof']):
    return False
```
- Verifica se a prova do bloco atual é uma continuação válida da prova do bloco anterior, segundo a regra de dificuldade de `core/mining.py`. **Por que existe:** impede que alguém simplesmente insira um bloco com dados arbitrários sem realizar o trabalho computacional exigido pela Proof of Work.

## 4.4 `core/transaction.py` — `new_transaction` (trecho de consumo)

```python
for utxo in inputs:
    available_utxos.remove(utxo)
    consume_utxo(utxo, spent_utxos)
```
- Para cada UTXO usado como entrada da transação: remove-o da lista de UTXOs disponíveis (impedindo que seja reutilizado por outra transação) e o registra na lista de UTXOs gastos. **Por que existe:** este é o mecanismo central de prevenção de gasto duplo (double-spend) no modelo UTXO — uma vez consumido, o UTXO deixa de existir na lista de disponíveis, então uma tentativa futura de usá-lo novamente falhará na etapa de validação (`valid_utxo`). **Efeito no estado:** reduz `available_utxos`, aumenta `spent_utxos`.

## 4.5 `core/utxo.py` — `valid_utxo`

```python
return utxo in available_utxos
```
- Verifica pertencimento por igualdade estrutural. **Conceito envolvido:** em Python, `dict in list` percorre a lista comparando cada elemento com `==`; dois dicionários são iguais em Python se tiverem exatamente os mesmos pares chave-valor, independentemente de serem o mesmo objeto em memória. Isso é o que permite ao projeto identificar um UTXO "pelo seu conteúdo" em vez de por uma referência de objeto.

## 4.6 `api/app.py` — rota `/mine` (trecho de encadeamento)

```python
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)
...
previous_hash = hash(last_block)
block = blockchain.add_block(proof, previous_hash)
```
- Obtém o último bloco confirmado e sua prova; busca uma nova prova válida a partir dela; calcula o hash do último bloco para usá-lo como `previous_hash` do próximo; e finalmente cria o novo bloco. **Fluxo conceitual:** este é o coração do processo de mineração — encontrar um número (`proof`) que, combinado com a prova anterior, produza um hash com o prefixo exigido, provando que um determinado esforço computacional foi realizado antes de o novo bloco ser aceito.

## 4.7 `main.py`

```python
from api.app import app
from config import DEFAULT_HOST, DEFAULT_PORT

if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
```
- Importa a aplicação Flask já totalmente configurada (rotas registradas via decoradores no momento da importação de `api.app`) e a executa usando host/porta centralizados em `config.py`. **Por que existe:** separar o "ponto de entrada" de execução da definição da aplicação é uma prática comum, permitindo, por exemplo, que a aplicação Flask seja importada por testes ou por outro servidor WSGI sem necessariamente iniciar o servidor de desenvolvimento embutido.

---

# 5. Glossário Técnico

| Termo | Definição geral | Como aparece na Stella | Onde no código |
|---|---|---|---|
| **Blockchain** | Estrutura de dados composta por uma sequência de blocos encadeados por hash, resistente a alterações retroativas. | Implementada como a lista `Blockchain.chain`, mantida em memória por processo (sem persistência em disco). | `core/blockchain.py` |
| **Bloco** | Unidade de agrupamento de transações, com metadados de encadeamento. | `dict` com `index`, `timestamp`, `transactions`, `proof`, `previous_hash`. | `core/block.py::new_block` |
| **Bloco gênese** | O primeiro bloco de uma blockchain, sem bloco anterior real. | Criado com `index=1`, `proof=100`, `previous_hash=1`, sem transações. | `Blockchain.__init__` |
| **Índice (`index`)** | Posição/número de ordem de um bloco na cadeia. | Começa em `1` para o gênese; cada bloco novo recebe `len(chain) + 1`. | `core/block.py`, `Blockchain.add_block` |
| **Timestamp** | Marca temporal de criação de um bloco. | Gerado por `time()` no momento em que `new_block` é chamada; tipo `float` (segundos desde a época Unix). | `core/block.py::new_block` |
| **Hash** | Resumo criptográfico de tamanho fixo derivado de dados arbitrários. | SHA-256 sobre a serialização JSON ordenada do bloco. | `core/block.py::hash` |
| **SHA-256** | Função de hash criptográfica que produz uma saída de 256 bits (64 caracteres hexadecimais). | Usada tanto para hash de blocos quanto (via `hashlib.sha256`) para o ID de transações e para o cálculo da Proof of Work. | `core/block.py`, `core/transaction.py`, `core/mining.py` |
| **Hash anterior (`previous_hash`)** | Referência ao hash do bloco imediatamente anterior, criando o encadeamento. | Campo do bloco; calculado explicitamente em `api/app.py` antes de chamar `add_block`. | `core/block.py`, `api/app.py::mine` |
| **Proof of Work (PoW)** | Mecanismo que exige a realização de um esforço computacional verificável para que um bloco seja aceito. | Busca por um número (`proof`) tal que o hash de `last_proof + proof` comece com `"0000"`. | `core/mining.py`, `Blockchain.proof_of_work` |
| **Proof (prova)** | O número encontrado que satisfaz a condição de dificuldade da PoW. | Campo `proof` do bloco; inteiro. | `core/block.py`, `core/mining.py` |
| **Difficulty (dificuldade)** | Parâmetro que determina quão difícil é encontrar uma prova válida. | Fixada implicitamente como "4 zeros hexadecimais iniciais" (`"0000"`), hardcoded em `core/mining.py`; existe também uma constante `POW_DIFFICULTY` em `config.py`, não utilizada por `mining.py`. | `core/mining.py::valid_proof`, `config.py` |
| **Mineração** | Processo de encontrar uma prova válida e, com isso, criar um novo bloco. | Disparada via requisição `GET /mine`. | `api/app.py::mine` |
| **Transação** | Registro de movimentação de valor entre partes. | `dict` com `inputs`, `outputs`, `transaction_id`. | `core/transaction.py` |
| **Input** | Entrada de uma transação: um UTXO sendo gasto. | Elemento da lista `inputs`, no mesmo formato de um UTXO (`transaction_id`, `output_index`, `owner`, `amount`). | `core/transaction.py::new_transaction` |
| **Output** | Saída de uma transação: uma nova alocação de valor para um proprietário. | `dict` `{'owner':..., 'amount':...}`, criado por `create_output`. | `core/transaction.py` |
| **UTXO** | "Unspent Transaction Output" — um output de uma transação anterior que ainda não foi gasto e pode ser usado como input de uma nova transação. | `dict` com `transaction_id`, `output_index`, `owner`, `amount`. | `core/utxo.py::create_utxo` |
| **Spent UTXO (UTXO gasto)** | Um UTXO que já foi consumido como input de alguma transação. | Elementos da lista `spent_utxos`, mantida em `api/app.py`. | `core/utxo.py::consume_utxo` |
| **Available UTXO (UTXO disponível)** | Um UTXO que ainda não foi gasto e pode ser usado. | Elementos da lista `available_utxos`, mantida em `api/app.py`. | `api/app.py`, `core/utxo.py::valid_utxo` |
| **Double-spend (gasto duplo)** | Tentativa de gastar o mesmo UTXO mais de uma vez. | Prevenido pela remoção do UTXO de `available_utxos` no momento em que é consumido pela primeira vez. | `core/transaction.py::new_transaction`, `core/utxo.py::valid_utxo` |
| **Troco (change)** | Valor excedente de um input em relação aos outputs solicitados, devolvido ao remetente. | Calculado como `input_amount - output_amount`; criado como um output extra para `inputs[0]['owner']`. | `core/transaction.py::new_transaction` |
| **Saldo (balance)** | Quantia total que um proprietário possui, derivada da soma de seus UTXOs disponíveis. | Calculado sob demanda por `get_balance`; não é armazenado como um número fixo em nenhuma estrutura. | `core/utxo.py::get_balance` |
| **Transaction ID** | Identificador único de uma transação. | SHA-256 da representação `str()` do dicionário da transação (antes de o `transaction_id` ser adicionado a ele). | `core/transaction.py::new_transaction` |
| **Nó (node)** | Um participante/processo executando uma cópia do software e da blockchain. | Cada processo Flask executando `api/app.py` é um nó; possui um `node_identifier` gerado por UUID. | `api/app.py`, `network/node.py` |
| **Node ID** | Identificador único de um nó. | Gerado via `str(uuid4()).replace('-', '')`, tanto em `network/node.py::generate_node_id` (não usada) quanto diretamente em `api/app.py` (efetivamente usada). | `network/node.py`, `api/app.py` |
| **API** | Interface de programação através da qual sistemas externos interagem com o nó. | Conjunto de rotas HTTP Flask. | `api/app.py` |
| **Endpoint** | Uma rota HTTP específica da API. | `/mine`, `/transactions/new`, `/chain`, `/nodes/register`, `/nodes/resolve`. | `api/app.py` |
| **Consenso** | Mecanismo para que múltiplos nós concordem sobre qual é a cadeia válida. | Algoritmo "cadeia mais longa válida vence", implementado em `resolve_conflicts`, mas **não conectado** à classe `Blockchain` atualmente (ver Seção 19). | `network/consensus.py` |
| **Cadeia (chain)** | A sequência ordenada de blocos. | `Blockchain.chain` (lista de dicionários). | `core/blockchain.py` |
| **Validação** | Processo de verificar se uma estrutura de dados obedece às regras esperadas. | Validação estrutural de blocos (`valid_block`), validação de encadeamento e PoW (`valid_chain`), validação de UTXOs (`valid_utxo`). | `core/block.py`, `core/blockchain.py`, `core/utxo.py` |
| **Serialização** | Conversão de uma estrutura de dados em memória para um formato transmissível/armazenável. | `json.dumps` (para hash de blocos e para respostas HTTP via `jsonify`); `str()` (para o ID de transações). | `core/block.py`, `core/transaction.py`, `api/app.py` |
| **JSON** | Formato de dados textual, usado para troca de informações via HTTP. | Formato de entrada (`request.get_json()`) e saída (`jsonify(...)`) da API; também usado internamente para hash de blocos. | `api/app.py`, `core/block.py` |
| **Flask** | Microframework web em Python usado para expor a API HTTP. | Base de `api/app.py`. | `api/app.py` |
| **HTTP** | Protocolo de comunicação cliente-servidor usado pela API. | Todas as interações com o nó ocorrem via HTTP (GET/POST). | `api/app.py` |
| **GET** | Método HTTP usado para operações de leitura/consulta (ou, no caso de `/mine`, para disparar uma ação, embora convencionalmente GET devesse ser idempotente/sem efeitos colaterais). | Usado em `/mine`, `/chain`, `/nodes/resolve`. Note-se que `/mine` e `/nodes/resolve` **alteram o estado do servidor apesar de usarem GET**, o que diverge da convenção HTTP de que requisições GET não devem ter efeitos colaterais relevantes — ponto de atenção, não um erro de execução. | `api/app.py` |
| **POST** | Método HTTP usado para operações que criam ou submetem dados. | Usado em `/transactions/new`, `/nodes/register`. | `api/app.py` |
| **Status codes** | Códigos numéricos HTTP indicando o resultado de uma requisição. | `200` (sucesso/consulta), `201` (criado/aceito), `400` (erro do cliente). | `api/app.py` |

---

# 6. Blockchain

```text
Bloco 1 (gênese)
   ↓ hash
Bloco 2
   ↓ hash
Bloco 3
   ↓ hash
...
```

- **Criação do bloco gênese:** ocorre uma única vez, dentro de `Blockchain.__init__`, com valores fixos (`index=1`, `transactions=[]`, `proof=100`, `previous_hash=1`). Não há nenhuma verificação de que esse bloco seja "válido" no sentido de PoW — ele é aceito por construção.
- **Criação de novos blocos:** ocorre via `Blockchain.add_block(proof, previous_hash)`, chamado exclusivamente pela rota `GET /mine`. O `index` do novo bloco é sempre `len(self.chain) + 1`.
- **Índice:** campo inteiro armazenado dentro do próprio bloco, refletindo sua posição lógica na cadeia (começando em `1`), que coincide com `posição_na_lista + 1` desde que nenhum bloco seja removido da lista (o que nunca ocorre no código atual, exceto quando `resolve_conflicts` **substitui inteiramente** `self.chain` por uma nova lista recebida de outro nó — funcionalidade atualmente desconectada, ver Seção 19).
- **Timestamp:** armazenado como `float` (segundos desde a época Unix, via `time.time()`), gerado no instante em que `new_block` é executada.
- **Armazenamento de transações:** cada bloco guarda, em seu campo `transactions`, a lista de transações que estavam em `Blockchain.current_transactions` no momento em que `add_block` foi chamado. Após a criação do bloco, essa lista pendente é esvaziada.
- **`previous_hash`:** calculado **fora** da classe `Blockchain`, na rota `/mine` de `api/app.py` (`previous_hash = hash(last_block)`), e passado como parâmetro para `add_block`. A classe `Blockchain` não calcula esse valor sozinha ao adicionar um bloco — ela apenas armazena o valor que lhe é fornecido.
- **Cálculo do hash:** feito por `core/block.py::hash`, usando SHA-256 sobre a serialização JSON (chaves ordenadas) do bloco inteiro (incluindo `timestamp`, o que significa que o hash de um bloco depende do instante exato em que foi criado).
- **Validação da cadeia:** `Blockchain.valid_chain(chain)` percorre a cadeia recebida a partir do segundo bloco, verificando estrutura (`valid_block`), encadeamento de hash (`previous_hash == hash(bloco_anterior)`) e validade da prova (`valid_proof`).
- **Participação da Proof of Work na validação:** cada bloco (exceto o gênese) só é considerado válido em `valid_chain` se sua prova, combinada com a prova do bloco anterior, satisfizer `valid_proof`.
- **Detecção de bloco inválido:** qualquer uma das três verificações falhando faz `valid_chain` retornar `False` **imediatamente** (a função não continua verificando os blocos restantes após a primeira falha).

---

# 7. Transações

```text
Transaction
├── inputs
└── outputs
```

- **Input:** um UTXO existente sendo referenciado como fonte de valor para a nova transação. Estruturalmente, um input tem exatamente o mesmo formato de um UTXO (`transaction_id`, `output_index`, `owner`, `amount`), pois um input **é** um UTXO que está sendo apontado para ser gasto.
- **Output:** uma nova alocação de valor, definida apenas por `owner` e `amount` no momento da criação da transação; após a transação ser processada, cada output dá origem a um novo UTXO.
- **Cálculo dos valores:** `input_amount` é a soma de `amount` de todos os inputs; `output_amount` é a soma de `amount` de todos os outputs fornecidos pelo solicitante (antes da adição do troco).
- **Validação dos inputs:** cada input deve estar presente em `available_utxos` (via `valid_utxo`); se qualquer um não estiver, a transação inteira é rejeitada (`None`), sem processamento parcial.
- **Validação dos valores:** a transação é rejeitada se `output_amount > input_amount` (não é possível gastar mais do que os inputs fornecem).
- **Troco:** calculado como `input_amount - output_amount`; se positivo, um output adicional é criado automaticamente para `inputs[0]['owner']` — ou seja, o troco sempre retorna ao dono do **primeiro** input listado, independentemente de haver múltiplos inputs de diferentes proprietários.
- **Transaction ID:** gerado via SHA-256 de `str(transaction)`, calculado **antes** de o campo `transaction_id` existir dentro do próprio dicionário (a chave é adicionada logo depois, então não há uma referência circular).
- **Armazenamento:** a transação validada é anexada a `Blockchain.current_transactions` (pela rota `/transactions/new`), aguardando ser incluída no próximo bloco minerado.
- **Rejeição:** ocorre retornando `None` de `new_transaction`, o que a rota `/transactions/new` traduz para uma resposta HTTP `400 Invalid transaction`.

**Exemplo concreto (formato descrito no `Plano_de_producao.md`):**

```text
Alice possui 100 STL.
Alice envia 30 STL para Bob.

Input:
  100 STL (UTXO de Alice)

Outputs solicitados:
  30 STL → Bob

Cálculo:
  input_amount  = 100
  output_amount = 30
  change        = 100 - 30 = 70

Outputs finais (após acréscimo do troco):
  30 STL → Bob
  70 STL → Alice
```

Esse é exatamente o cenário coberto pelo teste `test_transaction` em `tests/test_transaction.py` (ver Seção 16).

---

# 8. UTXO

- **O que é:** um UTXO é um output de uma transação anterior (ou, no caso do projeto atual, um UTXO criado manualmente em testes/estado inicial) que ainda não foi usado como input em nenhuma outra transação.
- **Criação:** via `create_utxo(transaction_id, output_index, owner, amount)`, chamada dentro de `new_transaction` para cada output de uma transação recém-criada (incluindo o output de troco).
- **Campos:** `transaction_id` (de onde veio), `output_index` (posição dentro dos outputs daquela transação), `owner` (proprietário), `amount` (valor).
- **Identificação de origem:** por meio do par `(transaction_id, output_index)`, que aponta exatamente para qual output de qual transação deu origem àquele UTXO.
- **Disponibilidade:** um UTXO é considerado disponível simplesmente por estar presente na lista `available_utxos` — não há um campo booleano `spent` dentro do próprio UTXO; a disponibilidade é definida pela **presença ou ausência** do UTXO nessa lista externa.
- **Consumo:** ocorre em duas etapas simultâneas dentro de `new_transaction`: remoção de `available_utxos` e adição a `spent_utxos`.
- **Novos UTXOs:** criados a partir de cada output de uma transação bem-sucedida, incluindo o de troco.
- **Cálculo de saldo:** feito por `get_balance`, somando os `amount` de todos os UTXOs de `available_utxos` cujo `owner` corresponda ao solicitado.

```text
Transaction
      ↓ (cada output)
Output {owner, amount}
      ↓ create_utxo
UTXO {transaction_id, output_index, owner, amount}
      ↓ (referenciado como input em outra transação)
Input de outra Transaction
      ↓ new_transaction (validação + remoção)
UTXO consumido (removido de available_utxos, adicionado a spent_utxos)
```

---

# 9. Double-Spend (Gasto Duplo)

- **O que é:** a tentativa de usar o mesmo UTXO como input em mais de uma transação, o que permitiria, em teoria, gastar o mesmo valor duas vezes.
- **Por que é um problema:** em qualquer sistema de valor digital, se um mesmo "token" pudesse ser gasto repetidamente, o sistema não teria escassez nem integridade contábil confiável.
- **Estrutura que impede sua ocorrência (na implementação atual):** a lista `available_utxos`, combinada com a remoção imediata do UTXO consumido dentro de `new_transaction`.
- **Participação de `valid_utxo()`:** é a primeira barreira — antes de qualquer outro processamento, cada input é checado quanto à sua presença em `available_utxos`. Se o UTXO já foi removido (por ter sido gasto anteriormente), `valid_utxo` retorna `False` e a transação inteira é rejeitada.
- **Participação de `consume_utxo()`:** registra o UTXO em `spent_utxos` no momento em que ele é efetivamente utilizado como input de uma transação aceita — mas note-se que `consume_utxo` **não é o que impede o reuso**; quem impede é a remoção de `available_utxos` (`available_utxos.remove(utxo)`), realizada logo antes da chamada a `consume_utxo` dentro do mesmo laço. `spent_utxos` funciona, na implementação atual, apenas como um **registro histórico**, e não é consultado por `valid_utxo` para decidir se um UTXO pode ser gasto.
- **O que acontece quando o mesmo UTXO é utilizado novamente:** a segunda tentativa de `new_transaction` encontrará esse UTXO ausente de `available_utxos` (pois foi removido na primeira vez) e retornará `None` na etapa de validação dos inputs, antes de qualquer outra mutação de estado.
- **Limitações da implementação atual:**
  1. A proteção depende inteiramente do estado em memória de um único processo (`available_utxos`/`spent_utxos` definidos em `api/app.py`). Não há persistência, nem sincronização entre nós — se dois nós diferentes existissem simultaneamente (uma vez que a rede P2P ainda não está implementada), cada um teria sua própria lista de UTXOs disponíveis, e não haveria mecanismo atual para impedir que o mesmo UTXO fosse gasto de forma diferente em cada nó (isso, aliás, é justamente o problema que uma rede P2P com consenso resolveria, mas essa parte ainda não está implementada — FASE 7 e FASE 8 do planejamento).
  2. Não há verificação criptográfica (assinatura) provando que quem está gastando um UTXO é de fato seu proprietário — qualquer requisição HTTP pode alegar estar gastando um UTXO de qualquer `owner`, desde que o UTXO exista em `available_utxos` (FASE 3, criptografia, ainda não implementada).
  3. A prevenção de gasto duplo dentro do mesmo bloco não pendente ainda minerado depende apenas da mutação imediata e síncrona de `available_utxos` a cada chamada de `/transactions/new` — não há trava explícita contra condições de corrida (*race conditions*) caso requisições concorrentes cheguem simultaneamente ao processo Flask; **não é possível determinar, apenas pelos arquivos enviados, se o servidor Flask é executado em modo single-threaded ou multi-threaded em produção**, o que afetaria a real exposição a esse tipo de condição de corrida.
- Não se deve concluir que esta proteção seja equivalente à do Bitcoin: o Bitcoin depende de um razão distribuído com consenso entre milhares de nós independentes e verificação criptográfica de assinaturas; a Stella, na fase atual, depende de uma única lista em memória de um único processo.

---

# 10. Saldo

```text
UTXOs disponíveis (available_utxos)
       ↓
filtrar pelos que possuem owner == proprietário solicitado
       ↓
somar o campo amount de cada um
       ↓
saldo
```

O saldo **não é armazenado como um número em uma variável ou campo de "conta"** em nenhum lugar do sistema. Não existe, por exemplo, um dicionário `{'Alice': 100}` mantendo o saldo corrente. Em vez disso, o saldo é **derivado, sob demanda**, a partir do estado agregado de todos os UTXOs disponíveis pertencentes àquele proprietário, toda vez que `get_balance(owner, available_utxos)` é chamada. Essa é uma característica central do modelo UTXO: a "conta" de alguém é, conceitualmente, a soma de todos os "pedaços" de valor (UTXOs) que ainda não foram gastos e que apontam para esse proprietário — não existe um saldo persistente único que precise ser incrementado/decrementado a cada operação.

Atualmente, **não existe nenhum endpoint HTTP** que exponha `get_balance` — a função só é exercitada nos testes automatizados (`tests/test_transaction.py::test_balance`).

---

# 11. Mineração e Proof of Work

```text
último bloco
     ↓
última proof (last_proof = last_block['proof'])
     ↓
tentativa proof = 0 → valid_proof(last_proof, 0)?  não
     ↓
tentativa proof = 1 → valid_proof(last_proof, 1)?  não
     ↓
tentativa proof = 2 → ...
     ↓
... (repete incrementando proof)
     ↓
proof válida encontrada (hash começa com "0000")
     ↓
previous_hash = hash(last_block)
     ↓
novo bloco criado via blockchain.add_block(proof, previous_hash)
```

- **`proof_of_work` (efetivamente usada):** método da classe `Blockchain` (não a função de mesmo nome em `core/mining.py`, que é código morto — ver Seção 19). Recebe a última prova conhecida e testa candidatos sequenciais começando de `0`.
- **`valid_proof(last_proof, proof)`:** concatena as duas provas como texto (`f'{last_proof}{proof}'`), calcula o SHA-256 dessa string e verifica se os quatro primeiros caracteres hexadecimais são `"0000"`.
- **Dificuldade atual:** fixa em 4 zeros hexadecimais iniciais (`"0000"`), hardcoded dentro de `valid_proof`. Não há mecanismo de ajuste de dificuldade (a FASE 6 do planejamento lista "Ajuste de dificuldade, caso adotado pelo protocolo" como item pendente).
- **Número de zeros exigidos:** 4 caracteres hexadecimais, o que corresponde a uma probabilidade aproximada de sucesso de 1 em 65536 (16^4) por tentativa, assumindo uma distribuição uniforme dos hashes.
- **Processo de tentativa:** puramente sequencial e local (busca por força bruta incrementando um contador inteiro), sem paralelismo nem otimizações.
- **Hash utilizado:** SHA-256, o mesmo algoritmo usado para o hash de blocos, mas aplicado sobre uma entrada diferente (a concatenação textual das duas provas, não a serialização de um bloco inteiro).
- **Relação entre mineração e criação de blocos:** a prova válida encontrada é o valor que será armazenado no campo `proof` do novo bloco; sem essa prova, `add_block` não é chamado pela rota `/mine`.
- **Recompensa de mineração:** o código para criar uma transação de recompensa ao minerador está fisicamente presente na rota `/mine` de `api/app.py`, mas **comentado (desativado)**. Além disso, como observado na Seção 3.8, mesmo se fosse reativado tal como está escrito, ele usaria uma assinatura de chamada incompatível com `new_transaction` no modelo UTXO atual (é um resquício do modelo antigo `sender → recipient → amount`). Portanto, **na implementação atual, minerar um bloco não gera nenhuma recompensa em STL para o minerador** — isso é consistente com o planejamento, que lista "Recompensa" e "Coinbase transaction" como itens pendentes da FASE 6.

---

# 12. API

## `GET /mine`
- **Finalidade:** minerar (encontrar prova válida para) um novo bloco e adicioná-lo à cadeia.
- **Parâmetros/body:** nenhum.
- **Resposta (200):** JSON com `message`, `index`, `transactions`, `proof`, `previous_hash`.
- **Comportamento em erro:** não há tratamento de erro explícito nesta rota; uma falha inesperada (por exemplo, se `blockchain.chain` estivesse vazio, o que não ocorre na implementação atual pois o construtor sempre cria o gênese) resultaria em uma exceção não tratada pelo Flask (erro 500 padrão).
- **Funções internas chamadas:** `Blockchain.last_block`, `Blockchain.proof_of_work`, `core.block.hash`, `Blockchain.add_block`.
- **Alterações no estado:** adiciona um bloco a `blockchain.chain`; esvazia `blockchain.current_transactions`.

## `POST /transactions/new`
- **Finalidade:** submeter uma nova transação para a fila de transações pendentes.
- **Body esperado:** JSON `{'inputs': [...], 'outputs': [...]}`.
- **Resposta de sucesso (201):** `{'message': 'Transaction will be added to Block <index>'}`.
- **Resposta de erro (400):** `'Missing values'` (campos ausentes) ou `'Invalid transaction'` (UTXOs inválidos ou valores incompatíveis) — ambas como texto simples, não JSON, ao contrário das demais respostas de sucesso que usam `jsonify`.
- **Funções internas chamadas:** `core.transaction.new_transaction` (via alias `create_transaction`).
- **Alterações no estado:** pode modificar `available_utxos`, `spent_utxos` e `blockchain.current_transactions`.

## `GET /chain`
- **Finalidade:** consultar a cadeia completa de blocos do nó.
- **Resposta (200):** `{'chain': [...], 'length': N}`.
- **Alterações no estado:** nenhuma.

## `POST /nodes/register`
- **Finalidade:** registrar um ou mais nós vizinhos.
- **Body esperado:** JSON `{'nodes': [...]}`.
- **Resposta de sucesso (201):** mensagem e lista atual de nós.
- **Resposta de erro (400):** se `nodes` ausente.
- **Funções internas chamadas:** `blockchain.register_node(node)` para cada nó.
- **Status real de funcionamento:** **este endpoint não funciona na implementação atual**, pois `Blockchain` não define `register_node` (ver Seção 19). Uma chamada a esta rota, com um corpo JSON válido, resultará em erro interno do servidor (`AttributeError` não tratado, refletido pelo Flask como uma resposta HTTP `500 Internal Server Error`).

## `GET /nodes/resolve`
- **Finalidade:** executar o algoritmo de consenso, substituindo a cadeia local por uma cadeia válida mais longa encontrada entre os nós conhecidos.
- **Resposta (200):** mensagem informando se a cadeia foi substituída, junto com a cadeia (nova ou atual).
- **Status real de funcionamento:** **também não funciona na implementação atual**, pelo mesmo motivo — `Blockchain` não define `resolve_conflicts` (ver Seção 19). Uma chamada a esta rota resultará em `AttributeError` não tratado.

---

# 13. Fluxos Completos

## Fluxo de mineração
```text
requisição GET /mine
→ blockchain.last_block
→ blockchain.proof_of_work(last_proof)
→ (busca sequencial de proof até valid_proof ser verdadeiro)
→ hash(last_block) → previous_hash
→ blockchain.add_block(proof, previous_hash)
→ novo bloco anexado a blockchain.chain
→ blockchain.current_transactions esvaziada
→ resposta HTTP 200 (JSON)
```

## Fluxo de transação
```text
requisição POST /transactions/new (JSON: inputs, outputs)
→ validação de presença dos campos obrigatórios
→ create_transaction(inputs, outputs, available_utxos, spent_utxos)
    → validação de cada input via valid_utxo
    → cálculo de input_amount e output_amount
    → validação: output_amount <= input_amount
    → cálculo do troco e (se houver) criação de output de troco
    → montagem do dicionário da transação
    → cálculo do transaction_id (SHA-256 de str(transaction))
    → remoção dos UTXOs de input de available_utxos
    → registro dos UTXOs de input em spent_utxos
    → criação de novos UTXOs para cada output (incluindo troco)
→ se None: resposta HTTP 400
→ se transação válida: blockchain.current_transactions.append(transaction)
→ resposta HTTP 201
```

## Fluxo de validação da blockchain (`valid_chain`)
```text
recebe uma lista "chain" (por exemplo, vinda de outro nó)
→ define last_block = chain[0]  (bloco gênese recebido, não validado estruturalmente aqui)
→ para cada bloco a partir do índice 1:
    → valid_block(bloco)?          se não → False
    → bloco.previous_hash == hash(last_block)?   se não → False
    → valid_proof(last_block.proof, bloco.proof)?  se não → False
    → last_block = bloco; avança para o próximo
→ se percorreu toda a cadeia sem falhar: True
```

---

# 14. Estado do Sistema

| Estrutura | O que armazena | Quando é criada | Quando é modificada | Quem modifica | Quem consulta | Impacto de alteração |
|---|---|---|---|---|---|---|
| `blockchain.chain` | Lista de todos os blocos confirmados. | Na instanciação de `Blockchain` (com o gênese). | Ao chamar `add_block` (append); teoricamente também por `resolve_conflicts` (substituição completa), mas essa função está desconectada da classe (Seção 19). | `Blockchain.add_block` | `GET /chain`, `GET /mine` (via `last_block`), `valid_chain` (indiretamente, ao validar cadeias recebidas) | Cresce a cada mineração bem-sucedida; é a fonte de verdade sobre o estado confirmado da rede local. |
| `blockchain.current_transactions` | Transações pendentes, ainda não incluídas em um bloco. | Na instanciação de `Blockchain` (vazia). | Recebe `append` em `POST /transactions/new`; é esvaziada (`= []`) dentro de `add_block`. | `api/app.py::new_transaction` (rota), `Blockchain.add_block` | `Blockchain.add_block` (para incluí-las no novo bloco) | Determina quais transações entram no próximo bloco minerado. |
| `blockchain.nodes` | Conjunto de endereços (`netloc`) de nós conhecidos. | Na instanciação de `Blockchain` (conjunto vazio). | Deveria ser modificado por `register_node`, mas esse método não existe na classe atualmente (Seção 19) — **na prática, nunca é modificado por nenhum caminho de código funcional atualmente presente**. | Nenhum (ver observação) | `POST /nodes/register` (para exibir a lista atualizada), `resolve_conflicts` (para saber quais nós consultar) | Sem modificação funcional, `resolve_conflicts` nunca encontraria vizinhos para consultar, mesmo se estivesse conectada. |
| `available_utxos` | UTXOs ainda não gastos, conhecidos pelo processo da API. | Como lista vazia, no escopo de módulo de `api/app.py`. | `create_transaction`/`new_transaction` remove UTXOs consumidos e adiciona novos UTXOs de output. | `core/transaction.py::new_transaction` | `core/utxo.py::valid_utxo`, `core/utxo.py::get_balance`, `core/transaction.py::new_transaction` | Determina quais UTXOs podem ser usados como input em transações futuras e o saldo calculado de cada proprietário. |
| `spent_utxos` | Registro histórico de UTXOs já consumidos. | Como lista vazia, no escopo de módulo de `api/app.py`. | Recebe `append` via `consume_utxo`, dentro de `new_transaction`. | `core/utxo.py::consume_utxo` (chamado por `new_transaction`) | Nenhuma função do projeto lê `spent_utxos` para tomar decisões (não é usada para validar nada) — atualmente é apenas um registro passivo. | Nenhum impacto funcional direto atualmente; serve apenas como histórico não consultado. |
| `node_identifier` | Identificador único deste processo/nó. | Uma vez, na inicialização do módulo `api/app.py`, via `uuid4()`. | Nunca (imutável após criação). | — | Nenhuma rota o utiliza atualmente (o trecho que o usaria, na recompensa de mineração, está desativado). | Nenhum impacto funcional atual. |

---

# 15. Ciclo de Vida de uma Transação

```text
UTXO disponível (presente em available_utxos)
↓
selecionado como input em uma requisição POST /transactions/new
↓
validação: valid_utxo(utxo, available_utxos) → deve ser True
↓
validação: soma dos outputs <= soma dos inputs
↓
cálculo do troco (se input_amount > output_amount)
↓
transação criada (dict com inputs, outputs, transaction_id)
↓
UTXO(s) de input removidos de available_utxos
↓
UTXO(s) de input registrados em spent_utxos
↓
novos UTXOs criados para cada output (incluindo o de troco, se houver)
↓
novos UTXOs adicionados a available_utxos (agora disponíveis para futuras transações)
↓
transação anexada a blockchain.current_transactions (pendente)
↓
(em uma futura chamada a GET /mine) transação incluída no campo "transactions" do novo bloco
↓
blockchain.current_transactions esvaziada
```

Cada seta representa uma transição de estado real observável no código: a saída de um UTXO de `available_utxos` corresponde exatamente à sua entrada em `spent_utxos` (dentro do mesmo laço de `new_transaction`), e a criação de novos UTXOs ocorre imediatamente após, dentro da mesma chamada de função — não há um estado intermediário em que a transação exista sem que essas atualizações já tenham ocorrido.

---

# 16. Testes

O arquivo `tests/test_transaction.py` contém três funções de teste, todas baseadas em `assert` simples (compatíveis com execução via `pytest` ou diretamente).

## `test_transaction()`
- **O que está sendo testado:** a criação básica de uma transação, incluindo o cálculo correto do troco.
- **Preparação:** cria um único UTXO de 100 STL pertencente a "Alice" em `available_utxos`; `spent_utxos` vazio; um output de 30 STL para "Bob".
- **Execução:** chama `new_transaction(available_utxos.copy(), outputs, available_utxos, spent_utxos)`. Note que os **inputs** passados são uma **cópia** (`available_utxos.copy()`) da lista de UTXOs disponíveis no momento — ou seja, o teste está usando o conteúdo daquela lista como se fossem os UTXOs que o "usuário" possui e deseja gastar, mas passando explicitamente a lista original (`available_utxos`, não a cópia) como o parâmetro `available_utxos` da função, que é a estrutura que será efetivamente mutada.
- **Resultado esperado e verificado:**
  - `transaction is not None` (a transação foi aceita).
  - `transaction["outputs"][0]["amount"] == 30` (o output original para Bob permanece na posição 0).
  - `transaction["outputs"][1]["amount"] == 70` (o troco de Alice foi adicionado na posição 1, com valor `100 - 30 = 70`).
- **Conceito validado:** criação de transação, cálculo de troco, ordem de inserção dos outputs (o troco é sempre adicionado ao final da lista de outputs).

## `test_double_spend()`
- **O que está sendo testado:** que um UTXO já gasto não pode ser reutilizado em uma segunda transação.
- **Preparação:** um único UTXO de 100 STL de "Alice"; `spent_utxos` vazio.
- **Execução:**
  1. `first_transaction`: gasta o UTXO (via cópia da lista) para enviar 30 STL a Bob — isso remove o UTXO original de `available_utxos` e adiciona os novos UTXOs (30 para Bob, 70 de troco para Alice).
  2. `second_transaction`: tenta gastar um UTXO **recriado do zero** com os mesmos valores (`create_utxo("tx0", 0, "Alice", 100)`) — um novo objeto `dict`, mas estruturalmente idêntico ao original.
- **Resultado esperado e verificado:**
  - `first_transaction is not None` (a primeira transação foi aceita).
  - `second_transaction is None` (a segunda foi rejeitada).
- **Conceito validado:** a prevenção de gasto duplo funciona **por igualdade estrutural**, não por identidade de objeto — mesmo um UTXO reconstruído do zero, mas com os mesmos campos de um UTXO já removido de `available_utxos`, é corretamente identificado como indisponível, pois `in` compara por valor. Isso confirma que a implementação de `valid_utxo` é robusta a esse cenário específico de teste, embora (como discutido na Seção 9) essa proteção só valha dentro de um único processo/lista em memória.

## `test_balance()`
- **O que está sendo testado:** o cálculo agregado de saldo por proprietário.
- **Preparação:** três UTXOs — dois de "Alice" (70 e 20) e um de "Bob" (30).
- **Execução:** chama `get_balance("Alice", available_utxos)` e `get_balance("Bob", available_utxos)`.
- **Resultado esperado e verificado:** saldo de Alice = 90 (70+20); saldo de Bob = 30.
- **Conceito validado:** agregação correta por filtro de proprietário.

## Partes do projeto ainda sem testes automatizados
- `core/block.py` (`new_block`, `hash`, `valid_block`) — nenhum teste dedicado.
- `core/blockchain.py` (`Blockchain`, incluindo `add_block`, `valid_chain`, `proof_of_work`, `last_block`) — nenhum teste dedicado.
- `core/mining.py` (`proof_of_work`, `valid_proof`) — nenhum teste dedicado.
- `network/node.py` (`generate_node_id`) — nenhum teste dedicado.
- `network/consensus.py` (`register_node`, `resolve_conflicts`) — nenhum teste dedicado (e, como visto, a funcionalidade sequer está conectada ao restante do sistema).
- `api/app.py` (nenhuma das cinco rotas HTTP possui teste automatizado, como um teste de integração usando o cliente de testes do Flask).
- Casos de borda de `core/transaction.py` não cobertos pelos três testes existentes: transação com múltiplos inputs de proprietários diferentes; transação sem troco (`output_amount == input_amount`); transação com `inputs` vazio; transação com `outputs` vazio.

---

# 17. O que está implementado

| Funcionalidade | Status | Implementação |
|---|---|---|
| Estrutura de bloco | Implementado | `core/block.py::new_block` |
| Hash SHA-256 de bloco | Implementado | `core/block.py::hash` |
| Validação estrutural de bloco | Implementado | `core/block.py::valid_block` |
| Bloco gênese | Implementado | `core/blockchain.py::Blockchain.__init__` |
| Encadeamento de blocos / adição de blocos | Implementado | `core/blockchain.py::Blockchain.add_block` |
| Validação de cadeia (estrutura + hash + PoW) | Implementado (não valida o gênese) | `core/blockchain.py::Blockchain.valid_chain` |
| Proof of Work (busca de prova) | Implementado (duplicado em dois lugares, ver Seção 19) | `core/blockchain.py::Blockchain.proof_of_work`, `core/mining.py::proof_of_work` |
| Validação de prova | Implementado | `core/mining.py::valid_proof` |
| Transações (inputs/outputs) | Implementado | `core/transaction.py::new_transaction` |
| Criação de outputs | Implementado | `core/transaction.py::create_output` |
| UTXO (criação, disponibilidade, consumo) | Implementado | `core/utxo.py` |
| Troco | Implementado | `core/transaction.py::new_transaction` |
| Identificação única de transações | Implementado | `core/transaction.py::new_transaction` |
| Prevenção de gasto duplo | Implementado (limitada a um único processo em memória) | `core/transaction.py`, `core/utxo.py::valid_utxo` |
| Cálculo de saldo | Implementado (sem endpoint HTTP correspondente) | `core/utxo.py::get_balance` |
| API — mineração (`/mine`) | Implementado (sem recompensa de mineração) | `api/app.py::mine` |
| API — nova transação (`/transactions/new`) | Implementado | `api/app.py::new_transaction` |
| API — consulta de cadeia (`/chain`) | Implementado | `api/app.py::full_chain` |
| API — registro de nós (`/nodes/register`) | Implementado no nível da rota, **não funcional** (depende de método inexistente) | `api/app.py::register_nodes`, `network/consensus.py::register_node` |
| API — resolução de conflitos (`/nodes/resolve`) | Implementado no nível da rota, **não funcional** (depende de método inexistente) | `api/app.py::consensus`, `network/consensus.py::resolve_conflicts` |
| Geração de identificador de nó | Implementado, porém não conectado ao restante do fluxo | `network/node.py::generate_node_id`, `api/app.py` (geração inline duplicada) |
| Configuração central | Parcialmente implementado (constantes existem, mas nem todas são usadas) | `config.py` |
| Ponto de entrada padronizado | Implementado | `main.py` |
| Testes automatizados de transação/UTXO | Implementado | `tests/test_transaction.py` |
| Criptografia (chaves, assinatura) | Não implementado | `core/crypto.py` (stub vazio) |
| Carteiras | Não implementado | `core/wallet.py` (stub vazio) |
| Política monetária (supply, recompensa efetiva) | Não implementado | — |
| Rede P2P (descoberta, propagação, sincronização) | Não implementado | — |
| Consenso funcional entre nós | Não implementado (código escrito, mas desconectado) | `network/consensus.py` |

---

# 18. O que ainda não está implementado

Comparando o `Plano_de_producao.md` com o código:

- **FASE 0 — Fundação:** o planejamento marca todos os itens como concluídos (`[x]`), incluindo "Criar `Transaction`" e "Criar testes básicos". O código confirma isso: há separação entre lógica de blockchain e API, `Block` e `Transaction` existem, há configuração central (`config.py`) e testes básicos (`test_transaction.py`).
- **FASE 1 — Blocos:** todos os itens estão marcados como concluídos (`[x]`) no planejamento, e o código confirma: criação de blocos, hash SHA-256, referência ao bloco anterior, validação individual e validação de cadeia estão todos presentes em `core/block.py` e `core/blockchain.py`.
- **FASE 2 — Transações e UTXO:** o planejamento marca **todos** os itens como pendentes (`[ ]`) — UTXO, criação de outputs, consumo de UTXOs, troco, identificação única, prevenção de gasto duplo, validação de valores, cálculo de saldo. **Divergência importante:** o código já implementa, de fato, todos esses itens (`core/transaction.py`, `core/utxo.py`, testes correspondentes em `test_transaction.py`). Ou seja, **a implementação está tecnicamente à frente do que o checklist do planejamento indica** — o planejamento não foi atualizado para refletir o trabalho já realizado nesta fase.
- **FASE 3 — Criptografia:** nenhum item implementado; `core/crypto.py` é um stub vazio.
- **FASE 4 — Carteiras:** nenhum item implementado; `core/wallet.py` é um stub vazio.
- **FASE 5 — Economia da STL:** nenhuma constante de supply máximo ou recompensa de bloco (`MAX_SUPPLY`, `BLOCK_REWARD`) está definida em `config.py` ou em qualquer outro arquivo enviado.
- **FASE 6 — Mineração / Proof of Work:** o planejamento lista Proof of Work, dificuldade e validação da prova como itens desta fase — esses já estão implementados desde a FASE 1/fundação, tecnicamente. Porém, "Recompensa" e "Coinbase transaction" (itens explicitamente desta fase) **não estão implementados**: o trecho de código correspondente em `api/app.py::mine` está desativado (comentado) e, mesmo se reativado, usaria uma assinatura incompatível com o modelo UTXO atual.
- **FASE 7 — Rede P2P:** nenhum item implementado. `network/node.py` apenas gera um identificador; não há descoberta de nós, propagação de blocos/transações, nem comunicação real entre nós além da chamada HTTP unidirecional dentro de `resolve_conflicts` (que, além disso, está desconectada — ver Seção 19).
- **FASE 8 — Consenso:** o código de `network/consensus.py` implementa a lógica de "cadeia mais longa válida", mas **nenhum dos itens da fase pode ser considerado funcionalmente implementado**, pois essa lógica não está conectada à classe `Blockchain` (ver Seção 19) — na prática, chamar os endpoints correspondentes resulta em erro.
- **FASE 9 — Segurança do protocolo:** nenhuma atividade de teste de segurança adversarial documentada nos arquivos enviados.
- **FASE 10 — API e interface:** os cinco endpoints básicos listados no planejamento (`/transactions/new`, `/mine`, `/chain`, `/nodes/register`, `/nodes/resolve`) já existem no código, mas dois deles (`/nodes/register`, `/nodes/resolve`) não funcionam (ver Seção 19). Os itens adicionais sugeridos ("API para carteiras", "Consulta de saldo", "Consulta de transação", "Consulta de bloco", "Envio de MRC") **não estão implementados**.
- **FASE 11 — Teste de rede:** não há evidência, nos arquivos enviados, de testes de rede distribuída com múltiplos nós.

**Funcionalidades que existem mas ainda não estão integradas:**
- `network/consensus.py::register_node` e `resolve_conflicts` — código escrito, mas nunca importado nem conectado à classe `Blockchain`.
- `network/node.py::generate_node_id` — código escrito e importado, mas nunca chamado.
- `core/mining.py::proof_of_work` — código escrito, mas nunca chamado (substituído, na prática, pelo método equivalente dentro de `Blockchain`).
- O trecho de recompensa de mineração em `api/app.py::mine` — presente no código-fonte como comentário, mas desativado e desatualizado em relação ao modelo UTXO.

---

# 19. Inconsistências e Pontos de Atenção

Esta seção documenta problemas técnicos identificados exclusivamente a partir da leitura do código. Nenhuma correção foi aplicada; apenas observação.

### 19.1 — Endpoints `/nodes/register` e `/nodes/resolve` estão quebrados
- **Arquivo(s):** `api/app.py`, `core/blockchain.py`, `network/consensus.py`.
- **Trecho:** `api/app.py` chama `blockchain.register_node(node)` e `blockchain.resolve_conflicts()`.
- **Problema:** a classe `Blockchain`, definida em `core/blockchain.py`, **não define os métodos `register_node` nem `resolve_conflicts`**. Essas funções existem em `network/consensus.py`, escritas com `self` como primeiro parâmetro (sugerindo a intenção de serem métodos de `Blockchain`), mas **`network/consensus.py` não é importado por nenhum arquivo do projeto** — nem por `core/blockchain.py`, nem por `api/app.py`. Não há atribuição do tipo `Blockchain.register_node = register_node`, nem herança, nem mixin, que conectasse essas funções à classe.
- **Causa:** aparente etapa de integração não concluída entre a definição das funções de consenso e sua efetiva ligação à classe `Blockchain`.
- **Consequência:** qualquer chamada às rotas `POST /nodes/register` ou `GET /nodes/resolve` resulta em `AttributeError: 'Blockchain' object has no attribute 'register_node'` (ou `'resolve_conflicts'`), que o Flask, por padrão, converteria em uma resposta HTTP `500 Internal Server Error`.
- **Gravidade:** alta — duas das cinco rotas documentadas na API não funcionam.
- **Impede a execução?** Não impede a inicialização do servidor nem o funcionamento das demais rotas (`/mine`, `/transactions/new`, `/chain`), mas impede completamente o funcionamento de qualquer fluxo de rede/consenso.

### 19.2 — `network/consensus.py` nunca é importado
- **Arquivo(s):** `network/consensus.py`.
- **Problema:** consequência direta do item 19.1 — o módulo inteiro está "órfão", sem nenhum ponto de entrada que o carregue.
- **Consequência:** o código de `register_node`/`resolve_conflicts` nunca é sequer carregado em memória durante a execução normal da aplicação (a menos que algum outro arquivo não enviado o importe, o que não pode ser confirmado nem descartado apenas pelos arquivos disponíveis).
- **Gravidade:** alta (mesma raiz do item 19.1).

### 19.3 — Duplicação do algoritmo de Proof of Work
- **Arquivo(s):** `core/mining.py`, `core/blockchain.py`.
- **Trecho:** `core/mining.py::proof_of_work(last_proof)` e `Blockchain.proof_of_work(self, last_proof)` implementam exatamente o mesmo algoritmo (mesmo laço, mesma dependência de `valid_proof`).
- **Problema:** duplicação de lógica em dois lugares diferentes; apenas a versão dentro de `Blockchain` é efetivamente usada por `api/app.py`.
- **Consequência:** não há erro de execução — o código funciona corretamente — mas há risco de manutenção: se a lógica precisar mudar no futuro, é preciso lembrar de atualizar dois lugares, ou a função não utilizada de `core/mining.py` se tornará ainda mais divergente/obsoleta silenciosamente.
- **Gravidade:** baixa/média (dívida técnica, não erro funcional).

### 19.4 — Dificuldade da PoW duplicada entre `config.py` e `core/mining.py`
- **Arquivo(s):** `config.py`, `core/mining.py`.
- **Trecho:** `config.py` define `POW_DIFFICULTY = "0000"`; `core/mining.py::valid_proof` usa o literal `"0000"` diretamente, sem importar `config.POW_DIFFICULTY`.
- **Problema:** a constante `config.POW_DIFFICULTY` não é a fonte real de verdade da dificuldade — mudar seu valor em `config.py` **não** teria nenhum efeito sobre o comportamento real da mineração, pois `mining.py` não a consulta.
- **Consequência:** risco de configuração "fantasma" — alguém poderia alterar `POW_DIFFICULTY` esperando mudar a dificuldade, sem perceber que o valor real está hardcoded em outro arquivo.
- **Gravidade:** média (não quebra a execução, mas é uma armadilha de manutenção).

### 19.5 — Estado de UTXOs mantido na camada de API, não no núcleo
- **Arquivo(s):** `api/app.py`.
- **Trecho:** `available_utxos = []` e `spent_utxos = []` são definidos como variáveis globais de módulo em `api/app.py`, e não como atributos da classe `Blockchain` ou de alguma outra estrutura do pacote `core`.
- **Problema:** o próprio `Plano_de_producao.md`, na FASE 10, estabelece a regra de que a API não deve conter as regras fundamentais da blockchain, devendo apenas se comunicar com o núcleo do protocolo. Manter as listas de UTXOs (que são estado central e fundamental do protocolo, não um detalhe de apresentação HTTP) diretamente no módulo da API é uma tensão com essa regra declarada no planejamento.
- **Consequência:** não há erro de execução; o sistema funciona. Porém, arquiteturalmente, isso mistura responsabilidades — testar ou reutilizar a lógica de UTXOs fora do contexto de uma requisição Flask exige acessar variáveis globais de `api/app.py` em vez de um objeto de domínio autocontido.
- **Gravidade:** baixa/média (dívida arquitetural, não erro funcional).

### 19.6 — `generate_node_id` importada mas nunca chamada
- **Arquivo(s):** `api/app.py`, `network/node.py`.
- **Trecho:** `from network.node import generate_node_id` em `api/app.py`, seguido de `node_identifier = str(uuid4()).replace('-', '')` diretamente, duplicando manualmente a mesma lógica que `generate_node_id()` já encapsula.
- **Problema:** import morto e duplicação de lógica idêntica.
- **Consequência:** nenhuma consequência funcional (o resultado é o mesmo), apenas redundância de código.
- **Gravidade:** baixa.

### 19.7 — Import não utilizado: `new_block` em `api/app.py`
- **Arquivo(s):** `api/app.py`.
- **Trecho:** `from core.block import new_block, hash` — `new_block` nunca é chamado diretamente neste arquivo.
- **Problema:** import morto.
- **Gravidade:** baixa.

### 19.8 — Import não utilizado: `new_transaction` em `core/blockchain.py`
- **Arquivo(s):** `core/blockchain.py`.
- **Trecho:** `from core.transaction import new_transaction` — nunca referenciado dentro do arquivo.
- **Problema:** import morto.
- **Gravidade:** baixa.

### 19.9 — Variável `node_identifier` sem uso funcional atual
- **Arquivo(s):** `api/app.py`.
- **Trecho:** `node_identifier` é gerado, mas o único trecho que o consumiria (a criação de uma transação de recompensa de mineração) está comentado.
- **Problema:** código morto/reservado para uma funcionalidade futura desativada.
- **Gravidade:** baixa (é uma reserva explícita para a FASE 6, não um bug).

### 19.10 — Trecho de recompensa de mineração incompatível com o modelo UTXO
- **Arquivo(s):** `api/app.py`.
- **Trecho:** `"""transaction = create_transaction("0", node_identifier, 1)"""` (comentado).
- **Problema:** mesmo que fosse descomentado, essa chamada usa uma assinatura de dois argumentos posicionais mais um terceiro (`"0"`, `node_identifier`, `1`), incompatível com a assinatura real de `new_transaction(inputs, outputs, available_utxos, spent_utxos)` (quatro parâmetros, os dois primeiros sendo listas estruturadas, não um remetente/destinatário/valor simples).
- **Consequência:** se alguém reativasse ingenuamente essa linha sem reescrevê-la, o código geraria um `TypeError` (número incorreto de argumentos) ao ser executado.
- **Gravidade:** baixa, pois está desativado, mas é um ponto de atenção relevante para quando a FASE 6 (recompensa de mineração) for retomada.
- **Status:** incompatibilidade de integração latente (resquício de um modelo de transação anterior — `sender → recipient → amount` — mencionado no cabeçalho de `core/transaction.py` como o modelo que "será substituído" pelo modelo UTXO, substituição essa que já ocorreu no restante do arquivo, mas não neste trecho comentado de `app.py`).

### 19.11 — A função `hash()` de `core/block.py` sobrescreve a função embutida `hash()` do Python
- **Arquivo(s):** `core/block.py`, e qualquer arquivo que faça `from core.block import hash` (`core/blockchain.py`, `api/app.py`).
- **Trecho:** `def hash(block): ...`.
- **Problema:** dentro dos módulos que importam essa função dessa forma, o nome `hash` deixa de se referir à função embutida do Python (usada, por exemplo, para calcular o hash de tipos primitivos como `frozenset` ou `str` para uso em `dict`/`set`) e passa a se referir exclusivamente a esta função customizada.
- **Consequência:** não há erro atual, pois nenhum desses módulos usa a função `hash()` embutida do Python para outro propósito. Porém, é uma armadilha potencial para desenvolvimento futuro nesses arquivos.
- **Gravidade:** baixa (estilístico/preventivo).

### 19.12 — Metodologia de hash diferente entre blocos e transações
- **Arquivo(s):** `core/block.py`, `core/transaction.py`.
- **Trecho:** `core/block.py::hash` usa `json.dumps(block, sort_keys=True).encode()`; `core/transaction.py::new_transaction` usa `str(transaction).encode()` para gerar o `transaction_id`.
- **Problema:** duas abordagens diferentes de serialização para dois hashes distintos dentro do mesmo projeto. `str()` sobre um dicionário Python usa a representação `repr` de cada valor, que pode variar conforme a versão do Python ou conforme tipos de dados internos, e não garante a mesma normalização que `json.dumps(..., sort_keys=True)` oferece.
- **Consequência:** não há erro de execução — cada `transaction_id` é calculado de forma consistente internamente (a mesma função sempre gera o mesmo hash para o mesmo dicionário, na mesma execução), mas a falta de uma metodologia unificada de serialização é uma inconsistência de projeto.
- **Gravidade:** baixa/média (dívida de consistência interna).

### 19.13 — `spent_utxos` não é utilizada para nenhuma validação
- **Arquivo(s):** `core/utxo.py`, `core/transaction.py`.
- **Trecho:** `consume_utxo` apenas adiciona a `spent_utxos`; nenhuma função do projeto (`valid_utxo` incluída) consulta `spent_utxos` para decidir algo.
- **Problema:** a prevenção de gasto duplo depende inteiramente da lista `available_utxos`; `spent_utxos` é, atualmente, apenas um registro histórico não utilizado para qualquer verificação.
- **Consequência:** nenhuma, funcionalmente (o sistema já funciona sem consultar `spent_utxos`), mas é digno de nota, já que o nome sugere um papel mais ativo do que o que de fato desempenha hoje.
- **Gravidade:** baixa.

### 19.14 — `new_transaction` muta a lista `outputs` recebida do chamador
- **Arquivo(s):** `core/transaction.py`.
- **Trecho:** `outputs.append(create_output(inputs[0]['owner'], change))`.
- **Problema:** a função modifica, por efeito colateral, o objeto `outputs` que lhe foi passado (em vez de, por exemplo, construir e retornar uma nova lista). Isso significa que, em `api/app.py`, a lista `values['outputs']` obtida do corpo JSON da requisição é alterada mesmo internamente ao servidor.
- **Consequência:** não há erro funcional na implementação atual (o chamador atual não reutiliza a lista `outputs` depois de chamar `new_transaction`), mas é um padrão de mutação implícita que pode gerar bugs sutis caso o chamador dependa do valor original de `outputs` após a chamada.
- **Gravidade:** baixa/média (boa prática de design, não bug ativo).

### 19.15 — Rotas `GET` com efeitos colaterais
- **Arquivo(s):** `api/app.py`.
- **Trecho:** `GET /mine` e `GET /nodes/resolve` alteram o estado do servidor (respectivamente, criam um bloco e potencialmente substituem toda a cadeia), apesar de usarem o método HTTP `GET`, convencionalmente reservado para operações seguras/idempotentes de leitura.
- **Problema:** divergência da convenção REST/HTTP.
- **Consequência:** nenhuma consequência de execução dentro do próprio sistema, mas pode causar efeitos colaterais indesejados se, por exemplo, ferramentas de cache, crawlers, ou pré-carregamento de links acessarem essas URLs via GET sem intenção de disparar uma ação.
- **Gravidade:** baixa/média (boa prática de API, não erro funcional imediato).

### 19.16 — Respostas de erro inconsistentes (texto simples vs. JSON)
- **Arquivo(s):** `api/app.py`.
- **Trecho:** respostas de sucesso usam `jsonify(...)`; respostas de erro em `/transactions/new` (`'Missing values', 400` e `'Invalid transaction', 400`) e em `/nodes/register` (`"Error: ...", 400`) retornam strings simples, não JSON.
- **Problema:** um cliente da API que espera sempre receber JSON precisaria tratar dois formatos de corpo de resposta diferentes dependendo do status.
- **Gravidade:** baixa (questão de padronização de API, não erro de execução).

### 19.17 — Ausência de tratamento de exceções em `resolve_conflicts`
- **Arquivo(s):** `network/consensus.py`.
- **Trecho:** `response = requests.get(f'http://{node}/chain')` sem bloco `try/except`.
- **Problema:** falhas de rede (nó indisponível, timeout, erro de conexão) não são tratadas e propagariam como exceção não capturada.
- **Consequência:** mesmo que esta função estivesse conectada à classe `Blockchain` (ver 19.1), uma única falha de conexão com um vizinho interromperia toda a checagem dos demais vizinhos.
- **Gravidade:** média (mas condicionada à resolução prévia do item 19.1, já que a função sequer é alcançável atualmente).

### 19.18 — Bloco gênese não é validado por `valid_chain`
- **Arquivo(s):** `core/blockchain.py`.
- **Trecho:** o laço de `valid_chain` começa em `current_index = 1`, nunca chamando `valid_block(chain[0])` nem verificando seu conteúdo.
- **Problema:** uma cadeia recebida de outro nó com um bloco gênese estruturalmente inválido, ou com valores de gênese diferentes dos esperados (`index`, `proof`, `previous_hash` diferentes do padrão local), seria aceita sem qualquer verificação sobre esse primeiro elemento.
- **Gravidade:** média (relevante apenas quando/se `resolve_conflicts` for conectada, ver 19.1).

### 19.19 — Duplo ponto de entrada (`app.py` standalone vs. `main.py`)
- **Arquivo(s):** `api/app.py`, `main.py`.
- **Trecho:** `api/app.py` possui seu próprio `if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)` com valores hardcoded, enquanto `main.py` executa a mesma aplicação usando `config.DEFAULT_HOST`/`config.DEFAULT_PORT`.
- **Problema:** existem dois caminhos possíveis para iniciar o servidor, com configurações potencialmente divergentes (ainda que, atualmente, `DEFAULT_HOST`/`DEFAULT_PORT` tenham os mesmos valores hardcoded em `api/app.py`, isso é coincidência de valores, não uma relação garantida pelo código).
- **Consequência:** se `config.py` for alterado no futuro (por exemplo, mudar a porta padrão), rodar `python app.py` diretamente continuaria usando a porta antiga, hardcoded, enquanto `python main.py` usaria a nova.
- **Gravidade:** baixa/média (dívida de manutenção).

---

# 20. Diferença entre Stella e Bitcoin

| Conceito | Bitcoin | Stella (implementação atual) |
|---|---|---|
| Modelo UTXO | UTXOs com scripts de bloqueio/desbloqueio (`scriptPubKey`/`scriptSig`), permitindo condições de gasto arbitrariamente complexas. | UTXOs simples, identificados apenas por `owner` (uma string), sem qualquer script ou condição de gasto. Não especificado na implementação atual se `owner` corresponde a algum tipo de endereço criptográfico — atualmente é apenas um identificador textual livre. |
| Transações | Assinadas digitalmente por cada input, com verificação de assinatura obrigatória. | Não há assinatura nem verificação criptográfica de propriedade (FASE 3, não implementada); qualquer requisição pode declarar `owner` livremente. |
| Mineração | Proof of Work com dificuldade ajustada dinamicamente (a cada 2016 blocos, aproximadamente), recompensa de bloco com halving programado, coinbase transaction. | Dificuldade fixa (`"0000"`), sem ajuste dinâmico; sem recompensa de mineração efetiva (código de recompensa comentado e desatualizado); sem coinbase transaction funcional. |
| Blocos | Cabeçalho de bloco com múltiplos campos (versão, merkle root, bits, nonce, etc.), corpo com lista de transações. | Estrutura simplificada: `index`, `timestamp`, `transactions`, `proof`, `previous_hash` — sem merkle root, sem campo de versão, sem "bits" de dificuldade codificados no próprio bloco. |
| Hashes | Duplo SHA-256 (SHA-256 aplicado duas vezes) sobre o cabeçalho do bloco. | SHA-256 aplicado uma única vez sobre a serialização JSON do bloco inteiro (incluindo as transações completas, não apenas um merkle root). |
| Rede | Rede P2P real com descoberta de nós (DNS seeds), propagação por gossip de blocos e transações, múltiplos milhares de nós. | Não implementada (FASE 7 pendente); a única comunicação entre nós prevista (`requests.get` em `resolve_conflicts`) não está sequer conectada à classe `Blockchain` atualmente. |
| Consenso | Cadeia de maior trabalho acumulado (não necessariamente a mais longa em número de blocos, mas a de maior dificuldade cumulativa), validado por milhares de nós independentes. | Algoritmo simplificado de "cadeia mais longa" por número de blocos (`length`), sem considerar dificuldade acumulada; e, na prática, não conectado/funcional atualmente. |
| Carteiras | Chaves privadas/públicas com derivação hierárquica (BIP32/39/44), endereços derivados de chaves públicas. | Não implementada (FASE 4 pendente; `core/wallet.py` vazio). |
| Criptografia | ECDSA (curva secp256k1) para assinaturas. | Não implementada (FASE 3 pendente; `core/crypto.py` vazio). |
| Emissão monetária | Supply máximo de 21 milhões de BTC, recompensa de bloco decrescente por halving. | Não definida (FASE 5 pendente); não há constantes de supply máximo ou recompensa no código fornecido. |

**Importante:** a implementação atual da Stella **não oferece garantias de segurança equivalentes às do Bitcoin** em nenhuma das dimensões acima — ausência de assinaturas criptográficas, ausência de rede distribuída funcional, dificuldade fixa e ausência de persistência tornam o sistema atual adequado apenas para fins de estudo em um único processo local, não para uso como meio de troca de valor real.

---

# 21. Exemplo Completo: Alice → Bob

**Estado inicial:**
```text
available_utxos = [
  {transaction_id: "tx0", output_index: 0, owner: "Alice", amount: 100}
]
spent_utxos = []
blockchain.current_transactions = []
```

**Requisição:** `POST /transactions/new` com corpo:
```json
{
  "inputs": [{"transaction_id": "tx0", "output_index": 0, "owner": "Alice", "amount": 100}],
  "outputs": [{"owner": "Bob", "amount": 30}]
}
```

**Passo a passo dentro de `new_transaction`:**
1. Validação do input: `{"transaction_id": "tx0", ...}` está presente em `available_utxos`? Sim → prossegue.
2. `input_amount = 100`; `output_amount = 30`.
3. `output_amount (30) > input_amount (100)`? Não → prossegue.
4. `change = 100 - 30 = 70`. Como `change > 0`, cria `{'owner': 'Alice', 'amount': 70}` e adiciona a `outputs`.
5. `outputs` agora é `[{"owner": "Bob", "amount": 30}, {"owner": "Alice", "amount": 70}]`.
6. Monta `transaction = {"inputs": [...], "outputs": [...]}`.
7. Calcula `transaction_id = sha256(str(transaction)).hexdigest()` (valor hexadecimal específico, dependente da representação exata da string — não especificado literalmente aqui, pois depende de detalhes de formatação do `str()` do Python).
8. Remove o UTXO original de `available_utxos` (agora vazio) e o adiciona a `spent_utxos`.
9. Cria dois novos UTXOs:
   - `{"transaction_id": <novo_id>, "output_index": 0, "owner": "Bob", "amount": 30}`
   - `{"transaction_id": <novo_id>, "output_index": 1, "owner": "Alice", "amount": 70}`
10. Adiciona ambos a `available_utxos`.

**Estado final:**
```text
available_utxos = [
  {transaction_id: <novo_id>, output_index: 0, owner: "Bob",   amount: 30},
  {transaction_id: <novo_id>, output_index: 1, owner: "Alice", amount: 70}
]
spent_utxos = [
  {transaction_id: "tx0", output_index: 0, owner: "Alice", amount: 100}
]
blockchain.current_transactions = [transaction]  # após o append feito pela rota
```

**Saldos após a transação:**
- `get_balance("Alice", available_utxos) = 70`
- `get_balance("Bob", available_utxos) = 30`

A transação permanece em `blockchain.current_transactions` até que `GET /mine` seja chamada, momento em que ela é incluída no campo `transactions` do novo bloco e a fila de pendentes é esvaziada.

---

# 22. Referência Rápida

### Arquivos

| Arquivo | Função |
|---|---|
| `core/block.py` | Estrutura, hash e validação de blocos. |
| `core/blockchain.py` | Classe `Blockchain`: cadeia, PoW, validação de cadeia. |
| `core/transaction.py` | Criação de transações UTXO. |
| `core/utxo.py` | Estrutura e operações sobre UTXOs. |
| `core/mining.py` | Algoritmo de Proof of Work. |
| `core/wallet.py` | Stub vazio (FASE 4). |
| `core/crypto.py` | Stub vazio (FASE 3). |
| `network/node.py` | Geração de ID de nó. |
| `network/consensus.py` | Registro de nós e resolução de conflitos (desconectado, ver Seção 19). |
| `api/app.py` | Aplicação Flask e rotas HTTP. |
| `config.py` | Constantes centrais. |
| `main.py` | Ponto de entrada. |
| `tests/test_transaction.py` | Testes de transação/UTXO. |
| `requirements.txt` | Dependências (`flask`, `requests`). |

### Classes

| Classe | Responsabilidade |
|---|---|
| `Blockchain` | Gerenciar a cadeia de blocos, transações pendentes, e nós conhecidos (`nodes`, embora sem método funcional para populá-lo atualmente). |

### Funções

| Função | Arquivo | Responsabilidade |
|---|---|---|
| `new_block` | `core/block.py` | Criar a estrutura de um bloco. |
| `hash` | `core/block.py` | Calcular hash SHA-256 de um bloco. |
| `valid_block` | `core/block.py` | Validar estrutura/tipos de um bloco. |
| `Blockchain.__init__` | `core/blockchain.py` | Inicializar cadeia com bloco gênese. |
| `Blockchain.add_block` | `core/blockchain.py` | Criar e anexar novo bloco. |
| `Blockchain.valid_chain` | `core/blockchain.py` | Validar uma cadeia recebida. |
| `Blockchain.proof_of_work` | `core/blockchain.py` | Buscar prova válida. |
| `Blockchain.last_block` | `core/blockchain.py` | Property: retorna o último bloco. |
| `create_output` | `core/transaction.py` | Criar um output de transação. |
| `new_transaction` | `core/transaction.py` | Criar e validar uma transação UTXO. |
| `create_utxo` | `core/utxo.py` | Criar um UTXO. |
| `consume_utxo` | `core/utxo.py` | Registrar UTXO como gasto. |
| `valid_utxo` | `core/utxo.py` | Verificar disponibilidade de um UTXO. |
| `get_balance` | `core/utxo.py` | Somar UTXOs disponíveis de um proprietário. |
| `proof_of_work` (módulo) | `core/mining.py` | Buscar prova válida (não utilizada, ver Seção 19). |
| `valid_proof` | `core/mining.py` | Validar uma prova de trabalho. |
| `generate_node_id` | `network/node.py` | Gerar ID de nó (não utilizada, ver Seção 19). |
| `register_node` | `network/consensus.py` | Registrar nó vizinho (desconectada, ver Seção 19). |
| `resolve_conflicts` | `network/consensus.py` | Resolver conflitos entre cadeias (desconectada, ver Seção 19). |
| `mine` | `api/app.py` | Rota `GET /mine`. |
| `new_transaction` (rota) | `api/app.py` | Rota `POST /transactions/new`. |
| `full_chain` | `api/app.py` | Rota `GET /chain`. |
| `register_nodes` | `api/app.py` | Rota `POST /nodes/register` (quebrada). |
| `consensus` | `api/app.py` | Rota `GET /nodes/resolve` (quebrada). |

### Estruturas

| Estrutura | Conteúdo |
|---|---|
| Bloco | `index`, `timestamp`, `transactions`, `proof`, `previous_hash`. |
| Transação | `inputs`, `outputs`, `transaction_id`. |
| Output | `owner`, `amount`. |
| UTXO | `transaction_id`, `output_index`, `owner`, `amount`. |

### Endpoints

| Método | Endpoint | Função |
|---|---|---|
| GET | `/mine` | Minerar novo bloco. |
| POST | `/transactions/new` | Submeter nova transação. |
| GET | `/chain` | Consultar cadeia completa. |
| POST | `/nodes/register` | Registrar nós vizinhos (não funcional atualmente). |
| GET | `/nodes/resolve` | Resolver conflitos entre cadeias (não funcional atualmente). |

### Conceitos

| Conceito | Onde aparece |
|---|---|
| Hash encadeado | `core/block.py`, `core/blockchain.py::valid_chain` |
| Proof of Work | `core/mining.py`, `core/blockchain.py` |
| UTXO | `core/utxo.py`, `core/transaction.py` |
| Double-spend prevention | `core/transaction.py`, `core/utxo.py::valid_utxo` |
| Consenso (não conectado) | `network/consensus.py` |

---

# 23. Observações Finais sobre Escopo e Fidelidade

Este documento foi construído exclusivamente a partir da leitura integral dos arquivos fornecidos: `app.py`, `wallet.py`, `block.py`, `blockchain.py`, `crypto.py`, `mining.py`, `transaction.py`, `utxo.py`, `consensus.py`, `node.py`, `test_transaction.py`, `requirements.txt`, `config.py`, `main.py` e `Plano_de_producao.md`. Nenhuma funcionalidade foi presumida como implementada além do que o código demonstra; onde havia dúvida legítima (por exemplo, se o servidor Flask roda em modo single ou multi-thread, ou onde fisicamente os arquivos residem em disco), isso foi declarado explicitamente como não determinável a partir dos arquivos enviados. As divergências entre o planejamento (`Plano_de_producao.md`) e a implementação real foram apresentadas separadamente, sem presumir que uma reflete automaticamente a outra.
