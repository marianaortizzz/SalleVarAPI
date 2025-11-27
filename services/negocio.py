from sqlalchemy import func
from models.negocio import Negocio as NegocioModel
from schemas.negocio import Negocio
from models.pedido import Pedido as PedidoModel
from models.detalle_pedido import DetallePedido as DetallePedidoModel  # OPCIONAL


class NegocioService:
    def __init__(self, db) -> None:
        self.db = db
    
    def obtener_negocios(self):
        """
        Obtener todos los negocios
        """
        return self.db.query(NegocioModel).all()
    
    def get_by_id(self, id_negocio: int):
        """
        Obtener negocio por id
        """
        return self.db.query(NegocioModel).filter(NegocioModel.id_negocio == id_negocio).first()
    
    # def create_negocio(self, negocio: Negocio):
    #     """
    #     Crear un negocio
    #     """
    #     negocio_data = negocio.model_dump()

    #     new_negocio = NegocioModel(**negocio_data)
    #     self.db.add(new_negocio)
    #     self.db.commit()
    #     self.db.refresh(new_negocio)
    #     return new_negocio
    
    def update_negocio(self, id_negocio: int, data: Negocio):
        """
        Actualizar negocio
        """
        negocio = self.db.query(NegocioModel).filter(NegocioModel.id_negocio == id_negocio).first()

        if not negocio:
            return None
        
        # Asignación de datos
        negocio.nombre = data.nombre
        # negocio.categoria = data.categoria  <-- BORRA ESTA LÍNEA (Error: no existe)
        
        negocio.rating = data.rating
        negocio.rango_precios = data.rango_precios
        negocio.ubicacion = data.ubicacion
        negocio.nombre_responsable = data.nombre_responsable
        negocio.telefono = data.telefono
        
        negocio.categorias = data.categorias # <-- ESTA ES LA CORRECTA
        
        negocio.imagen = data.imagen
        
        # CORRIGE ESTO TAMBIÉN (Deben ser dos campos, no "horario_atencion"):
        negocio.horario_apertura = data.horario_apertura 
        negocio.horario_cierre = data.horario_cierre
        
        negocio.activo = data.activo

        self.db.commit()
        self.db.refresh(negocio)
        return negocio
    
    def delete_negocio(self, id_negocio: int):
        """
        Eliminar negocio
        """
        result = self.db.query(NegocioModel).filter(NegocioModel.id_negocio == id_negocio).delete()
        self.db.commit()
        return result
    
    # registrar negocio
    def registrar_negocio(self, negocio: Negocio):
        """
        Crear un negocio
        """
        negocio_data = negocio.model_dump()

        new_negocio = NegocioModel(**negocio_data)
        self.db.add(new_negocio)
        self.db.commit()
        self.db.refresh(new_negocio)
        return new_negocio
    
    # filtrar negocios
    def filtrar_negocios(self, filtros):
        query = self.db.query(NegocioModel)

        # FILTRO POR CATEGORÍA
        if filtros.categoria:
            query = query.filter(NegocioModel.categorias.ilike(f"%{filtros.valor}%"))

        # FILTRO POR TEXTO (nombre, descripción, etc.)
        if filtros.texto:
            query = query.filter(
                (NegocioModel.nombre.ilike(f"%{filtros.valor}%"))
            )

        return query.all()

    # ESTADISTICA DE NEGOCIO
    def obtener_estadistica_negocio(self, id_negocio: int):
        """
        Obtener estadísticas básicas del negocio.
        """

        negocio = (
            self.db.query(NegocioModel)
            .filter(NegocioModel.id_negocio == id_negocio)
            .first()
        )

        if not negocio:
            return None

        # TOTAL DE PEDIDOS
        total_pedidos = (
            self.db.query(PedidoModel)
            .filter(PedidoModel.id_negocio == id_negocio)
            .count()
        )

        # TOTAL INGRESOS
        ingresos_totales = (
            self.db.query(func.sum(PedidoModel.monto_total))
            .filter(PedidoModel.id_negocio == id_negocio)
            .scalar()
        ) or 0

        # TOTAL PRODUCTOS VENDIDOS (SI EXISTE TABLA DETALLE)
        try:
            productos_vendidos = (
                self.db.query(func.sum(DetallePedidoModel.cantidad))
                .join(PedidoModel, DetallePedidoModel.id_pedido == PedidoModel.id_pedido)
                .filter(PedidoModel.id_negocio == id_negocio)
                .scalar()
            ) or 0
        except:
            # si no existe tabla detalle_pedido
            productos_vendidos = None

        # RATING DEL NEGOCIO
        rating = float(negocio.rating) if negocio.rating else 0.0

        return {
            "id_negocio": id_negocio,
            "total_pedidos": total_pedidos,
            "ingresos_totales": float(ingresos_totales),
            "productos_vendidos": productos_vendidos,
            "rating": rating
        }
    
    # LOGIN NEGOCIO
    def login_negocio(self, nombre: str, constrasena: str):
        """
        Login de negocio
        """
        negocio = (
            self.db.query(NegocioModel)
            .filter(
                NegocioModel.nombre == nombre,
                NegocioModel.constrasena == constrasena
            )
            .first()
        )
        return negocio

