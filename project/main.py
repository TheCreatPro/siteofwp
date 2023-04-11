from flask import Flask, render_template, redirect, request, make_response, \
    session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from DataBase.forms.user import RegisterForm
from forms.login import LoginForm
from data import db_session
from data.users import User
# from data.jobs import Jobs
from data.news import News
from data import db_session, news_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    # тут можно написать рендер темпэйт и сделать красивую страницу
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/blogs.db")

    # db_sess = db_session.create_session()  # создаём сессию
    # news = db_sess.query(News).all()  # выводим новости
    # print(news)
    app.register_blueprint(news_api.blueprint)
    # user = User()
    # user.name = "Пользователь 1"
    # user.about = "биография пользователя 1"
    # user.email = "email@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()
    # # ^ создаём пользователя, но ещё не добавили его
    # db_sess.add(user)  # добавляем пользователя в базу
    # db_sess.commit()  # подтверждаем

    # user = User(name='sanya', about='was born? dont die', email='123@123.ru',
    #             hashed_password='123123')
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    # users = db_sess.query(User).all()  # получаем запрос из таблицы (класса) User
    # есть метод .filter(User.id > 1).filter(можно другое условие, и тд) все, у кого id больше одного
    # for user in users:
    #     print(user.name, user.email)

    app.run()


if __name__ == '__main__':
    main()
