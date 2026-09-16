from network.node import Node

node_1 = Node()
node_2 = Node()

node_1.register_node('http://localhost:5001')

assert 'http://localhost:5001' in node_1.nodes

print("Teste de comunicação entre nós concluído com sucesso!")