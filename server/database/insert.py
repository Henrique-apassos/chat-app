import sqlite3

conn = sqlite3.connect("chatapp.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO pessoa(USUARIO, NOME, EMAIL, TELEFONE, SENHA, SOBRENOME, BIOGRAFIA, CAMINHO_FOTO) VALUES
               ('joao', 'joao', 'j@cin.ufpe.br', '123', '123', 'feliz', 'feliz', '10'),
               ('maria', 'maria', 'm@cin.ufpe.br', '200', '123', 'alegre', 'alegre', '01');
""")

conn.commit()