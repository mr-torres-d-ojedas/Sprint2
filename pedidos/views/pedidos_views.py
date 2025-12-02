from fastapi import APIRouter, status, Body
import logic.pedidos_logic as pedidos_service
from models.models import Pedido, PedidoOut, PedidoCollection

router = APIRouter()
ENDPOINT_NAME = "/pedidos"


@router.get(
    "/",
    response_description="Listando los pedidos",
    response_model=PedidoCollection,
    status_code=status.HTTP_200_OK,
)
async def get_pedidos():
    return await pedidos_service.get_pedidos()


@router.get(
    "/{pedido_code}",
    response_description="Obteniendo un pedido por código",
    response_model=PedidoOut,
    status_code=status.HTTP_200_OK,
)
async def get_pedido(pedido_code: str):
    return await pedidos_service.get_pedido(pedido_code)


@router.post(
    "/",
    response_description="Creando un pedido",
    response_model=PedidoOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_pedido(pedido: Pedido = Body(...)):
    return await pedidos_service.create_pedido(pedido)


@router.put(
    "/{pedido_code}",
    response_description="Actualizando un pedido",
    response_model=PedidoOut,
    status_code=status.HTTP_200_OK,
)
async def update_pedido(pedido_code: str, pedido: Pedido = Body(...)):
    return await pedidos_service.update_pedido(pedido_code, pedido)


@router.delete(
    "/{pedido_code}",
    response_description="Borrando Pedido",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_pedido(pedido_code: str):
    return await pedidos_service.delete_pedido(pedido_code)