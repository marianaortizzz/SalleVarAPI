from models.producto import Producto as ProductoModel
from schemas.producto_menu import ProductoMenu
from models.modificador import ModificadorProducto as ModificadorProductoModel

class ProductoService:
    def __init__(self, db) -> None:
        self.db = db    
    def get_menu(self, id_restaurante: int):
        """
        Obtener todos los productos
        """
        productos = self.db.query(ProductoModel).filter(ProductoModel.id_restaurante == id_restaurante).all()
        productos_with_modifiers = []
        for producto in productos:
            productoSchema = ProductoMenu(**producto.__dict__)
            productoSchema.modificadores = self.db.query(ModificadorProductoModel).filter(ModificadorProductoModel.id_producto == producto.id_producto).all()
            productos_with_modifiers.append(productoSchema)
        return productos_with_modifiers
    
    def create_producto(self, producto: ProductoMenu):
        """
        Crear un producto
        """
        producto_data = producto.model_dump()
        new_producto = ProductoModel(**producto_data)
        self.db.add(new_producto)
        self.db.commit()
        self.db.refresh(new_producto)
        return new_producto
    
    def update_producto(self, id_producto: int, data: ProductoMenu):
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
        