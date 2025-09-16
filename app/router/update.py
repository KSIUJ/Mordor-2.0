from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
import router.user.tagRouter as tags
from repository.fileRepository import FileRepository
templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/update")

@router.get("/{file_id}")
async def uploadPage(request: Request,
                     file_id: int):
    repo=FileRepository()
    data=await tags.tags()
    file=await repo.get_file_by_id(file_id)
    filetags=await repo.get_files_tags(file_id)
    data=[tag for tag in data if tag not in filetags]
    # TODO: ADD VALIDATION SO USERS CAN ONLY SEE MODIFIABLE FILES
    return templates.TemplateResponse("fileUpdate.html",
                                      {
                                          "request": request,
                                          "tags": data,
                                          "file": file,
                                          "filetags": filetags,
                                      })