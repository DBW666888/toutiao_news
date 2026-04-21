from datetime import datetime
from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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

#分页查询
@app.get("/book/get_book_list")
async def get_book_list(
        page: int = 1,
        page_size: int = 3,
        db: AsyncSession = Depends(get_db)
):
    # （页码 - 1） * 每页数量
    skip = (page - 1) * page_size

    # offset 跳过的记录数  ； limit 每页的记录数
    stmt = select(Book).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books


# #聚合查询
# @app.get("/book/count")
# async def get_count(db: AsyncSession = Depends(get_db)):
#     # result = await db.execute(select(func.count(Book.id)))
#     # result = await db.execute(select(func.max(Book.price)))
#     # result = await db.execute(select(func.sum(Book.price)))
#     result = await db.execute(select(func.avg(Book.price)))
#     num = result.scalar()
#     return num


# #模糊查询
# @app.get("/book/search_book")
# async def get_search_book(db: AsyncSession = Depends(get_db)):
#     # result = await db.execute(select(Book).where(Book.author.like("曹_")))
#     # result = await db.execute(select(Book).where((Book.author.like("曹%")) | (Book.price > 100)))
#     id_list = [1, 3, 5, 7]
#     result = await db.execute(select(Book).where(Book.id.in_(id_list)))
#     book = result.scalars().all()
#     return book


# #比较判断
# @app.get("/book/get_book/{book_id}")
# async def get_book_list(book_id: int, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Book).where(Book.id == book_id))
#     book = result.scalar_one_or_none()
#     return book
#
# @app.get("/book/search_book")
# async def get_search_book(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Book).where(Book.price >= 200))
#     books = result.scalars().all()
#     return books


# #查询数据
# @app.get("/book/get_books")
# async def get_book_list(db: AsyncSession = Depends(get_db)):
#     #查询
#     result=await db.execute(select(Book))
#     book = result.scalars().all()
#     return book
#
# @app.post("/book/add")
# async def add_book(bookname: str, author: str, price: float, publisher: str, db: AsyncSession = Depends(get_db)):
#     # 创建新书籍
#     new_book = Book(
#         bookname=bookname,
#         author=author,
#         price=price,
#         publisher=publisher
#     )
#     # 添加到数据库
#     db.add(new_book)
#     await db.commit()
#     await db.refresh(new_book)
#     return new_book


# 中间件的使用
# @app.middleware("http")
# async def middleware1(request, call_next):
#     print("middleware_1 start")
#     response=await call_next(request)
#     print("middleware_1 end")
#     return response
#
# @app.middleware("http")
# async def middleware2(request, call_next):
#     print("middleware_2 start")
#     response=await call_next(request)
#     print("middleware_2 end")
#     return response


# 依赖注入
# async def common_parameters(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(10, le=60),
# ):
#     return {"skip": skip, "limit": limit}
#
# @app.get("/new/new_list")
# async def get_new_list(commons = Depends(common_parameters)):
#     return commons


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
