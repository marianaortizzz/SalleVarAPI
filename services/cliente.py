from models.cliente import Cliente as ClienteModel
from schemas.cliente import Cliente

class ClienteService:
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all(self):
        """
        Obtener todos los clientes
        """
        return self.db.query(ClienteModel).all()
    
    def get_by_id(self, id_cliente: int):
        """
        Obtener cliente por id
        """
        return self.db.query(ClienteModel).filter(ClienteModel.id_cliente == id_cliente).first()
    
    def create_cliente(self, cliente: Cliente):
        """
        Crear un cliente
        """
        cliente_data = cliente.model_dump()

        new_cliente = ClienteModel(**cliente_data)
        self.db.add(new_cliente)
        self.db.commit()
        self.db.refresh(new_cliente)
        return new_cliente
    
    def update_cliente(self, id_cliente: int, data: Cliente):
        """
        Actualizar cliente
        """
        cliente = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == id_cliente).first()

        if not cliente:
            return None
        
        cliente.nombre_completo = data.nombre_completo
        cliente.matricula = data.matricula
        cliente.carrera = data.carrera
        cliente.repartidor = data.repartidor
        cliente.negocios_favoritos = data.negocios_favoritos
        cliente.contrasena = data.contrasena
        cliente.foto = data.foto
        cliente.telefono = data.telefono

        self.db.commit()
        self.db.refresh(cliente)
        return cliente
    
    def delete_cliente(self, id_cliente: int):
        """
        Eliminar cliente
        """
        result = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == id_cliente).delete()
        self.db.commit()
        return result
