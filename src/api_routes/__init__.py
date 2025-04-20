from fastapi import APIRouter
from .debug import debug_router
from .general import general_router

api_router = APIRouter(prefix='/api')

api_router.include_router(general_router)
api_router.include_router(debug_router)