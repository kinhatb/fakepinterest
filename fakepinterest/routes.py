#criar as rotas do site (os links)

from flask import render_template , url_for , redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user , logout_user,current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename

#rota do que vem depois do seu dominio - rota principal
@app.route('/', methods = ["GET","POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario = usuario.id))
            
    return render_template('homepage.html', form = formlogin)


@app.route('/criarconta',  methods = ["GET","POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username = formcriarconta.username.data , senha = senha , email = formcriarconta.email.data)
        #abrindo a conexao e adicionando as informações do usuario
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template('criarconta.html', form = formcriarconta)

#utilizando o <> para transformar em dinamico - transformar em uma variavel
#utilizando {{}} na pagina de perfil para exportar a informaçao 
# adicionar login_required para evitar que outras pessoas acesse a essa pagina
@app.route('/perfil/<id_usuario>',  methods = ["GET","POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        formfoto = FormFoto()
        #enviando o arquivo
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            #salvar arquivo na pasta
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],nome_seguro)
            arquivo.save(caminho)
            #registar arquivo no banco
            foto = Foto(imagem= nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html',usuario = current_user , form = formfoto)
    else:    
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html',usuario = usuario, form=None)

#current_user é o usuario logado
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

#@login_required pagina que so pode ver se estiver logado
@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao).all()
    return render_template("feed.html", fotos=fotos)