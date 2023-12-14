import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash


print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

# criando tabelas
TABLES = {}
TABLES['Games'] = ('''
      CREATE TABLE `games` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `category` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `name` varchar(20) NOT NULL,
      `email` varchar(100) NOT NULL,
      `password` varchar(100) NOT NULL,
      PRIMARY KEY (`email`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
      tabela_sql = TABLES[table_name]
      try:
            print('Criando tabela {}:'.format(table_name), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo users
user_sql = 'INSERT INTO users (name, email, password) VALUES (%s, %s, %s)'
users = [
      ("Bruno Divino", "bruno@gmail.com", generate_password_hash("alohomora").decode('utf-8')),
      ("Camila Ferreira", "mila@gmail.com", generate_password_hash("paozinho").decode('utf-8')),
      ("Guilherme Louro", "cake@gmail.com", generate_password_hash("python_eh_vida").decode('utf-8'))
]
cursor.executemany(user_sql, users)

cursor.execute('select * from jogoteca.users')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
games_sql = 'INSERT INTO games (name, category, console) VALUES (%s, %s, %s)'
games = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Luta', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(games_sql, games)

cursor.execute('select * from jogoteca.games')
print(' -------------  Jogos:  -------------')
for games in cursor.fetchall():
    print(games[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()