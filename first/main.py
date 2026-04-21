from fastapi import FastAPI,Path,Query,HTTPException
from fastapi.responses import HTMLResponse,FileResponse
from pydantic import BaseModel,Field


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/book/{id}")
async def get_book(id: int=Path(...,gt=0,lt=101)):
    return {"id":id,"message": f"这是第{id}本书"}

@app.get("/new/new_list")
async def get_new_list(
        skip: int=Query(0,lt=101),
        limit: int=Query(10)):
    return {"skip":skip,"limit": limit}



class User(BaseModel):
    username: str=Field(...,min_length=2,max_length=10)
    password: str=Field(...,min_length=6,max_length=20)
@app.post("/register")
async def register(user: User):
    return user

@app.get("/html",response_class=HTMLResponse)
async def get_html():
    return "<h1>这是一个一级标题</h1>"


@app.get("/file")
async def get_file():
    path="./file/dog.png"
    return FileResponse(path)


class News(BaseModel):
    id:int
    title:str
    content:str
@app.get("/news/{id}",response_model=News)
async def get_news(id:int):
    return {
        "id":id,
        "title":f"这是第{id}本书",
        "content":"这是一本好书",
    }

@app.get("/pages/{id}")
async def get_pages(id:int):
    id_list=[1,2,3,4,5,6]
    if id not in id_list:
        raise HTTPException(status_code=404,detail="您查找的页面不存在")
    return {"id":id}
