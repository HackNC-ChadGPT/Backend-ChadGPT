import sys # TODO: Do packages properly
sys.path.append('./')

from controller import Controller

class DefaultController(Controller):
    def run(self, query):
        answers = self.get_answers(query, 3)
        agreements = self.get_agreement(answers)
        return sum(agreements)/len(agreements)