import os

class rwcsv:

    @staticmethod
    def write_to_csv(msg):
        dirname = os.path.dirname(os.path.dirname(__file__))
        
        print(os.path.join(os.path.dirname(os.path.dirname(__file__)),"logs","transaction.csv"))