from fastapi import APIRouter, Request
from router.authtesting import router as auth_testing_router



router = APIRouter(prefix="/test", tags=["auth"])

router.include_router(auth_testing_router)



@router.get("/")
async def test_route(request: Request):
    """Public endpoint accessible to all."""
    return {"message": f"This is a test endpoint every endpoint that is a child of this one is meant for testing"}
