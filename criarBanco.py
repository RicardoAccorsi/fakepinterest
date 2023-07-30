from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto

# criar banco de dados do projeto
with app.app_context():
    database.create_all()