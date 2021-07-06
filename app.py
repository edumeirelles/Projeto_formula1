from logging import error
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import validate_arguments

app = Flask(__name__)

user = 'nribskms'
password = '5vzaXTm4whpCpVMys8SDYWwzBJS_n3Fr'
host = 'tuffi.db.elephantsql.com'
database = 'nribskms'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "chupa hamilton"

db = SQLAlchemy(app)

class Formula1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    vitorias = db.Column(db.Integer, nullable=False)
    poles = db.Column(db.Integer, nullable=False)
    gp_disputados = db.Column(db.Integer, nullable=False)
    pontos = db.Column(db.Float, nullable=False)
    podiums = db.Column(db.Integer, nullable=False)
    campeonatos = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String(4000), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)


    def __init__(self, nome, vitorias, poles, gp_disputados, pontos, podiums, campeonatos, bio, imagem_url):
        self.nome = nome
        self.vitorias = vitorias
        self.poles = poles
        self.gp_disputados = gp_disputados
        self.pontos = pontos
        self.podiums = podiums
        self.campeonatos = campeonatos
        self.bio = bio
        self.imagem_url = imagem_url
    
    @staticmethod
    def read_all():
        return Formula1.query.order_by(Formula1.vitorias.desc()).all()

    @staticmethod
    def read_single(registro_id):
        return Formula1.query.get(registro_id)
    
    

    def save(self):
        
        db.session.add(self)
        db.session.commit()
        
        
    
    def update(self, novo_nome, novo_vitorias, novo_poles, novo_gp_disputados, novo_pontos, novo_podiums, novo_campeonatos, novo_bio, novo_imagem_url):
        self.nome = novo_nome
        self.vitorias = novo_vitorias
        self.poles = novo_poles
        self.gp_disputados = novo_gp_disputados
        self.pontos = novo_pontos
        self.podiums = novo_podiums
        self.campeonatos = novo_campeonatos
        self.bio = novo_bio
        self.imagem_url = novo_imagem_url

        self.save()

    def delete(self):
        
        db.session.delete(self)
        db.session.commit()

            
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read')
def read_all():
    registros = Formula1.read_all()
    return render_template('read_all.html', registros=registros)


@app.route("/read/<registro_id>")
def read_id(registro_id):
    registro = Formula1.read_single(registro_id)
    print(registro)
    return render_template('read_single.html', registro=registro)

@app.route('/create', methods=('GET','POST'))
def create():
    id_atribuido = None
    erro = "Preencha todos os campos"
    if request.method == 'POST':
        form = request.form
        if not form['nome'] or not form['vitorias'] or not form['poles'] or not form['gp_disputados'] or not form['pontos'] or not form['podiums'] or not form['campeonatos'] or not form['bio'] or not form['imagem_url']:
            
            return render_template('erro.html', id_atribuido=id_atribuido, erro=erro)

        registro = Formula1(form['nome'], form['vitorias'], form['poles'], form['gp_disputados'], form['pontos'], form['podiums'], form['campeonatos'], form['bio'], form['imagem_url'])
        
        registro.save()

        id_atribuido = registro.id
    return render_template('create.html', id_atribuido=id_atribuido)

@app.route('/update/<registro_id>', methods=('GET', 'POST'))
def update(registro_id):

    sucesso = False
    erro = "Preencha todos os campos"
    registro = Formula1.read_single(registro_id)

    if request.method == 'POST':
        form = request.form
        if not form['nome'] or not form['vitorias'] or not form['poles'] or not form['gp_disputados'] or not form['pontos'] or not form['podiums'] or not form['campeonatos'] or not form['bio'] or not form['imagem_url']:

            return render_template('erro.html', registro=registro, erro=erro)

        registro.update(form['nome'], form['vitorias'], form['poles'], form['gp_disputados'], form['pontos'], form['podiums'], form['campeonatos'], form['bio'], form['imagem_url'])

        sucesso = True
    
    return render_template('update.html', registro=registro, sucesso=sucesso)

@app.route('/delete/<registro_id>')
def delete(registro_id):

    registro = Formula1.read_single(registro_id)
    return render_template("delete.html", registro=registro)

@app.route('/delete/<registro_id>/confirmed')
def delete_confirmed(registro_id):
    sucesso = False

    registro = Formula1.read_single(registro_id)

    if registro:

        registro.delete()

        sucesso = True
    
    return render_template("delete.html", registro=registro, sucesso=sucesso)


if (__name__ == '__main__'):
    app.run(debug=True)