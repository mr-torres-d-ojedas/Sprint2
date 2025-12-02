from fastapi import APIRouter

from views import pedidos_views

API_PREFIX = "/api"
router = APIRouter()

router.include_router(pedidos_views.router, prefix=pedidos_views.ENDPOINT_NAME)