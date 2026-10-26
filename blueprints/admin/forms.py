from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField, FloatField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, NumberRange, Optional
from .models import Role, Permission

class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")

class IntegrationForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    type = StringField("Тип", validators=[DataRequired()])
    config = TextAreaField("JSON конфигурации", validators=[DataRequired()])
    is_active = BooleanField("Активна")
    submit = SubmitField("Сохранить")

class RegistrationForm(FlaskForm):
    # Логин должен быть уникальным по модели User
    login = StringField(
        'Логин',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=6, max=50, message='Длина должна составлять от 6 до 50 символов')
        ]
    )
    
    full_name = StringField('Полное имя', validators=[Length(max=150)])

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Обязательное поле'),
            Email(message='Некорректный адрес электронной почты'),
            Length(max=150)
        ]
    )

    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=8, message='Минимальная длина пароля — 8 символов')
        ]
    )

    confirm_password = PasswordField(
        'Подтвердите пароль',
        validators=[
            DataRequired(message='Обязательное поле'),
            EqualTo('password', message='Пароли должны совпадать')
        ]
    )

    is_active = BooleanField('Активировать аккаунт сразу?', default=True)  # Флажок
    submit = SubmitField('Зарегистрироваться')


class ProductForm(FlaskForm):
    """Форма для создания или редактирования изделия."""
    name = StringField(
        label='Название',
        validators=[
            InputRequired(message='Введите название.'),
            Length(max=255, message='Максимальная длина названия — 255 символов.')
        ]
    )
    
    category = StringField(
        label='Категория',
        validators=[Length(max=100)]
    )  # Может быть пустым
    
    unit_price = FloatField(
        label='Цена за единицу',
        validators=[
            InputRequired(message='Укажите цену.'),
            NumberRange(min=0, message='Цена не может быть меньше нуля.')
        ],
        render_kw={'step': "0.01"}  # Шаг для инпутов типа number
    )
    
    submit = SubmitField('Сохранить')


class AssignPermissionForm(FlaskForm):
    r_role = SelectField("Роль", coerce=int, validators=[], choices=[])
    r_perm = SelectField("Право", coerce=int, validators=[], choices=[])
    submit = SubmitField("Назначить право")

    def populate_choices(self):
        self.r_role.choices = [(r.id, r.name) for r in Role.query.order_by(Role.name)]
        self.r_perm.choices = [(p.id, p.code + ": " + p.description[:30]) for p in Permission.query.order_by(Permission.code)]


class FilterLogs(FlaskForm):
    # Логин пользователя. Необязательное поле.
    login = StringField(
        label='Логин',
        name='login',
        validators=[Optional()]
    )
    
    # Дата начала периода. Тип datetime-local требует специального формата.
    date_from = DateTimeField(  # Назвал по-английски для единообразия
        label='С',
        name='from',
        format='%Y-%m-%dT%H:%M',  # Формат ISO8601 для datetime-local
        validators=[Optional()]
    )
    
    # Дата окончания периода.
    date_to = DateTimeField(
        label='По',
        name='to',
        format='%Y-%m-%dT%H:%M',
        validators=[Optional()]
    )
    
    submit = SubmitField('Показать')
