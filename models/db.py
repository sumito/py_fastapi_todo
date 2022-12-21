from sqlmodel import create_engine

# DBへの接続を定義
sqlite_file_name = "todos.sql"
sqlite_url = f"sqlite:///{sqlite_file_name}" # エンジンデータベースのURL
engine = create_engine(sqlite_url, echo=True) # engineを作成
