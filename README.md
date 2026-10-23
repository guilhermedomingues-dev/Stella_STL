# Stella (STL)

Stella é uma moeda digital experimental baseada em **UTXO** e **Proof of Work**, construída do zero em Python. Ela funciona como um site: você cria uma conta, ganha uma carteira, minera blocos e envia STL para outros usuários, tudo pelo navegador.

> **Projeto educacional.** A Stella foi criada para aprender e demonstrar como uma blockchain funciona por dentro. Não é um produto, não tem valor monetário e não deve ser usada para guardar ou movimentar valor real.

## Como usar

Tudo é feito pelo site, sem instalar nada:

1. **Crie sua conta** em `/register`. Ao cadastrar, você recebe um **ID de login** numérico e uma carteira própria.
2. **Entre** em `/login` com o seu ID e a senha.
3. **Minere** em `/mine` para produzir um bloco e receber a recompensa na sua carteira.
4. **Envie STL** em `/send`, informando o ID do destinatário e o valor. O site confirma o nome do destinatário antes do envio.
5. **Receba** compartilhando o seu ID de login (página `/receive`).
6. **Acompanhe** seu saldo em `/balance`, seu histórico em `/transactions` e qualquer bloco da cadeia em `/blocks`.

## Páginas do site

| Página | O que faz |
|---|---|
| `/register`, `/login`, `/logout` | Cadastro e sessão |
| `/home` | Painel com saldo e dados da conta |
| `/wallet` | Endereço da sua carteira |
| `/balance` | Saldo e últimas transações |
| `/send`, `/receive` | Enviar e receber STL |
| `/transactions` | Histórico completo da sua conta |
| `/blocks` | Explorador de blocos da cadeia |
| `/mine` | Minerar um bloco |
| `/account` | Dados da conta |

## Como a Stella funciona

```
Usuário cria a transação → ela é assinada com a chave privada → vai para a mempool
→ um minerador a inclui em um bloco → resolve o Proof of Work
→ o bloco é aceito pela rede → as saídas viram novos UTXOs
```

- **Modelo UTXO:** o saldo de cada usuário é a soma das saídas de transação ainda não gastas.
- **Proof of Work:** mineração com SHA-256 e dificuldade ajustada conforme o tempo entre blocos.
- **Emissão limitada:** novas STL só surgem como recompensa de bloco, até o teto de 20.000.000 STL, com halving programado.
- **Taxas:** quando a recompensa de bloco chegar a zero, as taxas de transação passam a remunerar os mineradores.
- **Mempool:** transações pendentes ficam guardadas até entrarem em um bloco.
- **Rede de nós:** nós da Stella trocam blocos e transações entre si e resolvem divergências adotando a cadeia válida com mais trabalho acumulado.

### Parâmetros do protocolo

Definidos em [`config.py`](config.py):

| Parâmetro | Valor |
|---|---|
| Fornecimento máximo | 20.000.000 STL |
| Recompensa inicial por bloco | 50 STL |
| Halving | a cada 200.000 blocos (até 33 halvings) |
| Menor unidade | 1 Saint = 0,00000001 STL (1 STL = 100.000.000 Saints) |
| Tempo-alvo entre blocos | 600 s |
| Maturação da coinbase | 1 bloco |
| Limite da mempool | 1.000 transações |
| Taxa de transação | 0,1% do valor (mínimo 1 Saint, máximo 1 STL), cobrada apenas quando a recompensa de bloco chega a zero |

## Segurança

- Cada carteira tem um par de chaves **ECDSA (secp256k1)**; o endereço é o SHA-256 da chave pública comprimida.
- As chaves privadas ficam **criptografadas com Fernet** no banco de dados.
- As senhas são guardadas com **scrypt** e salt aleatório, nunca em texto puro.
- Toda transação precisa de assinatura válida do dono dos UTXOs gastos.
- Blocos e transações recebidos de outros nós são validados antes de serem aceitos: estrutura, proof, hash anterior, coinbase, assinaturas, UTXOs e taxas.

## Tecnologias

- **Python** e **Flask** (servidor, páginas e rotas)
- **PostgreSQL** com `psycopg` (blocos, UTXOs, carteiras, mempool e usuários)
- **cryptography** (ECDSA e Fernet)
- **HTML, CSS e JavaScript** nas páginas do site

## Arquitetura

```
Stella_STL/
├── main.py            # Ponto de entrada do servidor
├── config.py          # Parâmetros do protocolo
├── api/
│   ├── app.py         # Rotas do site e rotas de comunicação entre nós
│   ├── templates/     # Páginas HTML
│   └── static/        # CSS
├── core/              # Blockchain, blocos, mineração, transações, UTXO, carteira, criptografia
├── network/           # Propagação de blocos e transações, consenso entre nós
├── persistence/       # Acesso ao PostgreSQL e repositório de usuários
├── tests/             # Testes de validação, segurança e rede
└── documents/         # Whitepaper, relatório técnico, políticas e SIPs
```

### Rotas de comunicação entre nós

Além das páginas do site, o servidor expõe rotas JSON que os nós da rede usam para conversar entre si:

| Método | Rota | Função |
|---|---|---|
| `GET` | `/chain` | Entrega a cadeia completa |
| `GET` | `/blocks/<index>` | Entrega um bloco |
| `POST` | `/blocks/receive` | Recebe um bloco minerado por outro nó |
| `POST` | `/transactions/receive` | Recebe uma transação de outro nó |
| `POST` | `/nodes/register` | Registra outros nós da rede |
| `GET` | `/nodes/resolve` | Sincroniza adotando a cadeia válida com mais trabalho |

## Configuração do servidor

Para quem mantém a instalação, o servidor lê estas variáveis de ambiente:

| Variável | Para que serve |
|---|---|
| `DATABASE_URL` | String de conexão do PostgreSQL |
| `STELLA_SECRET_KEY` | Chave de sessão do Flask |
| `STELLA_WALLET_KEY` | Chave Fernet que protege as chaves privadas das carteiras |

A `STELLA_WALLET_KEY` não pode ser perdida: sem ela, as carteiras já criadas não podem ser descriptografadas. As tabelas são criadas automaticamente na primeira execução.

## Testes

A pasta [`tests/`](tests) reúne scripts de verificação que cobrem, entre outros pontos: gasto duplo, adulteração de blocos e transações, gasto sem chave privada, criação arbitrária de moedas, proof inválido, hash anterior inválido, escolha de cadeia, propagação e validação entre nós e controle de acesso.

## Documentação

- [`documents/Whitepaper.pdf`](documents/Whitepaper.pdf): visão geral e modelo do sistema
- [`documents/Technical_Report.pdf`](documents/Technical_Report.pdf): detalhes técnicos
- [`documents/policies/Economic_Policy.pdf`](documents/policies/Economic_Policy.pdf): política econômica
- [`documents/policies/Mining_Policy.pdf`](documents/policies/Mining_Policy.pdf): política de mineração
- [`documents/sips/`](documents/sips): modelo de propostas de melhoria (SIP)

## Autor

**Guilherme Domingues**
GitHub: [@guilhermedomingues-dev](https://github.com/guilhermedomingues-dev) · LinkedIn: [guilherme-ldomingues](https://www.linkedin.com/in/guilherme-ldomingues)
