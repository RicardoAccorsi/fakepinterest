from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormCriarConta, FormLogin, FormFoto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])  # atribui funcionalidade à função abaixo dele (decorator)
def homepage():
    formlogin = FormLogin()

    if formlogin.validate_on_submit(): # se formulario estiver valido
        # pelo id usa .get(), para outros valores usa filter_by
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", usuario=usuario.id))

    return render_template("homepage.html", form=formlogin)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():  # se usuario clicou no botao e as informações foram preenchidas corretamente
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, email=formcriarconta.email.data, senha=senha)

        # comitar
        database.session.add(usuario)
        database.session.commit()

        # logar
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("criarconta.html", form=formcriarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])  # atribui funcionalidade à função abaixo dele (decorator)
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(int(id_usuario))

    if int(id_usuario) == int(current_user.id):

        form_foto = FormFoto()

        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)

            # salvar arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # registrar nome no banco de dados
            foto = Foto(img=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepge"))


@app.route("/feed")
@login_required
def feed():

    # ordenar todas as fotos da mais recente para a menos (limite 10 fotos)
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:10]
    return render_template("feed.html", fotos=fotos)
