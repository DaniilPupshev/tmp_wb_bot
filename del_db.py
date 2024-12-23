import sqlite3
import uuid

#тут просто сбрасываю флаг в бд
connection = sqlite3.connect('database.db')
cursor = connection.cursor()
# cursor.execute('DELETE FROM Users WHERE status_bot = ?', ('waiting',))
# cursor.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', 956854913))


#удаление данных
cursor.execute('DELETE FROM Users WHERE status_bot = ?', ('add_token',))

connection.commit()
connection.close()

