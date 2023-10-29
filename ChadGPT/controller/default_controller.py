import os
import sys
sys.path.append(os.path.dirname(__file__))

from controller import Controller

class DefaultController(Controller):
    ''' A custom controller that inherits from 
    Controller. Generates 3 answers to a query, 
    calculates the agreement within all the answer 
    pairs, and returns the mean agreement.
    '''
    def run(self, query):
        answers = self.get_answers(query, 3)
        agreements = self.get_agreement(answers)
        
        return sum(agreements)/len(agreements)