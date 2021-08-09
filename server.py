import os
import time
from flask import Flask, render_template, redirect, request, session, url_for
import data_manager
import sql_data_manager

app = Flask(__name__)
app.secret_key = "gaba"
DATAFILE = 'sample_data/question.csv'


def main():
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
    # comment_of_comment_list = sql_data_manager.list_of_comment_to_comment_by_comment_id(comment_list[0][4])
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
    sql_data_manager.delete_comment_by_question_id(question_id)
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


@app.route("/answer/<answer_id>/delete", methods=["POST"])
def delete_answer(answer_id):
    question_id = sql_data_manager.get_question_by_comment_id(answer_id)
    sql_data_manager.delete_comment_by_comment_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-up", methods=["GET", "POST"])
def vote_up(answer_id):
    question_id = sql_data_manager.get_question_by_comment_id(answer_id)
    sql_data_manager.add_vote(answer_id, question_id)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-down", methods=["GET", "POST"])
def vote_down(answer_id):
    question_id = sql_data_manager.get_question_by_comment_id(answer_id)
    sql_data_manager.delete_vote(answer_id, question_id)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/vote-up", methods=["GET", "POST"])
def vote_up_question(question_id):
    sql_data_manager.add_vote_question(question_id)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/vote-down", methods=["GET", "POST"])
def vote_down_question(question_id):
    sql_data_manager.delete_vote_question(question_id)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_comment(answer_id):
    answer_ide = answer_id
    question = sql_data_manager.get_all_of_question_by_comment_id(answer_ide)
    question_id = question[0]
    title = question[3]
    message = question[1]
    time_of_question = data_manager.convert_to_data(question[2])
    view = question[4]
    comment = sql_data_manager.get_comment_by_id(answer_ide)
    comment_message = comment[1]
    time_of_comment = data_manager.convert_to_data(comment [2])
    comment_vote = comment[3]

    if request.method == 'POST':
        answer_ide = answer_id
        comment_message = request.form['comment']
        vote = 0
        time_of_add_comment = time.time()
        comment_id = sql_data_manager.get_max_comment_of_comment_id()
        sql_data_manager.add_comment_to_comment(answer_ide, comment_id, comment_message, time_of_add_comment,vote)
        return redirect(f'/question/{question_id}')
    return render_template('add_comment_to_comment.html', title=title, message=message, time=time_of_question,
                           view=view, question_id=question_id, comment_message=comment_message,
                           comment_vote=comment_vote, time_of_comment=time_of_comment, answer_ide=answer_id)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == 'POST':
        user_name = request.form['email']
        password = request.form['password']
        date = time.time()
        sql_data_manager.add_user(user_name, password, date)
        return redirect("/")
    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user-name"]
        session["user"] = user
        return redirect(url_for('user'))
    return render_template('login.html')


@app.route("/user")
def user():
    if "user" in session:
        user_i = session["user"]
        return {user_i}
    else:
        return redirect("/login")


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
