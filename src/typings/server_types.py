from pydantic import BaseModel


class LoadQuestionsBody(BaseModel):
    questions_num: int


class FormattedQuestion(BaseModel):
    id: int
    answer: str
    question: str
    category_id: int
