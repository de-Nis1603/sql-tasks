from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms import BooleanField, FloatField, DateField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = StringField('Leader', validators=[DataRequired()])
    job = StringField('Goal', validators=[DataRequired()])
    work_size = FloatField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    start_date = DateField('Start date')
    finish_date = DateField('Finish date')
    is_finished = BooleanField('The job is finished')
    submit = SubmitField('Submit')