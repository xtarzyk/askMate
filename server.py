from flask import Flask, render_template, redirect, request, abort
import data_manager
from util import id_maker
from datetime import datetime
from collections import OrderedDict
from operator import getitem
import sql_data_manager
import os
import time

app = Flask(__name__)
DATAFILE = 'sample_data/question.csv'


def main():
    # Load database.sql
    # sql_data_manager.load_database()
    # Start server
    app.run()


@app.route("/")
def main_page():
    list_of_questions = sql_data_manager.last_questions(5)
    list_of_questions_with_data = data_manager.convert_to_data(list_of_questions)
    return render_template('main_page.html', list_of_questions=list_of_questions_with_data)


@app.route("/add-question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id_question = sql_data_manager.get_max_id()
        title = request.form['title']
        message = request.form['message']
        view = 0
        vote = 0
        time_of_add_question = time.time()
        sql_data_manager.add_question(id_question, message, time_of_add_question, title, view, vote)
        return redirect(f'/question/{id_question}')
    return render_template('add_question.html')


@app.route('/question/<question_id>')
def display_question(question_id):
    question_ide = question_id
    question = sql_data_manager.get_question_by_id(question_ide)
    title = question[3]
    message = question[1]
    time_of_question = data_manager.convert_to_data(question[2])
    vote = question[5]
    view = sql_data_manager.increment_view(question_ide)
    comment_list = sql_data_manager.get_comment_by_question_id(question_ide)
    comment_list_with_data = data_manager.convert_to_data(comment_list)
    print(comment_list_with_data)
    return render_template('question_side.html', title=title, message=message, time=time_of_question, vote=vote,
                           view=view, question_ide=question_ide, comment_list=comment_list_with_data)


@app.route("/list")
def list_questions():
    list_of_questions = sql_data_manager.all_question()
    list_of_questions_with_data = data_manager.convert_to_data(list_of_questions)
    return render_template('list_question.html', list_of_questions=list_of_questions_with_data)


@app.route("/list-sorted", methods=['GET'])
def list_questions_sorted():
    list_of_questions = sql_data_manager.select_question_by(request.args['select'])
    list_of_questions_with_data = data_manager.convert_to_data(list_of_questions)
    return render_template('list_question.html', list_of_questions=list_of_questions_with_data)


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    sql_data_manager.delete_question_by_id(question_id)
    return redirect('/list')


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    if request.method == 'GET':
        question_ide = question_id
        question = sql_data_manager.get_question_by_id(question_ide)
        title = question[3]
        message = question[1]
        return render_template('edit_question.html', title=title, message=message, question_id=question_ide)
    else:
        sql_data_manager.update_question(question_id, request.form['title'], request.form['message'])
        return redirect('/list')


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_comment(question_id):
    question_ide = question_id
    question = sql_data_manager.get_question_by_id(question_id)
    title = question[3]
    message = question[1]
    time_of_question = data_manager.convert_to_data(question[2])
    view = question[4]

    if request.method == 'POST':
        comment_id = question_id
        comment_message = request.form['comment']
        vote = 0
        time_of_add_comment = time.time()
        answer_id = sql_data_manager.get_max_comment_id()
        sql_data_manager.add_comment(comment_id, comment_message, time_of_add_comment, vote, answer_id)
        return redirect(f'/question/{question_id}')
    return render_template('add_comment.html', title=title, message=message, time=time_of_question, view=view,
                           question_id=question_ide)


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    if request.method == 'GET':
        answer_ide = answer_id
        answer = sql_data_manager.get_comment_by_id(answer_ide)
        message = answer[1]
        return render_template('edit_comment.html', message=message, answer_id=answer_ide)
    else:
        sql_data_manager.update_comment(answer_id, request.form['message'])
        question_id = sql_data_manager.get_question_by_comment_id(answer_id)
        return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_plz(answer_id):
    pass


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
    main()
