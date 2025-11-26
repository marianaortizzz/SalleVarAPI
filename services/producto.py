from config.database import SessionLocal
from models.producto import Producto as ProductoModel
from schemas.producto_menu import ProductoMenu
from models.modificador import ModificadorProducto as ModificadorProductoModel
from models.opcion import OpcionModificador as OpcionModificadorModel
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from schemas.modificador_producto import ModificadorProducto as ModificadorProductoSchema
from schemas.modificador_producto import OpcionModificador as OpcionModificadorSchema
from schemas.modificador_producto import OpcionModificador

class ProductoService:
    def __init__(self, db) -> None:
        self.db = db    
    def get_menu(self, id_restaurante: int):
        """
        Obtener todos los productos
        """

        productos = (
            self.db.query(ProductoModel)
            .filter(ProductoModel.id_negocio == id_restaurante)
            .all()
        )
        productos_with_modifiers = []
        for producto in productos:
            producto = ProductoMenu(
                id_producto=producto.id_producto,
                nombre=producto.nombre,
                precio=producto.precio,
                descripcion=producto.descripcion,
                imagen=producto.imagen,
                categoria=producto.categoria,
                disponible=producto.disponible,
                id_negocio=producto.id_negocio,
                modificadores=[],
            )
            modificadores = (
                self.db.query(ModificadorProductoModel)
                .filter(ModificadorProductoModel.id_producto.in_([producto.id_producto for p in productos]))
                .all()
            )
            for mod in modificadores:
                mod.opciones = (
                    self.db.query(OpcionModificadorModel)
                    .filter(OpcionModificadorModel.modificador_id.in_([mod.id_modificador for m in modificadores]))
                    .all()
                )
                producto.modificadores.append(mod)
            productos_with_modifiers.append(producto)
        return productos_with_modifiers
    
    def create_producto_completo(self, producto: ProductoMenu):
        producto_sin_modificadores = ProductoModel(
            nombre=producto.nombre,
            precio=producto.precio,
            descripcion=producto.descripcion,
            imagen=producto.imagen,
            categoria=producto.categoria,
            disponible=producto.disponible,
            id_negocio=producto.id_negocio
        )
        modificadores = producto.modificadores or []
        producto_creado = self.create_producto(producto_sin_modificadores)
        for mod in modificadores:
            modificador_creado = self.create_modificador(producto_creado.id_producto, mod)
            opciones = mod.opciones or []
            for opcion in opciones:
                self.create_opcion(modificador_creado.id_modificador, opcion)
        producto_completo = ProductoMenu(
            id_producto=producto_creado.id_producto,
            nombre=producto_creado.nombre,
            precio=producto_creado.precio,
            descripcion=producto_creado.descripcion,
            imagen=producto_creado.imagen,
            categoria=producto_creado.categoria,
            disponible=producto_creado.disponible,
            id_negocio=producto_creado.id_negocio,
            modificadores=modificadores
        )
        return producto_completo

    
    def create_producto(self, producto: ProductoMenu):
        """
        Crear un producto y sus modificadores/opciones
        """
        new_producto = ProductoModel(
            nombre=producto.nombre,
            precio=producto.precio,
            descripcion=producto.descripcion,
            imagen=producto.imagen,
            categoria=producto.categoria,
            disponible=producto.disponible,
            id_negocio=producto.id_negocio
        )
        self.db.add(new_producto)
        self.db.commit()
        if not self.db.is_active:
            self.db = SessionLocal()  # Reopen the session if needed

        self.db.merge(new_producto)
        self.db.refresh(new_producto)
        return new_producto
    
    def create_modificador(self, id_producto: int, modificador_data: ModificadorProductoSchema):
        """
        Crear un modificador y sus opciones
        """
        new_modificador = ModificadorProductoModel(
            nombre_modificador=modificador_data.nombre_modificador,
            num_max_selec=modificador_data.num_max_selec,
            id_producto=id_producto
        )
        self.db.add(new_modificador)
        self.db.commit()
        if not self.db.is_active:
            self.db = SessionLocal()  # Reopen the session if needed

        self.db.merge(new_modificador)
        self.db.refresh(new_modificador)
        return new_modificador

    def create_opcion(self, modificador_id: int, opcion_data: OpcionModificadorSchema):
        """
        Crear una opción de modificador
        """
        new_opcion = OpcionModificadorModel(
            nombre=opcion_data.nombre,
            descripcion=opcion_data.descripcion,
            precio=opcion_data.precio_adicional,
            disponible=opcion_data.disponible,
            modificador_id=modificador_id
        )
        self.db.add(new_opcion)
        self.db.commit()
        if not self.db.is_active:
            self.db = SessionLocal()  # Reopen the session if needed

        self.db.merge(new_opcion)
        self.db.refresh(new_opcion)
        return new_opcion
    
    def update_producto(self, id_producto: int, producto_data: ProductoMenu):
        """
        Actualizar un producto
        """
        producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        producto.nombre = producto_data.nombre
        producto.precio = producto_data.precio
        producto.descripcion = producto_data.descripcion
        producto.imagen = producto_data.imagen
        producto.categoria = producto_data.categoria
        producto.disponible = producto_data.disponible
        producto.id_negocio = producto_data.id_negocio

        self.db.commit()
        return producto

    def delete_producto(self, id_producto: int):
        """
        Eliminar producto
        """
        result = self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).delete()
        self.db.commit()
        return result
    
    