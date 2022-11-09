from src.app.database import database
from src.app.models import quizzes, questions
from src.app import schemas
import datetime

from src.app.schemas import BaseQuiz, BaseQuestion


class ResultCrud():

    async def get_questions(self, quiz_id) -> BaseQuestion:
        query = questions.select().where(quiz_id == questions.c.quiz_id)
        return await database.fetch_all(query=query)

    # async def create



res_crud = ResultCrud()
