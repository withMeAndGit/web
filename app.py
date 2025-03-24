from flask import Flask, render_template, request, make_response, session
from flask_restful import Api
from flask_wtf import FlaskForm
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from werkzeug import Response
from werkzeug.utils import redirect

from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired

from data import db_session
from data.users import User
from data.jobs import Jobs

from jobs_api import blueprint
from users_resource import UserResource, UserListResource

import datetime

from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

api = Api(app)
api.add_resource(UserResource, '/api/v2/users/<int:user_id>')
api.add_resource(UserListResource, '/api/v2/users')

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    title = StringField('Job Title')
    team_leader = StringField('Team Leader id')
    work_size = StringField('Work Size')
    collaborators = StringField('Collaborators')
    finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def main() -> str:
    session = db_session.create_session()

    return render_template('index.html', jobs=session.query(Jobs).all())


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def jobs() -> str | Response:
    form = JobsForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.is_finished = form.finished.data
        current_user.jobs.append(job)
        sess.merge(current_user)
        sess.commit()
        return redirect('/')
    return render_template('jobs.html', form=form)


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
def login() -> str:
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/cookie')
def cookie() -> Response:
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


if __name__ == '__main__':
    db_session.global_init('database/mars_explorer.db')
    app.register_blueprint(blueprint)
    app.run(host='127.0.0.1', port=5555)
