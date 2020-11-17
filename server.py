from flask import Flask, render_template, redirect, request
import random
import string

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
        id = id_maker()
        return redirect('/question/<question_id>')
    return render_template('index.html')


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
