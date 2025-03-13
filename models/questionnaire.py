import json
from typing import List, Optional
from models.question import Question


class Questionnaire:
    def __init__(self, questions: List[Question]):
        self.questions = questions

    @classmethod
    def from_json(cls, json_data: str):
        data = json.loads(json_data)
        questions = [Question.from_dict(item) for item in data]
        return cls(questions)