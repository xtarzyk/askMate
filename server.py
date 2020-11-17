from flask import Flask, render_template, redirect, request, abort
from util import get_question_by_id, get_answers_by_question_id
from datetime import datetime
import random
import string

app = Flask(__name__)
saved_data = {}
question_dict = {}


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add-question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id_question = id_maker(question_dict)
        user_question = request.form['note']
        new = {id_question: user_question}
        question_dict.update(new)
        return redirect('/question/%d' % id_question)
    return render_template('index.html')


@app.route('/question/<question_id>')
def display_question(question_id):
    question = get_question_by_id(question_id)
    if question is None:
        return abort(404)
    answers = get_answers_by_question_id(question_id)
    return render_template('question.html', question=question, answers=answers)


@app.template_filter('date')
def date(convert_time):
    time = datetime.fromtimestamp(int(convert_time))

    return time.strftime('%d.%m.%Y')


def id_maker():
    ide = []
    allowed_special_chars = "_", "+", "-", "!"

    for letter in range(0, 6):
        if letter < 4:
            ide.append(([random.choice(string.ascii_lowercase)]))
        else:
            ide.append(([random.choice(string.ascii_uppercase)]))
            ide.append(([random.choice(string.digits)]))
            ide.append([random.choice(allowed_special_chars)])
    random.shuffle(ide)
    all_ide = []
    for let in range(len(ide)):
        all_ide.append(ide[let][0])
    in_ide = ''.join(all_ide)

    return in_ide


if __name__ == "__main__":
    app.run()
