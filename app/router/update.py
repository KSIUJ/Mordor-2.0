from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
import router.user.tagRouter as tags

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/update")

@router.get("/")
async def uploadPage(request: Request):
    data=await tags.tags()
    return templates.TemplateResponse("fileUpdate.html",
                                      {
                                          "request": request,
                                          "tags": data
                                      })