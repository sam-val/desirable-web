from flask import Flask, request

import config
import core.core as c
import core.exceptions as core_ex

app = Flask(__name__)
app.secret_key = config.FLASK_SECRETKEY

@app.route("/")
def hello_world():
    return {"message": "hello"}, 404

@app.get("/question/<int:id>")
def get_question(id):
    try:
        message = c.get_question(id)
    except core_ex.NoQuestionFound:
        return {"message": f"Question {id} not found"}, 404

    return {
        "message": message
    }

@app.post("/question/<int:id>")
def question(id):
    # set session['p1'] for point of question 1, p2 for question 2, etc.
    # return {"message": "", "next_questions": next_url}
    request_data = request.get_json()
    answer = request_data.get("answer")
    if not answer:
        return {
            "message": "bad input: answer"
        }, 400
    message, next_question_id, err = c.answer_question(id, answer)
    if err:
        if err == core_ex.NoQuestionFound:
            return {"message": "No question found"}, 404
        return {"message": message}, 400

    next_question_url = ""
    if next_question_id:
        next_question_url = f"/question/{next_question_id}"

    return {
        "message": message,
        "next_question": next_question_url
    }, 200

@app.get("/calculate")
def calculate():
    # require the session having points for all questions
    # return {"message": }
    point = 0
    try:
        for k,v in c.questions_dic.items():
            point += c.points_dict[k]
    except KeyError as e:
        return {
            "message": f"question {k} has not been answered"
        }, 400

    message = c.get_result(point)
    return {
        "message": message,
        "point": point,
    }, 200

@app.delete("/reset")
def clear():
    c.points_dict.clear()
    return {}, 200