from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def start_page():
    db_sess = db_session.create_session()
    works = db_sess.query(Jobs)
    people = db_sess.query(User)
    return render_template('index.html', works=works, people=people)


def main():
    db_session.global_init("db/just_db.db")
    app.run()


if __name__ == '__main__':
    main()