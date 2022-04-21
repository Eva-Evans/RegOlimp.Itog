from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from models import School, Klass
from wtforms_sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    email = StringField("email: ", validators=[Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=5, max=50)])
    remember = BooleanField("Запомнить", default=False)
    submit =SubmitField("Войти")


class RegFormOrg(FlaskForm):
    fio = StringField("ФИО: ", validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField("email: ", validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message='Пароль должен состоять минимум из %(min)d символов')])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(message='*Required'), EqualTo('password', message='Пароли должны совпадать')])
    submit =SubmitField("Регистрация")


def school_query():
    return School.query


class RegFormTeach(FlaskForm):
    fio = StringField("ФИО: ", validators=[DataRequired(), Length(min=5, max=50)])
    school = QuerySelectField(query_factory=school_query, allow_blank=True, validators=[DataRequired(message='Поле школа обязательно для заполнения')])
    email = StringField("email: ", validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message='Пароль должен состоять минимум из %(min)d символов')])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(message='*Required'), EqualTo('password', message='Пароли должны совпадать')])
    submit =SubmitField("Регистрация")


def klass_query():
    return Klass.query


class RegFormStud(FlaskForm):
    fio = StringField("ФИО: ", validators=[DataRequired(), Length(min=5, max=50)])
    school = QuerySelectField(query_factory=school_query, allow_blank=True, validators=[DataRequired(message='Поле школа обязательно для заполнения')])
    klass = QuerySelectField(query_factory=klass_query, allow_blank=True, validators=[DataRequired(message='Поле класс обязательно для заполнения')])
    email = StringField("email: ", validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message='Пароль должен состоять минимум из %(min)d символов')])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(message='*Required'), EqualTo('password', message='Пароли должны совпадать')])
    submit =SubmitField("Регистрация")


class CreateOlimp(FlaskForm):
    title = StringField("Заголовок: ", validators=[DataRequired()])
    body = TextAreaField("Описание: ", validators=[DataRequired()])
    submit = SubmitField("Создать")


class EditOlimp(FlaskForm):
    title = StringField("Заголовок: ", validators=[DataRequired()])
    body = TextAreaField("Описание: ", validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class RecordStud(FlaskForm):
    submit = SubmitField("Записаться")


class FormGrade(FlaskForm):
    grade = StringField("Оценка", validators=[NumberRange(min=0, max=5)])
    submit = SubmitField("сохранить")
