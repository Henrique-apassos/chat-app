import sqlite3

def create_tables(conn):
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pessoa (
    USUARIO TEXT PRIMARY KEY,
    NOME TEXT NOT NULL,
    EMAIL TEXT UNIQUE NOT NULL,
    TELEFONE TEXT UNIQUE NOT NULL,
    SENHA TEXT NOT NULL,
    SOBRENOME TEXT,
    BIOGRAFIA TEXT,
    CAMINHO_FOTO TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grupo (
    ID_GRUPO INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME_GRUPO TEXT NOT NULL,
    DATA_CRIACAO TEXT NOT NULL,
    DESCRICAO TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS esta_em (
    USUARIO TEXT,
    ID_GRUPO INTEGER,
    PAPEL TEXT,
    DATA_ENTRADA TEXT,
    PRIMARY KEY (USUARIO, ID_GRUPO),
    FOREIGN KEY (USUARIO) REFERENCES pessoa (USUARIO),
    FOREIGN KEY (ID_GRUPO) REFERENCES grupo (ID_GRUPO)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagem (
    ID_MENSAGEM INTEGER PRIMARY KEY AUTOINCREMENT,
    TIMESTAMP TEXT NOT NULL,
    TEXTO TEXT NOT NULL,
    STATUS_ENVIO TEXT,
    USUARIO TEXT,
    ID_GRUPO INTEGER,
    FOREIGN KEY (USUARIO) REFERENCES pessoa (USUARIO),
    FOREIGN KEY (ID_GRUPO) REFERENCES grupo (ID_GRUPO)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recebe (
    USUARIO TEXT,
    ID_MENSAGEM INTEGER,
    LIDA INTEGER,
    PRIMARY KEY (USUARIO, ID_MENSAGEM),
    FOREIGN KEY (USUARIO) REFERENCES pessoa (USUARIO),
    FOREIGN KEY (ID_MENSAGEM) REFERENCES mensagem (ID_MENSAGEM)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documento (
    ID_DOCUMENTO INTEGER PRIMARY KEY AUTOINCREMENT,
    CAMINHO TEXT NOT NULL,
    TIPO TEXT,
    TAMANHO TEXT,
    ID_MENSAGEM INTEGER,
    FOREIGN KEY (ID_MENSAGEM) REFERENCES mensagem (ID_MENSAGEM)
    );
    """)

    conn.commit()

conn = sqlite3.connect("chatapp.db")
create_tables(conn)

print("Tabelas criadas com sucesso!")
conn.close()