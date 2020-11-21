from flask import Flask, render_template, redirect, request, abort
from util import get_question_by_id, get_answers_by_question_id, id_maker
from datetime import datetime
from data_manager import read_csv_file, csv_columns, write_csv_file
from collections import OrderedDict
from operator import getitem
import os

app = Flask(__name__)
DATAFILE = 'sample_data/question.csv'


@app.route("/")
def hello():
    return "Hello World!"


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


@app.route("/list")
def list_questions():
    questions = read_csv_file(DATAFILE)
    questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "view_number")))

    sort_by = request.args.get("sort_by")
    order = request.args.get("order")
    if order == "asc":
        if sort_by == "title":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "title")))
        if sort_by == "submission_time":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "submission_time")))
        if sort_by == "message":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "message")))
        if sort_by == "view_number":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "view_number")))
        if sort_by == "vote_number":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "vote_number")))
    if order == "desc":
        if sort_by == "title":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "title"), reverse=True))
        if sort_by == "submission_time":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "submission_time"), reverse=True))
        if sort_by == "message":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "message"), reverse=True))
        if sort_by == "view_number":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "view_number"), reverse=True))
        if sort_by == "vote_number":
            questions = OrderedDict(sorted(questions.items(), key=lambda x: getitem(x[1], "vote_number"), reverse=True))




    for question in questions:
        questions[question]["submission_time"] = date(questions[question]["submission_time"])
    return render_template('list.html', questions=questions)


app.config["IMAGE_UPLOADS"] = "E:/Dev/WEB/ask-mate-1-python-Fraktalia/static/image/uploads"


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if request.files:
            image = request.files["image"]

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print("Image saved")

            return redirect(request.url)

    return render_template('upload_image.html')


if __name__ == "__main__":
    app.run()
