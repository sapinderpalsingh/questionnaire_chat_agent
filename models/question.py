from typing import List, Optional, Dict

class Option:
    def __init__(self, label: str, next_question: Optional[int]):
        self.label = label
        self.next_question = next_question

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            label=data['label'],
            next_question=data['next_question']
        )

class Question:
    def __init__(self, id: int, question: str, options: List[Option], answer: Optional[str] = None):
        self.id = id
        self.question = question
        self.options = options
        self.answer = answer

    @classmethod
    def from_dict(cls, data: dict):
        options = [Option.from_dict(option) for option in data['options']]
        return cls(
            id=data['id'],
            question=data['question'],
            options=options,
            answer=data.get('answer')
        )