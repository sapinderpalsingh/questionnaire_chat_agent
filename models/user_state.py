import json
from typing import List, Optional
from models.question import Question


class UserState:
    def __init__(self, user_id:str, questions: List[Question]):
        self.user_id = user_id
        self.questions = questions
        self.is_completed = False
        self.next_question_id = questions[0].id if questions else None

   
    def update_answer(self, question_id: int, answer: str) :
        question = next(filter(lambda q: q.id == question_id, self.questions), None)
        if question:
            question.answer = answer
            self.next_question_id = next((option.next_question for option in question.options if option.label == answer), None)            
        return None

   
    def get_next_question(self) -> Optional[Question]:
        if self.next_question_id is not None:
            question = next(filter(lambda q: q.id == self.next_question_id, self.questions), None)
            return question
        else:
            self.is_completed = True
            return None            
    
    def to_json(self) -> str:
        data = {
            "user_id": self.user_id,
            "questions": [question.__dict__ for question in self.questions]
        }
        return json.dumps(data, indent=4)
    
    def save_state(self):
        contents = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        with open(f"{self.user_id}.json", 'w') as file:
            file.write(contents)