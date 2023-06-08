from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends
from middleware.validate_token import validate_token
from services.finance_analyzer.ex_ante import get_ex_ante

router = APIRouter()


@router.get("/")
async def ex_ante_controller(
    _: str = Depends(validate_token), overhours: int = 0
) -> JSONResponse:
    return JSONResponse(
        content={
            "message": "Ex ante income and expenses for the end of the current month.",
            "data": get_ex_ante(overhours),
        }
    )
