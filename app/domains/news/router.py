from fastapi import APIRouter

router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_news():
    return [{"headline": "News 1"}, {"headline": "News 2"}]
