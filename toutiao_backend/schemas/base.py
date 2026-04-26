from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class NewItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str]=None
    image: Optional[str]=None
    author: Optional[str]=None
    category_id: int=Field(...,alias="categoryId")
    views: int
    publish_time: Optional[datetime]=Field(...,alias="publishTime")

    model_config = ConfigDict(
        populate_by_name=True,  # alias/字段兼容
        from_attributes=True,  # 允许从orm对象中取值

    )
