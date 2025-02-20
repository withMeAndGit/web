from flask import Flask

app = Flask(__name__)


@app.route('/index')
def index() -> str:
    return '<p>И на Марсе будут яблони цвести!</p>'


@app.route('/promotion')
def promotion() -> str:
    return '''<p>Человечество вырастает из детства.<br><br>
Человечеству мала одна планета.<br><br>
Мы сделаем обитаемыми безжизненные пока планеты.<br><br>
И начнем с Марса!<br><br>
Присоединяйся!</p>'''


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
