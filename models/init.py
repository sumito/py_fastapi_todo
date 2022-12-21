from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine



class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# DBへの接続を定義
sqlite_file_name = "todos.sql"
sqlite_url = f"sqlite:///{sqlite_file_name}" # エンジンデータベースのURL

engine = create_engine(sqlite_url, echo=True) # engineを作成
SQLModel.metadata.create_all(engine)  # モデルからテーブルを生成


