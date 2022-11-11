def make_rating(answer_input: list, right_answers: list):
    try:
        quiz_score = 0
        list_of_user_answer = [dict(user_answer) for user_answer in answer_input]
        for i in range(len(right_answers)):
            if list_of_user_answer[i]['answer'] == right_answers[i]['answer']:
                quiz_score += 1
        if quiz_score > 0:
            result = round((float(quiz_score) / len(right_answers)), 3)
        else:
            result = 0
        return quiz_score, right_answers, result
    except IndexError:
        return 'sqe'


def get_user_pass(get_users: list):
    dc = {}
    ls = []
    for i in get_users:
        dc[i['user_id']] = {'rating': i['rating'], 'time': i['time']}
    for key, value in dc.items():
        ls.append({'user_id': key, 'rating': value['rating'], 'time': value['time']})
    return ls


def get_quiz_last(get_users: list):
    dc = {}
    ls = []
    for i in get_users:
        dc[i['quiz_id']] = {'rating': i['rating'], 'time': i['time']}
    for key, value in dc.items():
        ls.append({'quiz_id': key, 'rating': value['rating'], 'time': value['time']})
    return ls
