from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from werkzeug import Response
from werkzeug.utils import redirect

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class LoginForm(FlaskForm):
    astronaut_id = StringField('ID астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])

    capitan_id = StringField('ID капитана', validators=[DataRequired()])
    capitan_password = PasswordField('Пароль капитана', validators=[DataRequired()])

    access = SubmitField('Доступ')


@app.route('/')
def main() -> str:
    return render_template('base.html')


@app.route('/index/<title>')
def index(title: str) -> str:
    return render_template('base.html',
                           title=title)


@app.route('/training/<prof>')
def training(prof: str) -> str:
    return render_template('training.html', prof=prof)


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


@app.route('/astronaut_selection')
def astronaut_selection() -> str:
    return render_template('astronaut_selection.html')


@app.route('/answer', methods=['POST'])
@app.route('/auto_answer', methods=['POST'])
def answer() -> str:
    context = {
        'title': 'Анкета',
        'surname': request.form['surname'],
        'name': request.form['name'],
        'education': request.form['education'],
        'profession': ', '.join(request.form.getlist('profession')),
        'gender': request.form['gender'],
        'motivation': request.form['motivation'],
        'ready': bool(request.form.get('ready'))
    }

    return render_template('auto_answer.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if form.validate_on_submit():
        return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
