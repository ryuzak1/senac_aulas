from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TabelaNome

# Conexão com o banco de dados aula_teste no MySQL / phpMyAdmin
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/aula_teste"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def salvar_nome(nome, telefone):
    session = Session()
    try:
        novo_registro = TabelaNome(nome=nome, telefone=int(telefone))
        session.add(novo_registro)
        session.commit()
    finally:
        session.close()


# Função para listar os nomes com filtro opcional de pesquisa
def listar_nomes(pesquisa=""):
    session = Session()
    try:
        if pesquisa:
            return session.query(TabelaNome).filter(TabelaNome.nome.like(f"%{pesquisa}%")).all()
        return session.query(TabelaNome).all()
    finally:
        session.close()

# Função para excluir um registro pelo ID
def excluir_nome(id_registro):
    session = Session()
    try:
        registro = session.query(TabelaNome).filter_by(id=id_registro).first()
        if registro:
            session.delete(registro)
            session.commit()
            return True
        return False
    finally:
        session.close()


