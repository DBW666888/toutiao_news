from datetime import datetime
from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
app = FastAPI()


#创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:2b2b123123@localhost:3306/fastapi_test?charset=utf8"
async_engine= create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

class Base(DeclarativeBase):
    create_time:Mapped[datetime]=mapped_column(DateTime, nullable=False, server_default=func.now())
    update_time:Mapped[datetime]=mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class Book(Base):
    __tablename__ = "book"

    id:Mapped[int]=mapped_column(primary_key=True,comment="book_id")
    bookname:Mapped[str]=mapped_column(String(255),comment="book_name")
    author:Mapped[str]=mapped_column(String(255),comment="author")
    price:Mapped[float]=mapped_column(Float,comment="price")
    publisher: Mapped[str] = mapped_column(String(255), comment="publisher")

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()

AsyncSessionLocal=async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

#删除数据
@app.delete("/book/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    # 先查再删 提交
    db_book = await db.get(Book, book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="查无此书"
        )

    await db.delete(db_book)
    await db.commit()
    return {"msg": "删除图书成功"}


# #更新数据
# class BookUpdate(BaseModel):
#     bookname: str
#     author: str
#     price: float
#     publisher: str
#
# @app.put("/book/update_book/{book_id}")
# async def update_book(book_id: int, data: BookUpdate, db: AsyncSession = Depends(get_database)):
#     db_book = await db.get(Book, book_id)
#     if db_book is None:
#         raise HTTPException(
#             status_code=404,
#             detail="查无此书"
#         )
#     db_book.bookname = data.bookname
#     db_book.author = data.author
#     db_book.price = data.price
#     db_book.publisher = data.publisher
#     await db.commit()
#     return db_book


# #新增数据
# class BookBase(BaseModel):
#     id: int
#     bookname: str
#     author: str
#     price: float
#     publisher: str
#
# @app.post("/book/add_book")
# async def add_book(book: BookBase, db: AsyncSession = Depends(get_db)):
#     book_obj = Book(**book.__dict__)
#     db.add(book_obj)
#     await db.commit()
#     return book


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
