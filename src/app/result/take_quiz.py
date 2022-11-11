import csv, json

import aioredis
from src.app.config import settings

from src.app.database import database
from src.app.models import questions, answers, result_quiz, rating, users_of_company

import datetime

from src.app.schemas import BaseQuestion, AnswerInput


class ResultCrud():

    async def one_user_of_company(self, company_id: int, user_id: int):
        redis = await aioredis.from_url(settings.REDIS_URL)
        find_keys = f'user:{user_id}_company:{company_id}'
        keys = await redis.keys(f'*{find_keys}*')
        f = open('export_company_user_results.csv', 'w', newline='')
        writer = csv.writer(f, delimiter=' ')
        for key in keys:
            answer = json.loads(await redis.get(key))
            filter = str(key).split("'")
            keyses = filter[1].split("_")
            writer.writerow([f'{keyses[0]}, {keyses[1]}, {keyses[2]}, result:{answer}'])
        f.close()

    async def all_users_results_csv(self, company_id: int):
        redis = await aioredis.from_url(settings.REDIS_URL)
        find_keys = f'company:{company_id}'
        keys = await redis.keys(f'*{find_keys}*')
        f = open('export_company_results.csv', 'w', newline='')
        writer = csv.writer(f, delimiter=' ')
        for key in keys:
            answer = json.loads(await redis.get(key))
            filter = str(key).split("'")
            keyses = filter[1].split("_")
            writer.writerow([f'{keyses[0]}, {keyses[1]}, {keyses[2]}, result:{answer}'])
        f.close()

    async def user_results_csv(self, user_id: int):
        redis = await aioredis.from_url(settings.REDIS_URL)
        find_keys = f'user:{user_id}'
        keys = await redis.keys(f'*{find_keys}*')
        f = open('export_user_results.csv', 'w', newline='')
        writer = csv.writer(f, delimiter=' ')
        for key in keys:
            answer = json.loads(await redis.get(key))
            filter = str(key).split("'")
            keyses = filter[1].split("_")
            writer.writerow([f'{keyses[0]}, {keyses[1]}, {keyses[2]}, result:{answer}'])
        f.close()

    async def get_questions(self, quiz_id: int) -> BaseQuestion:
        query = questions.select().where(quiz_id == questions.c.quiz_id)
        return await database.fetch_all(query=query)

    async def if_user_in_company(self, user_id: int, company_id: int):
        query = users_of_company.select().where(user_id == users_of_company.c.user_id, company_id == users_of_company.c.company_id)
        return await database.fetch_one(query=query)


    async def get_right_answers(self, quiz_id: int) -> AnswerInput:
        query = answers.select().join(questions).where(answers.c.question_id == questions.c.question_id,
                                                       questions.c.quiz_id == quiz_id)
        question = await database.fetch_all(query=query)
        return question

    async def put_user_result(self, score: str, result: float, quiz_id: int, user_id: int, company_id: int) -> float:
        query = result_quiz.insert().values(score=score, result=result, time=datetime.datetime.now(), quiz=quiz_id,
                                            company=company_id,
                                            user=user_id)
        await database.execute(query=query)
        query2 = result_quiz.select().where(user_id == result_quiz.c.user)
        main = await database.fetch_all(query2)
        list_of_score = [dict(aba) for aba in main]
        user_answer = 0
        all_question = 0
        for i in list_of_score:
            answer, question = i['score'].split('/')
            user_answer += int(answer)
            all_question += int(question)
        my_rating = round((user_answer / all_question), 2)

        query4 = rating.insert().values(rating=my_rating, user_id=user_id, time=datetime.datetime.now(),
                                        company_id=company_id, quiz_id=quiz_id)
        await database.execute(query=query4)

        return result


res_crud = ResultCrud()
