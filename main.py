from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/just_db.db")
    db_sess = db_session.create_session()
    j = Jobs()
    j.team_leader = 1
    j.job = 'deployment of residential modules 1 and 2'
    j.work_size = 15
    j.collaborators = '2, 3'
    j.is_finished = False
    db_sess.add(j)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()