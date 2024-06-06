#usado para criar o site

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

#render_tamplate para reconhecer todos os arquivos criados na pasta tampletes
# url for vai servir para usar a funcao na chamada para navegar entre pagina
#assim não teremos problemas futuros caso mude a rota

#criando o site e o banco de dados
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]  = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "29cecf8afd6176f06bb3f55472d490d2"
app.config["UPLOAD_FOLDER"] = "static/todas_fotos_posts"

database = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakepinterest import routes