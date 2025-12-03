"""
This module contains the logic for the pedidos app.
Main functions:
- get_pedidos: Get a list of all pedidos
- get_pedidos: Get a single pedidos
- create_pedidos: Create a new pedidos
- update_pedidos: Update a pedidos
- delete_pedidos: Delete a pedidos
"""

from models.models import Pedido, PedidoCollection
from models.db import pedidos_collection
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
import requests
import json

async def get_pedidos():
    """
    Get a list of pedidos
    :return: A list of pedidos
    """
    pedidos = await pedidos_collection.find().to_list(1000)
    return PedidoCollection(pedidos = pedidos)


async def get_pedido(pedido_code: str):
    """
    Get a single Pedido
    :param pedido: The code of the pedido
    :return: The pedido
    """
    if (pedido := await pedidos_collection.find_one({"code": pedido_code})) is not None:
        return pedido

    raise HTTPException(
        status_code=404, detail=f"Pedido with code {pedido_code} not found"
    )





async def get_price_product(product_id):
    """
    Obtiene el precio de un producto desde el microservicio de productos
    """
    PATH_PRODUCT = f"http://3.231.224.209:8000/productos/{product_id}"

    try:
        r = requests.get(PATH_PRODUCT, headers={"Accept": "application/json"}, timeout=5)
        
        if r.status_code != 200:
            return None

        data = r.json()
        product_data = data.get("data")

        if not product_data:
            return None

        # Retorna el precio o 0 si no existe
        return product_data.get("precio", 0)

    except Exception as e:
        print(f"Error al obtener precio del producto {product_id}: {e}")
        return None


async def check_product(product_id):
    """
    Verifica que un producto exista en el microservicio
    """
    PATH_PRODUCT = f"http://3.231.224.209:8000/productos/{product_id}"

    try:
        r = requests.get(PATH_PRODUCT, headers={"Accept": "application/json"}, timeout=5)
        return r.status_code == 200
    except Exception as e:
        print(f"Error al verificar producto {product_id}: {e}")
        return False


async def create_pedido(pedido: Pedido):
    """
    Insert a new pedido record with validation of product IDs and price calculation.
    """

    try:
        # 1) Validar productos y calcular valorTotal ANTES de insertar
        valor_total = 0.0
        productos_validados = []

        for product_id in pedido.productos:
            # Verificar que el producto existe
            exists = await check_product(product_id)

            if not exists:
                raise HTTPException(
                    status_code=404,
                    detail=f"Producto {product_id} not found in product service",
                )

            # Obtener precio del producto
            precio = await get_price_product(product_id)

            if precio is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al obtener precio del producto {product_id}",
                )

            # Sumar al total
            valor_total += precio
            productos_validados.append(product_id)

        # 2) Actualizar el valorTotal en el objeto pedido ANTES de insertarlo
        pedido.valorTotal = valor_total
        pedido.productos = productos_validados

        # 3) Insertar el pedido con el valorTotal ya calculado
        new_pedido = await pedidos_collection.insert_one(
            pedido.model_dump(by_alias=True, exclude=["id"])
        )

        pedido_id = new_pedido.inserted_id

        # 4) Recuperar el pedido creado y devolverlo
        created_pedido = await pedidos_collection.find_one({"_id": pedido_id})
        
        return created_pedido

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail=f"Pedido with code {pedido.code} already exists"
        )
    except HTTPException:
        # Re-lanzar excepciones HTTP ya manejadas
        raise
    except Exception as e:
        print(f"Error inesperado al crear pedido: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al crear pedido: {str(e)}"
        )



async def update_pedido(pedido_code: str, pedido: Pedido):
    """
    Update a pedidos
    :param pedidos_code: The code of the pedidos
    :param pedidos: The pedidos data
    :return: The updated pedidos
    """

    try:
        update_result = await pedidos_collection.update_one(
            {"code": pedido_code},
            {"$set": pedido.model_dump(by_alias=True, exclude=["id"])},
        )
        if update_result.modified_count == 1:
            if (
                updated_pedido := await pedidos_collection.find_one({"code": pedido.code})
            ) is not None:
                return updated_pedido
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409, detail=f"Pedido with code {pedido.code} already exists"
        )

    raise HTTPException(
        status_code=404,
        detail=f"Pedido with code {pedido_code} not found or no updates were made",
    )


async def delete_pedido(pedido_code: str):
    """
    Delete a pedido
    :param pedido_code: The code of the pedido
    """
    delete_result = await pedidos_collection.delete_one({"code": pedido_code})

    if delete_result.deleted_count == 1:
        return

    raise HTTPException(
        status_code=404, detail=f"Pedido with code {pedido_code} not found"
    )