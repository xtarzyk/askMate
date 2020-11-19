from flask import Flask, render_template, redirect, request, abort
from util import get_question_by_id, get_answers_by_question_id, id_maker, get_all_questions
from datetime import datetime
from data_manager import read_csv_file, csv_columns, write_csv_file


app = Flask(__name__)
DATAFILE = './sample_data/movie_questions.csv'


@app.route("/list")
def list_questions():
    questions = get_all_questions()
    for question in questions:
        if question[0] != "id":
            question[1] = date(question[1])

    return render_template('list.html', questions=questions)


@app.route("/add-question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        question_dict = read_csv_file(DATAFILE)
        id_question = id_maker(question_dict)
        user_question = request.form['note']
        new = {}
        for key in csv_columns:
            new[key] = ''
        new["id"] = str(id_question)
        new['message'] = user_question
        write_csv_file(DATAFILE, [new], write_method="a")
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




if __name__ == "__main__":
    app.run()
