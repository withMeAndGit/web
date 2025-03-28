from flask import Flask, render_template, request

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


@app.route('/choice/<planet_name>')
def choice(planet_name: str) -> str:
    return render_template('planet_choice.html', planet_name=planet_name)


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname: str, level: float, rating: float) -> str:
    data = {
        'nickname': nickname,
        'level': level,
        'rating': rating
    }

    return render_template('results.html', **data)


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo() -> str:
    if request.method == 'POST':
        file = request.files['file']
        with open('static/images/loaded_image.png', 'wb') as f:
            f.write(file.read())
    return render_template('load_photo.html')


@app.route('/carousel')
def carousel() -> str:
    return render_template('carousel.html')

@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection() -> str:
    if request.method == 'GET':
        return render_template('astronaut_selection.html')
    elif request.method == 'POST':
        print(f'''Имя: {request.form['surname']}
Фамилия: {request.form['name']}
email: {request.form['email']}
Профессия: {request.form['profession']}
Пол: {request.form['gender']}
Мотивация: {request.form['motivation']}
Готовность: {request.form['ready']}''')
        return '<p>Анкета отправлена</p>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
