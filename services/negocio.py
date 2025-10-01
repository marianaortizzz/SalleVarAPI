from models.negocio import Negocio as NegocioModel
from schemas.negocio import Negocio

class NegocioService:
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all(self):
        """
        Obtener todos los negocios
        """
        return self.db.query(NegocioModel).all()
    
    def get_by_id(self, id_negocio: int):
        """
        Obtener negocio por id
        """
        return self.db.query(NegocioModel).filter(NegocioModel.id_negocio == id_negocio).first()
    
    def create_negocio(self, negocio: Negocio):
        """
        Crear un negocio
        """
        negocio_data = negocio.model_dump()

        new_negocio = NegocioModel(**negocio_data)
        self.db.add(new_negocio)
        self.db.commit()
        self.db.refresh(new_negocio)
        return new_negocio
    
    def update_negocio(self, id_negocio: int, data: Negocio):
        """
        Actualizar negocio
        """
        negocio = self.db.query(NegocioModel).filter(NegocioModel.id_negocio == id_negocio).first()

        if not negocio:
            return None

        negocio.nombre = data.nombre
        negocio.categoria = data.categoria
        negocio.rating = data.rating
        negocio.rango_precios = data.rango_precios
        negocio.ubicacion = data.ubicacion
        negocio.nombre_responsable = data.nombre_responsable
        negocio.telefono = data.telefono
        negocio.categorias = data.categorias
        negocio.imagen = data.imagen
        negocio.horario_atencion = data.horario_atencion
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
