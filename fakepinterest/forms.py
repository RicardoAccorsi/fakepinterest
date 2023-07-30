# criar forms do site
'''
pip install flask-wtf email-validator
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Fazer Login")

    def validate_email(self, email):
        # pelo id usa .get(), para outros valores usa filter_by
        usuario = Usuario.query.filter_by(email=email.data).first()

        if not usuario:
            raise ValidationError("Usuário Inexistente. Crie uma conta para continuar")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirm_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha")])
    botao = SubmitField("Criar Conta")

    def validate_email(self, email):

        # pelo id usa .get(), para outros valores usa filter_by
        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError("E-mail já cadastrado. Faça login para continuar")


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirm = SubmitField("Postar")