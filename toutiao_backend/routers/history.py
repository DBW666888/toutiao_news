from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history",tags=["history"])


@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        user: User=Depends(get_current_user),
        db: AsyncSession=Depends(get_db)
):
    result = await history.add_news_history(db,user.id,data.news_id)
    return success_response(message="添加成功",data=result)


@router.delete("/remove")
async def remove_history(
        news_id: int=Query(..., alias="newsId"),
        user: User=Depends(get_current_user),
        db: AsyncSession=Depends(get_db)
):
    result = await history.remove_news_history(db,user.id,news_id)
    if not result:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    return success_response(message="删除成功")


@router.delete("/delete/{news_id}")
async def delete_history(
        news_id: int=Path(...),
        user: User=Depends(get_current_user),
        db: AsyncSession=Depends(get_db)
):
    result = await history.remove_news_history(db,user.id,news_id)
    if not result:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    return success_response(message="删除成功")


@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, alias="pageSize", ge=1, le=100),
        user: User=Depends(get_current_user),
        db: AsyncSession=Depends(get_db)
):
    rows,total = await history.get_history_list(db,user.id,page,page_size)
    history_list=[{
        **news.__dict__,
        "view_time": view_time,
        "history_id": history_id
    }for news,view_time,history_id in rows]
    has_more=total > page*page_size

    data=HistoryListResponse(list=history_list,total=total,hasMore=has_more)
    return success_response(message="获取历史列表成功",data=data)


@router.delete("/clear")
async def clear_history(
        user: User=Depends(get_current_user),
        db: AsyncSession=Depends(get_db)
):
    count=await history.remove_all_histories(db,user.id)
    return success_response(message=f"清空了{count}条历史记录")
