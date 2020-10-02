import sqlite3
import time

class dbconn:

    def __init__(self):
        self.sqliteConnection = None
        self.cursor = None
        self.tablename = "tbl_users"

    def db_exec(self, mode, db_query):
        try:
            self.cursor.execute(db_query)
            if mode == 1:
                results = self.cursor.fetchall()
                return results
            elif mode == 2:
                self.sqliteConnection.commit()
                return "Execution Completed"
        except sqlite3.Error as e:
            print(e)
            return "Error"

    def get_stats(self, userId):
        stats_dict = { "tb" : 0, "tbw" : 0, "tbm" : 0, "roles" : "" }
        db_query = f'SELECT total_bet,total_bet_week,total_bet_month,roles FROM {self.tablename} WHERE user_id=\"{userId}\"'
        try:
            self.cursor.execute(db_query)
            results =  self.cursor.fetchall()
            stats_dict["tb"] = results[0][0]
            stats_dict["tbw"] = results[0][1]
            stats_dict["tbm"] = results[0][2]
            stats_dict["roles"] = results[0][3]
            return stats_dict
        except sqlite3.Error as e:
            print("Error in getting stats")

    def update_role(self, userId, role : str):
        db_query = f'UPDATE {self.tablename} SET roles = \"{role}\" WHERE user_id=\"{userId}\"'
        try:
            self.cursor.execute(db_query)
            self.sqliteConnection.commit()
        except sqlite3.Error as e:
            print("Error in updating role")

    def register_user(self, user, userId):
        db_query = f'INSERT INTO {self.tablename} (user, user_id, joined_date, last_active_date, roles) values (\"{user}\", \"{userId}\", \"{time.ctime()}\", \"{time.ctime()}\", "Bronze")'
        try:
            self.cursor.execute(db_query)
            print("User: " + user + " registered in database")
            self.sqliteConnection.commit()
            return "Bronze"
        except sqlite3.IntegrityError as e:
            db_query = f'UPDATE {self.tablename} SET user = \'{user}\' WHERE user_id=\'{userId}\''
            self.cursor.execute(db_query)
            self.sqliteConnection.commit()
            db_query = f'SELECT roles from {self.tablename} WHERE user_id = \'{userId}\''
            self.cursor.execute(db_query)
            results = self.cursor.fetchall()[0][0]
            print(f'Updated {userId}\'s username to {user}')
            return results


    def update_bal(self, caller, userId, amount):
        try:
            db_query = f'UPDATE {self.tablename} SET balance = {amount} WHERE user_id=\"{userId}\"'
            self.cursor.execute(db_query)
            self.sqliteConnection.commit()
            print(f'{caller} Updated {userId} balance to {amount} @@@@ {time.ctime()}')
        except sqlite3.Error as e:
            print(e)

    def withdraw_bal(self, userId, amount):
        #check user balance
        final_balance = self.get_current_balance(userId) - amount
        if(final_balance < 0):
            return False
        else:
            try:
                db_query = f'UPDATE {self.tablename} SET balance = {final_balance} WHERE user_id=\"{userId}\"'
                self.cursor.execute(db_query)
                self.sqliteConnection.commit()
                print(f'Withdrawn {amount} from {userId}\'s Account @@@@ {time.ctime()}')
            except sqlite3.Error as e:
                print(e)
        return True

    def deposit_bal(self, userId, amount):
        final_balance = self.get_current_balance(userId) + amount
        try:
            db_query = f'UPDATE {self.tablename} SET balance = {final_balance} WHERE user_id=\"{userId}\"'
            self.cursor.execute(db_query)
            self.sqliteConnection.commit()
            print(f'Deposited {amount} into {userId}\'s Account @@@@ {time.ctime()}')
        except sqlite3.Error as e:
            print(e)

    def update_lad_bet(self, userId, amount):
        try:
            db_query = f'UPDATE {self.tablename} SET last_active_date = \"{time.ctime()}\",total_bet = total_bet + {amount},total_bet_week = total_bet_week + {amount},total_bet_month = total_bet_month + {amount} WHERE user_id=\"{userId}\"'
            self.cursor.execute(db_query)
            self.sqliteConnection.commit()
        except sqlite3.Error as e:
            print(e)

    def get_current_balance(self, userId):
        db_query = f'SELECT balance FROM {self.tablename} WHERE user_id=\"{userId}\"'
        self.cursor.execute(db_query)
        balance = self.cursor.fetchall()[0][0]
        return int(balance)

    def get_username_from_ID(self,userId):
        db_query = f'SELECT user FROM {self.tablename} WHERE user_id=\"{userId}\"'
        self.cursor.execute(db_query)
        user = self.cursor.fetchall()[0][0]
        return user

    def dbconn_open(self):
        try:
            self.sqliteConnection = sqlite3.connect('c:/Users/raven/OneDrive/Desktop/Discord/Code/db/bot.db')
            self.cursor = self.sqliteConnection.cursor()
            # print("Database created and Successfully Connected to SQLite")
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def dbconn_close(self):
        self.cursor.close()
        self.sqliteConnection.close()
        # print("The SQLite connection is closed")
