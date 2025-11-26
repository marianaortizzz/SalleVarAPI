from models.cliente import Cliente as ClienteModel
from schemas.cliente import Cliente
from schemas.LoginRequest import LoginRequest
from schemas.LoginResponse import LoginResponse
from schemas.RepartidorResponse import RepartidorResponse
from schemas.UsuarioResponse import UsuarioResponse

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
    
    # LOGIN
    def login(self, login_data: LoginRequest):
        usuario = self.db.query(ClienteModel).filter(
            (ClienteModel.nombre_completo == login_data.usuario) |
            (ClienteModel.matricula == login_data.usuario)
        ).first()

        if not usuario:
            return None
        
        if usuario.contrasena != login_data.contrasena:
            return False

        return usuario

    # CONVERTIR A USUARIO
    def convert_to_usuario(self, cliente: ClienteModel):
        return UsuarioResponse(
            id_usuario=cliente.id_cliente,
            nombre_usuario=str(cliente.matricula),
            nombre_completo=cliente.nombre_completo,
            matricula=cliente.matricula,
            carrera=cliente.carrera,
            negocio_favorito=cliente.negocios_favoritos,
            foto=cliente.foto,
            telefono=cliente.telefono,
            edificio=cliente.edificio,
            salon=cliente.salon
        )

    # CONVERTIR A REPARTIDOR
    def convert_to_repartidor(self, cliente: ClienteModel):
        numero_pedidos = 0
        rating_promedio = 5.0

        return RepartidorResponse(
            id_usuario=cliente.id_cliente,
            nombre_completo=cliente.nombre_completo,
            telefono=cliente.telefono,
            foto=cliente.foto,
            numero_pedidos=numero_pedidos,
            rating_repartidor=rating_promedio
        )
    
    #Calificar cliente
    def calificar_como_cliente(self, id_cliente: int, calificacion: int):
        cliente = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == id_cliente).first()

        if not cliente:
            return False
        nueva_calificacion = (calificacion + cliente.calificacion_cliente) / 2
        cliente.calificacion_cliente = nueva_calificacion

        self.db.commit()
        self.db.refresh(cliente)
        return True
    
    #Calificar repartidor
    def calificar_como_repartidor(self, id_repartidor: int, calificacion: int):
        repartidor = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == id_repartidor, ClienteModel.repartidor == True).first()

        if not repartidor:
            return False
        
        nueva_calificacion = (calificacion + repartidor.calificacion_repartidor) / 2
        
        repartidor.calificacion_repartidor = nueva_calificacion

        self.db.commit()
        self.db.refresh(repartidor)
        return True