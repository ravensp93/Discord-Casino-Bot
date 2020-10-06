import os
import datetime

class rwcsv:

    @staticmethod
    def write_to_raw_log(msg : str):
        raw_log_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),"logs",f'transaction_{datetime.datetime.now().strftime("%b%y")}.csv')
        
        if not os.path.exists(raw_log_filepath):
            with open(raw_log_filepath, 'w+') as file: 
                file.write(f'Action,From,Username,UserId,Amount,Game,Date\n')
                file.close()
        
        with open(raw_log_filepath,'a') as file:
            file.write(msg + "\n")
            file.close()

    @staticmethod            
    def write_to_activity_log(msg : str):
        activity_log_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),"logs",f'Activity_{datetime.datetime.now().strftime("%b%y")}.csv')

        if not os.path.exists(activity_log_filepath):
            with open(activity_log_filepath, 'w+') as file: 
                file.write(f'PLAYED BY, AMOUNT, SPECIAL_BET, USER_ID, GAME_TYPE, SCORE_A, SCORE_B, SPECIAL, RESULT, PROFIT\n')
                file.close()
        
        with open(activity_log_filepath,'a') as file:
            file.write(msg + "\n")
            file.close()