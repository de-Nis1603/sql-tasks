from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/just_db.db")
    db_sess = db_session.create_session()
    surnames = ['Scott', "Steymoore", "Ivanov", 'Watson']
    names = ['Ridley', "Richard", 'Semen', 'John']
    ages = [21, 53, 32, 37]
    positions = ['captain', 'vice-captain', 'commander', 'commander']
    specialities = ['research manager', 'ecologist', 'communicator', 'doctor']
    addresses = ['module_1', 'module_4', 'module_2', 'module_3']
    emails = ['scott_chief@mars.org', 'steymoore@mars.org', 'ivanov-translator@mars.org', 'dr_watson@mars.org']
    for i in range(len(names)):
        user = User()
        user.surname = surnames[i]
        user.name = names[i]
        user.age = ages[i]
        user.position = positions[i]
        user.speciality = specialities[i]
        user.address = addresses[i]
        user.email = emails[i]
        db_sess.add(user)
        db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()