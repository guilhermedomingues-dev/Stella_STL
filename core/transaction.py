"""
Funções relacionadas à criação de transações.

Modelo atual: sender -> recipient -> amount.
Será substituído pelo modelo de inputs/outputs (UTXO) na FASE 2.
"""

def new_transaction(self, sender, recipient, amount):
        """
        Cria uma nova transação para ser incluída no próximo bloco minerado
        :param sender: <str> Endereço de quem está enviando
        :param recipient: <str> Endereço de quem está recebendo
        :param amount: <int> Quantidade transferida
        :return: <int> Índice do bloco que receberá essa transação
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1