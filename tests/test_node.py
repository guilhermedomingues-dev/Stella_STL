from network.node import Node


node = Node()

node.register_node("http://127.0.0.1:5001")
node.register_node("http://127.0.0.1:5002")

assert "http://127.0.0.1:5001" in node.nodes
assert "http://127.0.0.1:5002" in node.nodes
assert len(node.nodes) == 2

print("Teste de registro de nós concluído com sucesso!")