from models.Calificacion import Calificacion
from models.cliente import Cliente as ClienteModel
from models.negocio import Negocio as NegocioModel

class CalificacionService:
    def __init__(self, db):
        self.db = db

    def calificar(self, data):
        origen = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == data.id_origen).first()

        if not origen:
            return None, "Cliente que califica no existe"

        # REGLAS SEGÚN TIPO DE CLIENTE
        if not origen.repartidor:
            # Usuario
            if data.tipo_destino not in [2, 3]:
                return None, "Un usuario solo puede calificar repartidores y negocios"
        else:
            # Repartidor
            if data.tipo_destino != 1:
                return None, "Un repartidor solo puede calificar usuarios"

        # Validar destino según tipo
        if data.tipo_destino == 1 or data.tipo_destino == 2:
            destino = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == data.id_destino).first()
            if not destino:
                return None, "Cliente destino no existe"
        elif data.tipo_destino == 3:
            destino = self.db.query(NegocioModel).filter(NegocioModel.id_negocio == data.id_destino).first()
            if not destino:
                return None, "Negocio destino no existe"

        nueva = Calificacion(
            id_origen=data.id_origen,
            id_destino=data.id_destino,
            tipo_destino=data.tipo_destino,
            rating=data.rating
        )
        self.db.add(nueva)
        self.db.commit()

        return nueva, None
