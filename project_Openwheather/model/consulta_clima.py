from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from database.connection import Base

class ConsultaClima(Base):
    __tablename__ = "consultas_clima"

    id = Column(Integer, primary_key=True)
    cidade = Column(String(120), nullable=False)
    pais = Column(String(10))
    descricao = Column(String(120), nullable=False)
    temperatura = Column(Float, nullable=False)
    temp_min = Column(Float)
    temp_max = Column(Float)
    sensacao_termica = Column(Float)
    umidade = Column(Integer)
    pressao = Column(Integer)
    velocidade_vento = Column(Float)
    observacao = Column(String(255), default="")
    data_consulta = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "cidade": self.cidade,
            "pais": self.pais,
            "descricao": self.descricao,
            "temperatura": self.temperatura,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "sensacao_termica": self.sensacao_termica,
            "umidade": self.umidade,
            "pressao": self.pressao,
            "velocidade_vento": self.velocidade_vento,
            "observacao": self.observacao,
            "data_consulta": self.data_consulta.strftime("%d/%m/%Y %H:%M")
        }
