# -- coding: utf-8 --
from flask import Flask, render_template, request, redirect, make_response
import json

app = Flask(__name__)

inputData = dict()
personData = dict()
resultData = dict()
answer = [
    ('male', 20),
    ('female', 19),
    ('male', 19),
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET'])
def game():
    nickname = request.args.get('nickname')
    gender = request.args.get('gender')

    if not nickname in personData.keys():
        inputData[nickname] = []
        personData[nickname] = 0
        resultData[nickname] = 0

    if not gender == None:
        age = int(request.args.get('age'))
        sequence = personData[nickname]
        genderResult = (gender == answer[sequence][0])
        ageResult = (age == answer[sequence][1] - 1) or (age == answer[sequence][1]) or (age == answer[sequence][1] + 1)

        if genderResult and ageResult:
            inputData[nickname].append('O')
            resultData[nickname] += 1
        else:
            inputData[nickname].append('X')

        personData[nickname] += 1

        if personData[nickname] > 2:
            return redirect('/result/' + nickname)

        return redirect('/game?nickname=' + nickname)

    src = "img/face" + str(personData[nickname] + 1) + ".jpeg"
    return render_template('game.html', image_file=src)

@app.route('/result/<nickname>')
def result(nickname):
    return render_template('result.html', cnt=resultData[nickname])

@app.route('/result')
def resultAll():
    json_data = json.dumps(resultData, ensure_ascii=False)
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/result_detail')
def result_detail():
    json_data = json.dumps(inputData, ensure_ascii=False)
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    return response

app.run(debug=True)