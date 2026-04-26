from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update

from cache.news_cache import (
    get_cache_news_detail,
    get_cache_news_list,
    get_cached_categories,
    set_cache_categories,
    set_cache_news_detail,
    set_cache_news_list,
)
from models.news import Category, News
from schemas.base import NewItemBase


async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    #先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    categories=result.scalars().all()

    #写入缓存
    if categories:
        categories=jsonable_encoder(categories)
        await set_cache_categories(categories)

    #返回数据
    return categories


async def get_news_list(db: AsyncSession, category_id: int,limit: int = 10, skip: int = 0):
    # 先尝试从缓存中获取数据
    page=skip // limit + 1
    cached_list = await get_cache_news_list(category_id, page, limit)
    if cached_list:
        return [News(**item)for item in cached_list]

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        # ORM 转成 Pydantic，再转为 字典
        news_data = [NewItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)

    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_news_detail(db: AsyncSession, news_id: int):
    cached_detail = await get_cache_news_detail(news_id)
    if cached_detail:
        return News(**cached_detail)

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()

    if news_detail:
        await set_cache_news_detail(news_id, jsonable_encoder(news_detail))

    return news_detail


async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    if not result.rowcount:
        return False

    stmt = select(News).where(News.id == news_id)
    detail_result = await db.execute(stmt)
    news_detail = detail_result.scalar_one_or_none()
    if news_detail:
        await set_cache_news_detail(news_id, jsonable_encoder(news_detail))

    return True


async def get_related_news(db: AsyncSession, news_id: int,category_id: int,limit: int = 5):
    #order_by按浏览量和发布时间进行排序
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    #return result.scalars().all()
    related_news = result.scalars().all()
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
    } for news_detail in related_news]
