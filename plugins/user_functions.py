import json
from models.user_state import UserState

def get_next_question(user_state: UserState): 
        question = user_state.get_next_question()
        if question is None:
            return None
        else:
            return json.dumps(question, default=lambda o: o.__dict__, indent=4)

def update_answer(user_state: UserState, question_id: int, answer: str) :
    user_state.update_answer(question_id, answer)