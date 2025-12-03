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




async def check_product(product_id):
        PATH_PRODUCT = f"http://3.236.215.110:8000/productos/{product_id}"

        try:
            r = requests.get(PATH_PRODUCT, headers={"Accept": "application/json"})
            if r.status_code != 200:
                return False

            data = r.json()
            product_list = data.get("data", [])

            if len(product_list) == 0:
                return False

            return True

        except Exception:
            return False

async def get_price_product(product_id):
        PATH_PRODUCT = f"http://3.236.215.110:8000/productos/{product_id}"

        try:
            r = requests.get(PATH_PRODUCT, headers={"Accept": "application/json"})
            if r.status_code != 200:
                return False

            data = r.json()
            product_list = data.get("data", [])

            return product_list.precio

        except Exception:
            return 0
    

async def create_pedido(pedido: Pedido):
    """
    Insert a new pedido record with validation of product IDs.
    """

    # 1) Crear el pedido SIN productos (solo datos principales)
    try:
        new_pedido = await pedidos_collection.insert_one(
            pedido.model_dump(by_alias=True, exclude=["id"])
        )

        pedido_id = new_pedido.inserted_id

        # 2) Validar los productos
        for product_id in pedido.productos:

            # check_product debe ser async
            exists = await check_product(product_id)

            if exists is not True:
                # rollback → borrar el pedido que se creó
                await pedidos_collection.delete_one({"_id": pedido_id})

                raise HTTPException(
                    status_code=404,
                    detail=f"Producto {product_id} not found",
                )
            else:
                valor = await get_price_product(product_id)       
                pedido.valorTotal +=  valor
                    
        # 3) Buscar y retornar el pedido ya creado
        created_pedido = await pedidos_collection.find_one({"_id": pedido_id})
        return created_pedido

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail=f"Pedido with code {pedido.code} already exists"
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