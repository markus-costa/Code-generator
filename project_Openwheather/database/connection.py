from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class DatabaseManager:
    def __init__(self, database_url="sqlite:///clima_app.db"):
        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def criar_tabelas(self):
        Base.metadata.create_all(self.engine)

    def criar_sessao(self):
        return self.Session()
