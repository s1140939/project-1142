from database import engine, Base
from models import Laptop

print("開始建立資料表")

Base.metadata.create_all(bind=engine)

print("資料表建立完成")