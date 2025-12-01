from schemas.producto import Producto, ProductoCreate, ProductoUpdate
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
from schemas.modificador_producto import ModificadorProductoCreate
from schemas.modificador_producto import ModificadorProducto
from schemas.modificador_producto import OpcionModificadorCreate
from typing import List
from schemas.modificador_producto import ModificadorProductoUpdate
from schemas.modificador_producto import OpcionModificadorUpdate


class ProductoService:
    def __init__(self, db) -> None:
        self.db = db    
    def get_menu(self, id_restaurante: int):
        """
        Obtener todos los productos
        """
        productos = self.db.query(ProductoModel).filter(ProductoModel.id_negocio == id_restaurante).options(
            joinedload(ProductoModel.modificadores).joinedload(ModificadorProductoModel.opciones)
        ).all()
        return productos

    def get_product_by_id(self, id_producto: int):
        """
        Obtener producto por id
        """
        return self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).options(
            joinedload(ProductoModel.modificadores).joinedload(ModificadorProductoModel.opciones)
        ).first()
    
    def create_producto_completo(self, product_data: ProductoCreate, id_negocio: int):
        producto_fields = product_data.model_dump(exclude={"modificadores"})
        db_producto = ProductoModel(**producto_fields, id_negocio=id_negocio) 
        if(product_data.modificadores):
            for mod_in in product_data.modificadores:
                modificador_fields = mod_in.model_dump(exclude={"opciones"})
                db_modificador = ModificadorProductoModel(**modificador_fields)
                for opcion_in in mod_in.opciones:
                    opcion_fields = opcion_in.model_dump()
                    db_opcion = OpcionModificadorModel(**opcion_fields)
                    db_modificador.opciones.append(db_opcion)
                db_producto.modificadores.append(db_modificador)
        self.db.add(db_producto)
        self.db.commit() 
        self.db.refresh(db_producto) 
        
        return db_producto

    def update_producto_completo(self, producto_id: int, product_data: ProductoUpdate):
        
        db_producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == producto_id).first()
        if not db_producto:
            return None 

        update_data = product_data.model_dump(exclude_unset=True, exclude={"modificadores"})
        for key, value in update_data.items():
            setattr(db_producto, key, value)
            
        if product_data.modificadores is not None:
            existing_modificadores = {m.id_modificador: m for m in db_producto.modificadores}
            incoming_modificadores_ids = set()

            for mod_in in product_data.modificadores:
                mod_id = mod_in.id_modificador
                
                if mod_id and mod_id in existing_modificadores:
                    db_modificador = existing_modificadores[mod_id]
                    incoming_modificadores_ids.add(mod_id)
                    mod_update_data = mod_in.model_dump(exclude_unset=True, exclude={"opciones"})
                    for key, value in mod_update_data.items():
                        setattr(db_modificador, key, value)

                    if mod_in.opciones is not None:
                        self._update_opciones(db_modificador, mod_in.opciones)
                        
                else:
                    mod_fields = mod_in.model_dump(exclude={"opciones"})
                    db_new_mod = ModificadorProductoModel(**mod_fields)
                    
                    if mod_in.opciones:
                        for opcion_in in mod_in.opciones:
                            opcion_fields = opcion_in.model_dump()
                            db_new_opcion = OpcionModificadorModel(**opcion_fields)
                            db_new_mod.opciones.append(db_new_opcion)
                            
                    db_producto.modificadores.append(db_new_mod)
            mods_to_delete = [
                m for m in db_producto.modificadores
                if m.id_modificador not in incoming_modificadores_ids
                and m.id_modificador is not None
            ]
            for mod_to_del in mods_to_delete:
                self.db.delete(mod_to_del)
        self.db.commit()
        self.db.refresh(db_producto)
        return db_producto

    def _update_opciones(self, db_modificador: ModificadorProducto, opciones_data: List[OpcionModificadorUpdate]):
        """Función auxiliar para manejar el anidamiento de Opciones."""
        existing_opciones = {o.id: o for o in db_modificador.opciones}
        incoming_opciones_ids = set()
        
        for opcion_in in opciones_data:
            opcion_id = opcion_in.id_opcion
            
            if opcion_id and opcion_id in existing_opciones:
                db_opcion = existing_opciones[opcion_id]
                incoming_opciones_ids.add(opcion_id)
                
                opcion_update_data = opcion_in.model_dump(exclude_unset=True)
                for key, value in opcion_update_data.items():
                    setattr(db_opcion, key, value)
            else:
                opcion_fields = opcion_in.model_dump()
                db_new_opcion = OpcionModificadorModel(**opcion_fields)
                db_modificador.opciones.append(db_new_opcion)

        opciones_to_delete = [
            o for o in db_modificador.opciones 
            if o.id not in incoming_opciones_ids
            and o.id is not None
        ]
        for opcion_to_del in opciones_to_delete:
            self.db.delete(opcion_to_del)

    def delete_producto(self, id_producto: int):
        """
        Eliminar producto
        """
        result = self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).delete()
        self.db.commit()
        return result
    
    def obtener_producto_por_id(self, id_producto: int):
        """
        Obtener producto por id
        """
        return self.db.query(ProductoModel).filter(ProductoModel.id_producto == id_producto).options(joinedload(ProductoModel.modificadores).joinedload(ModificadorProductoModel.opciones)).first()
    