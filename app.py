from flask import Flask, render_template

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


@app.route('/image_mars')
def image_mars() -> str:
    return render_template('image_mars.html')


@app.route('/promotion_image')
def promotion_image() -> str:
    return render_template('promotion_image.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
