from fastapi import APIRouter

from views import pedidos_view

API_PREFIX = "/api"
router = APIRouter()

router.include_router(pedidos_view.router, prefix=pedidos_view.ENDPOINT_NAME)