from flask import Flask, render_template, redirect, request

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


if __name__ == "__main__":
    app.run()
