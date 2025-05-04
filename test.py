import database


# database.dropTables()
# database.createTables()

database.addClient('uwu', 'owo', 100)


cursor = database.connection.cursor()
res = cursor.execute('SELECT * from client')
# res.fetchall()
print(res.fetchall())
