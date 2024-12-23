# def add_shop(self, id_user, name_shop, text_msg):
#     con = sqlite3.connect(self.name_db)
#     cur = con.cursor()
#
#     tmp = '/'
#
#     shop = self.check_text(name_shop)
#     chek_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[5])
#
#     if len(name_shop) > 0:
#         if chek_shop[0] != None:
#             permission_user = self.create_tuple_db_posizione(id_user, config.name_posizione[7])[0].split('/')
#             nick_user = self.create_tuple_db_posizione(id_user, config.name_posizione[1])[0].split('/')
#             time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')
#             permission_user.append(tmp)
#             nick_user.append(tmp)
#             time_add.append(tmp)
#             count_shop = (list(chek_shop)[0]).split(';')
#             count_shop.append(shop)
#             cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?',('/'.join(permission_user)[:-1], id_user))
#             cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', (';'.join(time_add)[:-1], id_user))
#             cur.execute('UPDATE Users SET nick_user = ? WHERE id_user = ?', ('/'.join(nick_user)[:-1], id_user))
#             cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (';'.join(count_shop), id_user))
#             cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('add_token', id_user))
#
#         elif chek_shop[0] == None:
#             cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (shop, id_user))
#             cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('add_token', id_user))
#             cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', (tmp, id_user))
#             cur.execute('UPDATE Users SET nick_user = ? WHERE id_user = ?', (tmp, id_user))
#             cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', (';', id_user))
#
#         con.commit()
#         return text_msg[0]
#     return text_msg[1]
import config
import db

# import base64
# import json
#
#
# token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQxMTE4djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0Nzk3OTY0MSwiaWQiOiIwMTkzNGZkYy0wYjI5LTdmMjMtYTAyMS1kNzRlNWNlZWY2OTciLCJpaWQiOjIyMDAzMjkyLCJvaWQiOjEyMzg5OCwicyI6MTA3Mzc0OTc1OCwic2lkIjoiM2NjZmMyNTctZTVjMi00OThlLWFmYzAtYTUwZDE3YWQ4MzZlIiwidCI6ZmFsc2UsInVpZCI6MjIwMDMyOTJ9.2LVYoulqb5DW1fuh3SbBcTQJ28gLnTysoYFAXPaBUwp1nQs45QBJCn5kpSBFX6d_rp00T713-yMbL7E24JMd5A'
#
# header_b64, payload_b64, signature_b64 = token.split('.')
#
# def decode_base64url(data):
#     padded = data + '=' * (4 - len(data) % 4)
#     return base64.urlsafe_b64decode(padded).decode('utf-8')
#
# header = json.loads(decode_base64url(header_b64))
# payload = json.loads(decode_base64url(payload_b64))
#
# print("Header:", header)
# print(payload['sid'])

db_process = db.options_db()

check_name_company = db_process.create_tuple_db_posizione(956854913, config.name_posizione[5])
print(check_name_company[0].split('/'))

