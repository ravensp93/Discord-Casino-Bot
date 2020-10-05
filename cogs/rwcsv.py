import os

class rwcsv:

    @staticmethod
    def write_to_csv(msg):
        dirname = os.path.dirname(os.path.dirname(__file__))
        
        print(dirname+"\\logs\\transaction.csv")