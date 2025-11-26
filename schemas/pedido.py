from pydantic import BaseModel, Field
from typing import Literal
from datetime import date
from decimal import Decimal
from typing import List, Optional
from schemas.producto_pedido import ProductoPedido
from schemas.repartidor import Repartidor

class Pedido(BaseModel):
    id_pedido: int
    fecha: str 
    status_general: str
    status_rest: str
    status_rep: str
    id_cliente: int
    id_negocio: int
    id_repartidor: Optional[int] = None
    subtotal: float
    costo_envio: float
    costo_servicio: float
    monto_total: float
    status_pago: str
    rating_pedido: Optional[int] = None
    rating_rep: Optional[int] = None
    codigo_restaurante: str
    codigo_repartidor: str
    delivery: bool
    repartidor: Optional[Repartidor] = None
    para_llevar: bool
    comentarios: str
    productos: List[ProductoPedido]


    class Config:
        json_schema = {
            "example": {
                "id_pedido": 1001,
                "fecha": "2024-10-01T12:30:00",
                "status_general": "En Proceso",
                "status_rest": "Preparando",
                "status_rep": "Asignado",
                "id_cliente": "cliente123",
                "id_negocio": "negocio456",
                "subtotal": 35.00,
                "costo_envio": 5.00,
                "costo_servicio": 5.75,
                "monto_total": 45.75,
                "status_pago": "Pagado",
                "rating_pedido": 5,
                "rating_rep": 4,
                "codigo_pedido": "PED789",
                "codigo_rep": "REP101",
                "repartidor": {
                    "id_repartidor": "rep123",
                    "nombre": "Juan Perez",
                    "telefono": "555-1234",
                    "vehiculo": "Moto"
                },
                "id_repartidor": "rep123",
                "para_llevar": False,
                "comentarios": "Por favor, entregar rápido.",
                "productos": [
                    {
                        "id_producto": "prod001",
                        "nombre": "Hamburguesa",
                        "precio": 15.50,
                        "descripcion": "Hamburguesa con queso y tocino",
                        "cantidad": 2,
                        "opciones_seleccionadas": ["Extra queso", "Sin cebolla"],
                        "comentarios_extra": "Bien cocida"
                    },
                    {
                        "id_producto": "prod002",
                        "nombre": "Papas Fritas",
                        "precio": 5.25,
                        "descripcion": "Papas fritas grandes",
                        "cantidad": 1,
                        "opciones_seleccionadas": [],
                        "comentarios_extra": ""
                    }
                ]
            }
        }
