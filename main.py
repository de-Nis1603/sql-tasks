from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm, LoginForm
from forms.job import JobForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def start_page():
    db_sess = db_session.create_session()
    works = db_sess.query(Jobs)
    people = db_sess.query(User)
    return render_template('index.html', works=works, people=people)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html',
                                   form=form,
                                   message="Passwords are different")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html',
                                   form=form,
                                   message="User already exists")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('registration.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Invalid input",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            news = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            news = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if news:
            form.job.data = news.job
            form.work_size.data = news.work_size
            form.team_leader.data = news.team_leader
            form.collaborators.data = news.collaborators
            form.is_finished.data = news.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        print('validate')
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id,
                                             Jobs.user == current_user).first()
        if news:
            news.team_leader = form.team_leader.data
            news.job = form.job.data
            news.work_size = form.work_size.data
            news.is_finished = form.is_finished.data
            news.collaborators = form.collaborators.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        news = db_sess.query(Jobs).filter(Jobs.id == id).first()
    else:
        news = db_sess.query(Jobs).filter(Jobs.id == id,
                                             Jobs.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.finish_date = form.finish_date.data
        job.is_finished = form.is_finished.data
        current_user.news.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)


def main():
    db_session.global_init("db/just_db.db")
    app.run()


if __name__ == '__main__':
    main()