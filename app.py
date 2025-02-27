from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main() -> str:
    return render_template('base.html')


@app.route('/index/<title>')
def index(title: str) -> str:
    return render_template('base.html',
                           title=title)


@app.route('/training/<prof>')
def training(prof: str) -> str:
    context = {
        'prof': prof
    }
    return render_template('training.html', **context)


@app.route('/list_prof/<list_>')
def list_prof(list_: str) -> str:
    context = {
        'list': list_,
        'profs': ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог',
                  'врач', 'инженер по терраформированию', 'климатолог',
                  'специалист по радиационной защите', 'астрогеолог',
                  'гляциолог', 'инженер жизнеобеспечения', 'метеоролог',
                  'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов']
    }

    return render_template('list_prof.html', **context)


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
