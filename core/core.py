from typing import Tuple

import core.exceptions as ex

questions_dic = {
    1: "How old are you (please enter a number): ",
    2: "Next question, how much money do you really make a year in US Dollars: ",
    3: "Last question, how do you rate yourself from 1 to 10 in terms of perfection: ",
}

result_dic = {
   4: "You're not at all desirable, Perhaps try again",
   5: "You're almost desirable",
   6: "You're desirable. Congrats!"
}

points_dict = {} 

def get_result(point):
    for k,v in result_dic.items():
        if point <= k:
            return v

    # more than max, return the max point's message
    return v

def get_question(id):
    if id not in questions_dic:
        raise ex.NoQuestionFound

    return questions_dic[id]

def question_1(answer) -> Tuple[str, int]:
    answer = float(answer)
    if answer <= 0:
        raise ValueError
    elif answer >= 120:
        raise ex.TooOld
    elif 0 < answer < 18:
        return "You're too young, didn't you know this game is 18+ ?", 0 
    elif 18 <= answer <= 30:
        return "Good! You are young, must feel great!", 2
    elif 30 < answer < 50:
        return "Your skin is having wrinkles.", -1
    else:
        return "I'm sorry...", -1


def question_2(answer):
    answer2 = float(answer)
    if answer2 < 0:
        raise ValueError
    elif answer2 >= 10_000_000:
        raise ex.TooMuchMoney
    elif 0 <= answer2 < 3000:
        return "I know, I know, I cry sometimes too...", -2
    elif 3000 <= answer2 <= 10000:
        return "Well at least you make more than the homeless...", -1
    elif 10000 < answer2 < 35000:
        return "You are categorized within the LOWER CLASS", -1 
    elif 35000 <= answer2 < 75000:
        return "You are categorized within the MIDDLE CLASS", 0 
    elif 75000 <= answer2 < 300000:
        return "You are categorized within the UPPER CLASS", 1 
    elif 300000 <= answer2 < 500000:
        return "You're doing real well, care to give me some money?", 2 
    elif 500000 <= answer2 < 1000000:
        return "You rich bastard!", 3 
    elif answer2 >= 1000000:
        return "I can see money coming out of your a**hole from here.", 4 

def question_3(answer):
    answer3 = float(answer)
    if answer3 < 1:
        raise ValueError
    elif answer3 == 1:
        return "Who would rate themselves the lowest number?, You have bigger issues...", 0
    elif 1 < answer3 < 4:
        return "That's okay, a lot people don't think they are attractive", 2
    elif 4 <= answer3 <= 7:
        return "You are pretty much average", 1 
    elif 8 <= answer3 <= 10:
        return "If you think so...", -1
    elif answer3 > 10:
        return "If you're so perfect then I'm sure you won't mind never winning this game---", -10


def answer_question(id, answer) -> Tuple[str, int, Exception]:
    if id not in questions_dic:
        return f"No Question {id} Found", None, ex.NoQuestionFound 

    if id in points_dict:
        return f"Question already answered", None, ex.AlreadyAnswered

    dispatch_dict = {
        1: question_1,
        2: question_2,
        3: question_3,
    }

    try:
        message, points = dispatch_dict[id](answer)
    except ValueError:
        return "Please enter a valid number", None, ValueError
    except ex.TooOld:
        return "What are you? A vampire? Enter your real age please", None, ex.TooOld
    except ex.TooMuchMoney:
        return "Please, Enter the amount you make not the amount you want to make", None, ex.TooMuchMoney

    points_dict[id] = points
    if id == len(questions_dic):
        next_id = None
    else:
        next_id = id + 1
    return message, next_id, None
