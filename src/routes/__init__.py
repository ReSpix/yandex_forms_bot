from fastapi import APIRouter
from .debug import debug_router
from .general import general_router

main_router = APIRouter()

main_router.include_router(general_router)
main_router.include_router(debug_router)