from datetime import datetime

from flask import Flask, render_template, redirect, request, abort
from util import get_question_by_id, get_answers_by_question_id

app = Flask(__name__)
saved_data = {}
question = {}


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add-question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        question['note'] = request.form['note']

    return render_template("index.html"), redirect('/question/<question_id>')

@app.route('/question/<question_id>')
def display_question(question_id):
    question = get_question_by_id(question_id)
    if question == None:
        return abort(404)
    answers = get_answers_by_question_id(question_id)
    return render_template('question.html', question=question, answers=answers)

@app.template_filter('date')
def date(convert_time):
    time = datetime.fromtimestamp(int(convert_time))

    return time.strftime('%d.%m.%Y')



if __name__ == "__main__":
    app.run()
