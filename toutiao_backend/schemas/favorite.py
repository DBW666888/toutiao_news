from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool=Field(...,alias="isFavorite")



class FavoriteAddRequest(BaseModel):
    news_id: int=Field(...,alias="newsId")



class FavoriteNewsItemResponse(NewItemBase):
    favorite_id:int=Field(...,alias="favoriteId")
    favorite_time: datetime=Field(...,alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段兼容
        from_attributes=True,  # 允许从orm对象中取值
    )

#收藏列表接口响应模型类
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool=Field(...,alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段兼容
        from_attributes=True,  # 允许从orm对象中取值

    )
