import os
import sys
sys.path.append(os.path.dirname(__file__))

from controller import Controller

class DefaultController(Controller):
    def run(self, query):
        answers = self.get_answers(query, 2)
        agreements = self.get_agreement(answers)
        print(f'\n=========\nAnswers \n{answers}\n{agreements}\n')
        return sum(agreements)/len(agreements)
