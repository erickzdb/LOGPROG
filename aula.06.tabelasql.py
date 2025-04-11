import sqlite3
conn = sqlite3.connect("banco_usuarios.db") # cria arquivo se não existir

cursor = conn.cursor() # cria um cursor para executar comandos SQL
cursor.execute("""

CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    idade INTEGER

  )

  """)
nome = input("Digite seu nome: ")
idade = int(input("Digite sua idade: "))
cursor.execute("INSERT INTO usuarios (nome, idade) VALUES (?, ?)", (nome, idade))

conn.commit() # salva a transação no banco
ursor.execute("SELECT * FROM usuarios")

for linha in cursor.fetchall():

    print(linha)
  conn.close()//pra encerrar a conexão
