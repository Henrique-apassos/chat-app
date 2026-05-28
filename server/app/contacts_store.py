"""
Armazenamento simples em memória para lista de contatos por usuário.
Usado nos testes para simular a feature de contatos
"""
user_contacts: dict[str, list[str]] = {}