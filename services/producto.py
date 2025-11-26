from models.producto import Producto as ProductoModel
from schemas.producto_menu import ProductoMenu
from models.modificador import ModificadorProducto as ModificadorProductoModel
from models.opcion import OpcionModificador as OpcionModificadorModel
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
        modificadores = producto_data.pop("modificadores", [])
        opciones = modificadores.pop("opciones", []) if modificadores else []
        new_producto = ProductoModel(**producto_data)
        if(modificadores):
            for mod in modificadores:
                new_modificador = ModificadorProductoModel(
                    nombre=mod['nombre'],
                    tipo=mod['tipo'],
                    id_producto=new_producto.id_producto
                )
                self.db.add(new_modificador)
                self.db.commit()
                self.db.refresh(new_modificador)
                for opcion in mod.get('opciones', []):
                    new_opcion = OpcionModificadorModel(
                        nombre=opcion['nombre'],
                        precio_adicional=opcion['precio_adicional'],
                        id_modificador=new_modificador.id_modificador
                    )
                    self.db.add(new_opcion)
        self.db.add(new_producto)
        self.db.commit()
        self.db.refresh(new_producto)
        return new_producto
    
    def update_producto(self, id_producto: int, data: ProductoMenu):
        """
        Actualizar producto y sus modificadores/opciones
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

        modificadores_data = data.modificadores
        for mod_data in modificadores_data:
            modificador = self.db.query(ModificadorProductoModel).filter(
                ModificadorProductoModel.id_modificador == mod_data.id_modificador
            ).first()

            if modificador:
                modificador.nombre_modificador = mod_data.nombre_modificador
                modificador.num_max_selec = mod_data.num_max_selec

                for opcion_data in mod_data.opciones:
                    opcion = self.db.query(OpcionModificadorModel).filter(
                        OpcionModificadorModel.id == opcion_data.id
                    ).first()

                    if opcion:
                        opcion.nombre = opcion_data.nombre
                        opcion.descripcion = opcion_data.descripcion
                        opcion.precio = opcion_data.precio
                        opcion.disponible = opcion_data.disponible
                    else:
                        nueva_opcion = OpcionModificadorModel(
                            nombre=opcion_data.nombre,
                            descripcion=opcion_data.descripcion,
                            precio=opcion_data.precio,
                            disponible=opcion_data.disponible,
                            modificador_id=modificador.id_modificador
                        )
                        self.db.add(nueva_opcion)
            else:
                # Crear nuevo modificador
                nuevo_modificador = ModificadorProductoModel(
                    nombre_modificador=mod_data.nombre_modificador,
                    num_max_selec=mod_data.num_max_selec,
                    id_producto=id_producto
                )
                self.db.add(nuevo_modificador)

                # Agregar opciones al nuevo modificador
                for opcion_data in mod_data.opciones:
                    nueva_opcion = OpcionModificadorModel(
                        nombre=opcion_data.nombre,
                        descripcion=opcion_data.descripcion,
                        precio=opcion_data.precio,
                        disponible=opcion_data.disponible,
                        modificador_id=nuevo_modificador.id_modificador
                    )
                    self.db.add(nueva_opcion)

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
