from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
import router.user.tagRouter as tags

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/upload")

@router.get("/")
async def uploadPage(request: Request):
    data=await tags.tags()
    return templates.TemplateResponse("fileUpload.html",
                                      {
                                          "request": request,
                                          "tags": data
                                      })
