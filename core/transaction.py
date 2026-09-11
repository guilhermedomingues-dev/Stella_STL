"""
Funções relacionadas à criação de transações.

Modelo atual: sender -> recipient -> amount.
Será substituído pelo modelo de inputs/outputs (UTXO) na FASE 2.
"""
import hashlib
from core.utxo import valid_utxo, consume_utxo, create_utxo

# Cria um novo output da transação.
def create_output(owner, amount):
    # Retorna o proprietário e o valor do output.
    return {
        'owner': owner,
        'amount': amount,
    }

def new_transaction(inputs, outputs, available_utxos, spent_utxos):
    # Verifica cada UTXO utilizado como input.
    for utxo in inputs:
        # Impede o uso de um UTXO que não esteja disponível.
        if not valid_utxo(utxo, available_utxos):
            # Interrompe a criação da transação caso um UTXO seja inválido.
            return None

    # Soma o valor de todos os UTXOs utilizados como inputs.
    input_amount = sum(utxo['amount'] for utxo in inputs)

    # Soma o valor de todos os outputs solicitados.
    output_amount = sum(output['amount'] for output in outputs)

    # Impede que a transação gaste mais do que possui.
    if output_amount > input_amount:
        # Interrompe a criação da transação caso os valores sejam inválidos.
        return None

    # Calcula o valor que deverá retornar ao proprietário dos inputs.
    change = input_amount - output_amount

    # Cria um output de troco quando ainda existe valor restante.
    if change > 0:
        # Adiciona o troco ao primeiro proprietário dos inputs.
        outputs.append(create_output(inputs[0]['owner'], change))

    # Cria a estrutura inicial da transação.
    transaction = {
        'inputs': inputs,
        'outputs': outputs,
    }

    # Gera o identificador único da transação.
    transaction['transaction_id'] = hashlib.sha256(
        str(transaction).encode()
    ).hexdigest()

    # Consome cada UTXO utilizado pela transação.
    for utxo in inputs:
        # Remove o UTXO dos disponíveis.
        available_utxos.remove(utxo)
        # Registra o UTXO como gasto.
        consume_utxo(utxo, spent_utxos)

    # Cria um novo UTXO para cada output da transação.
    for index, output in enumerate(outputs):
        # Cria o UTXO associado ao output recém-criado.
        new_utxo = create_utxo(
            transaction['transaction_id'],
            index,
            output['owner'],
            output['amount']
        )
        # Adiciona o novo UTXO aos disponíveis.
        available_utxos.append(new_utxo)

    # Retorna a transação criada.
    return transaction