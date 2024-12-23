import sqlite3
import time
import base64
import json

import config
import api
import text

wb_api = api.work_api()

class options_db():
    def __init__(self):
        self.name_db = 'database.db'

    def add_user(self, id_user, owner_nick, status_bot, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        if self.check_user(id_user):
            return True, text_msg
        cur.execute(
            'REPLACE INTO Users (id_user, owner_nick, status_bot) VALUES (?, ?, ?)',
            (
                id_user,
                '@' + owner_nick,
                status_bot,
            )
        )
        con.commit()
        con.close()
        return False, text_msg

    def check_user(self, id_user):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        user_check = self.create_tuple_db_posizione(id_user, config.name_posizione[0])
        if (user_check != None) and (id_user in user_check):
            return True
        return False

    def check_status(self, id_user, checked_status):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        db_status = self.create_tuple_db_posizione(id_user, config.name_posizione[2])
        if (db_status != None) and (db_status[0] == checked_status):
            return True
        return False

    def check_text(self, checked_text):
        tmp = checked_text
        if ';' in tmp:
            tmp = checked_text.replace(';', '')
        return ''.join(tmp)

    import time
    def check_time_format(self, checked_time):
        try:
            time.strptime(checked_time, '%H:%M')
            return True
        except ValueError:
            return False

    def create_tuple_db_posizione(self, id_user, name_posizione):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        db_posizione = cur.execute(f'SELECT {name_posizione} FROM Users WHERE id_user = {id_user}').fetchone()
        con.commit()
        return db_posizione

    def change_status(self, id_user, new_status, text_msg, check):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        if check == 'st_b':
            if self.check_user(id_user):
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', (new_status, id_user))
                con.commit()
                return text_msg[0]

        elif check == 'st_sh':
            if self.check_user(id_user):
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', (config.statuses[4], id_user))
                cur.execute('UPDATE Users SET use_shop = ? WHERE id_user = ?', (new_status, id_user))
                con.commit()
                return text_msg[0]
        return text_msg[1]

    def add_shop(self, id_user, name_shop, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        tmp = '/'

        shop = self.check_text(name_shop)
        chek_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[5])

        if len(name_shop) > 0:
            if chek_shop[0] != None:
                permission_user = self.create_tuple_db_posizione(id_user, config.name_posizione[7])[0].split('/')
                # time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split('/')
                permission_user.append(tmp)
                # time_add.append(tmp)
                count_shop = (list(chek_shop)[0]).split('/')
                count_shop[-1] = shop
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', ('/'.join(permission_user)[:-1], id_user))
                # cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', (';'.join(time_add)[:-1], id_user))
                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(count_shop) + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('add_token', id_user))

            elif chek_shop[0] == None:
                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (shop + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('add_token', id_user))
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', (tmp, id_user))
                # cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', (';', id_user))

            con.commit()
            return text_msg[0]
        return text_msg[1]

    def change_name_shop(self, id_user, new_name):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        name = self.check_text(new_name)

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        tmp = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')
        tmp[id_use_shop] = name

        cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(tmp), id_user))
        cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
        con.commit()

        return 'Название магазина изменено'

    def decode_base64url(self, data):
        padded = data + '=' * (4 - len(data) % 4)
        return base64.urlsafe_b64decode(padded).decode('utf-8')

    def add_token(self, id_user, text_token, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        token = self.check_text(text_token)
        check_token = self.create_tuple_db_posizione(id_user, config.name_posizione[6])
        check_id_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[3])
        # check_pull_add = self.create_tuple_db_posizione(id_user, config.name_posizione[11])
        check_id_token = self.create_tuple_db_posizione(id_user, config.name_posizione[10])
        check_name_company = self.create_tuple_db_posizione(id_user, config.name_posizione[12])
        print(wb_api.check_token(text_token))
        if wb_api.check_token(text_token):
            header_b64, payload_b64, signature_b64 = token.split('.')
            payload = json.loads(self.decode_base64url(payload_b64))
            sid = payload['sid']
            tmp_set_company = wb_api.get_full_list_campaign(token)

            set_name_company = []
            set_id_company = []

            for num_company in range(len(tmp_set_company)):
                set_name_company.append(str(tmp_set_company[num_company][0]))
                set_id_company.append(str(tmp_set_company[num_company][1]))

            if check_name_company[0] != None:
                count_token = list(check_token)[0].split('/')
                count_id_shop = list(check_id_shop)[0].split('/')
                # count_pull_add = list(check_pull_add)[0].split(';')
                count_id_token = list(check_id_token)[0].split('/')
                count_name_company = list(check_name_company)[0].split('/')

                if str(sid) in count_id_token:
                    chek_name_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))
                    tmp_check_name_shop = (list(chek_name_shop)[0]).split('/')
                    del tmp_check_name_shop[-2]
                    cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', ('/'.join(tmp_check_name_shop) + '/', id_user))
                    cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                    con.commit()
                    return text_msg[1]

                count_token[-1] = token
                # count_pull_add.append('stop')
                count_id_token[-1] = str(sid)

                for name_company in set_name_company:
                    count_name_company[-1] += name_company

                for id_company in set_id_company:
                    count_id_shop[-1] += id_company

                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', ('/'.join(count_token) + '/', id_user))
                # cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', (';'.join(count_pull_add), id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', ('/'.join(count_name_company) + '/', id_user))
                cur.execute('UPDATE Users SET id_token = ? WHERE id_user = ?', ('/'.join(count_id_token) + '/', id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', ('/'.join(count_id_shop) + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))

            elif check_name_company[0] == None:
                tmp_set_company = wb_api.get_full_list_campaign(token)

                set_name_company = []
                set_id_company = []

                for num_company in range(len(tmp_set_company)):
                    set_name_company.append(str(tmp_set_company[num_company][0]))
                    set_id_company.append(str(tmp_set_company[num_company][1]))

                # cur.execute('UPDATE Users SET pull_add = ? WHERE id_user = ?', ('stop', id_user))
                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', (token + '/', id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', (';'.join(set_name_company) + '/', id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', (';'.join(set_id_company) + '/', id_user))
                cur.execute('UPDATE Users SET id_token = ? WHERE id_user = ?', (str(sid) + '/', id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))

            con.commit()
            return text_msg[0]
        return text_msg[1]

    def add_admin(self, id_user, id_admin, text_msg, nick_user):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        admin = self.check_text(id_admin)
        nick = self.check_text(nick_user)

        chek_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[7])
        check_nick = self.create_tuple_db_posizione(id_user, config.name_posizione[1])
        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split(';')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        if len(id_admin) > 0:
            if chek_admin[0] != None:
                count_admin = (list(chek_admin)[0]).split('/')
                count_nick = (list(check_nick)[0]).split('/')
                count_admin[id_use_shop] += f'{admin};'
                count_nick[id_use_shop] += f'@{nick};'
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', ('/'.join(count_admin), id_user))
                cur.execute('UPDATE Users SET nick_user = ? WHERE id_user = ?', ('/'.join(count_nick), id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))

            elif chek_admin[0] == None:
                cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', (admin, id_user))
                cur.execute('UPDATE Users SET nick_user = ? WHERE id_user = ?', (nick, id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))

            con.commit()
            return text_msg[0]
        return text_msg[1]

    def del_admin(self, id_user, text_msg, nick_user):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        nick = self.check_text(nick_user)

        chek_admin = self.create_tuple_db_posizione(id_user, config.name_posizione[7])
        check_nick = self.create_tuple_db_posizione(id_user, config.name_posizione[1])
        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split(';')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        id_del = (list(check_nick)[0]).split('/')[id_use_shop].split(';').index(nick_user)

        if chek_admin[0] != None:
            tmp_count_admin = (list(chek_admin)[0]).split('/')[id_use_shop].split(';')
            tmp_count_nick = (list(check_nick)[0]).split('/')[id_use_shop].split(';')
            del tmp_count_admin[id_del]
            del tmp_count_nick[id_del]

            count_admin = ';'.join(tmp_count_admin)
            count_nick = ';'.join(tmp_count_nick)

            ret_c_a = (list(chek_admin)[0]).split('/')
            ret_c_a[id_use_shop] = count_admin

            ret_c_n = (list(check_nick)[0]).split('/')
            ret_c_n[id_use_shop] = count_nick

            cur.execute('UPDATE Users SET permission_user = ? WHERE id_user = ?', ('/'.join(ret_c_a), id_user))
            cur.execute('UPDATE Users SET nick_user = ? WHERE id_user = ?', ('/'.join(ret_c_n), id_user))
            cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
            con.commit()
            return text_msg[0]

        elif chek_admin[0] == None:
            cur.execute('UPDATE Users SET nick_user = ? WHERE id_user = ?', (nick, id_user))
            cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
            con.commit()
            return text_msg[0]

        return text_msg[1]

    def add_time(self, id_user, checked_text, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        time_add = self.create_tuple_db_posizione(id_user, config.name_posizione[8])[0].split(';')

        chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split(';')
        use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

        id_use_shop = chek_shop.index(use_shop)

        tmp = self.check_text(checked_text)

        if self.check_time_format(tmp[:4]) and self.check_time_format(tmp[-5:]) and len(tmp) == 11:
            count_time = time_add
            count_time[id_use_shop] = tmp

            cur.execute('UPDATE Users SET time_add = ? WHERE id_user = ?', (';'.join(count_time), id_user))
            cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
            con.commit()
            return text_msg[0]
        con.commit()
        return text_msg[1]

    def del_shop(self, id_user, text_msg):
        con = sqlite3.connect(self.name_db)
        cur = con.cursor()

        chek_name_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))
        check_id_shop = self.create_tuple_db_posizione(id_user, config.name_posizione[3])
        check_token = self.create_tuple_db_posizione(id_user, config.name_posizione[6])
        check_id_token = self.create_tuple_db_posizione(id_user, config.name_posizione[10])
        check_name_company = self.create_tuple_db_posizione(id_user, config.name_posizione[12])

        if chek_name_shop != None:
            tmp_check_name_shop = (list(chek_name_shop)[0]).split('/')
            tmp_check_id_shop = (list(check_id_shop)[0]).split('/')
            tmp_check_token = (list(check_token)[0]).split('/')
            tmp_id_token = (list(check_id_token)[0]).split('/')
            tmp_name_company = (list(check_name_company)[0]).split('/')

            chek_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')[:-1]
            use_shop = list(self.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

            id_use_shop = chek_shop.index(use_shop)

            del tmp_check_name_shop[id_use_shop]
            del tmp_check_id_shop[id_use_shop]
            del tmp_check_id_shop[id_use_shop]
            del tmp_id_token[id_use_shop]
            del tmp_name_company[id_use_shop]

            count = 0
            all_check = tmp_check_name_shop + tmp_check_id_shop + tmp_check_id_shop + tmp_id_token + tmp_name_company

            for i in range(len(all_check)):
                if len(all_check[i]) > 0:
                    count += 1

            if count == 5:
                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (';'.join(tmp_check_name_shop), id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', (';'.join(tmp_check_id_shop), id_user))
                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', (';'.join(tmp_check_token), id_user))
                cur.execute('UPDATE Users SET id_token= ? WHERE id_user = ?', (';'.join(tmp_id_token), id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', (';'.join(tmp_name_company), id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                con.commit()
                return text_msg[0]

            elif count < 5:
                cur.execute('UPDATE Users SET name_shop = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET id_shop = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET token = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET id_token= ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET name_company = ? WHERE id_user = ?', (None, id_user))
                cur.execute('UPDATE Users SET status_bot = ? WHERE id_user = ?', ('waiting', id_user))
                con.commit()
                return text_msg[0]

        con.commit()
        return text_msg[1]

