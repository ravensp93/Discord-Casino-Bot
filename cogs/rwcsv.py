import os
import datetime

class rwcsv:

    @staticmethod
    def write_to_csv(msg : str):
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),"logs",f'transaction{datetime.datetime.now().strftime("%b%y")}.csv')
        
        if not os.path.exists(filepath):
            with open(filepath, 'w+'): pass
        
        with open(filepath,'a') as file:
            file.write(msg + "\n")

