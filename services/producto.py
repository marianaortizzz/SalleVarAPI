from models.producto import Producto as ProductoModel
from schemas.producto import Producto

class ProductoService:
    def __init__(self, db) -> None:
        self.db = db    
    def get_all(self):
        """
        Obtener todos los productos
        """
        return self.db.query(ProductoModel).all()
    def get_by_id(self, id_producto: int):
        """
        Obtener producto por id
        """
        return self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).first()
    def create_producto(self, producto: Producto):
        """
        Crear un producto
        """
        producto_data = producto.model_dump()

        new_producto = ProductoModel(**producto_data)
        self.db.add(new_producto)
        self.db.commit()
        self.db.refresh(new_producto)
        return new_producto
    def update_producto(self, id_producto: int, data: Producto):
        """
        Actualizar producto
        """
        producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).first()

        if not producto:
            return None
        
        producto.nombre = data.nombre
        producto.precio = data.precio
        producto.descripcion = data.descripcion
        producto.imagen = data.imagen
        producto.categoria = data.categoria
        producto.disponible = data.disponible
        producto.id_negocio = data.id_negocio

        self.db.commit()
        self.db.refresh(producto)
        return producto
    
    def delete_producto(self, id_producto: int):
        """
        Eliminar producto
        """
        result = self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).delete()
        self.db.commit()
        return result
        