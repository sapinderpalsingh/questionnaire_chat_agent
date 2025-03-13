import json
from models.question import Question
from models.user_state import UserState

from semantic_kernel.functions import kernel_function

class QuestionnairePlugin:
    
    def __init__(self, user_state: UserState):
        self.user_state = user_state

    @kernel_function(name="get_next_question", description="Get the next question for the user, if the function does not return any question then the questionnaire is completed.")
    def get_next_question(self) :
        question = self.user_state.get_next_question()
        if question is None:
            return None
        else:
            return json.dumps(question, default=lambda o: o.__dict__, indent=4)

    @kernel_function(description="This function is called to update the answer to a question")
    def update_answer(self, question_id: int, answer: str) :
        self.user_state.update_answer(question_id, answer)
