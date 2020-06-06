import csv
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://uhgkbxajvrkqnl:94da5245d5c41a08a6cff3825e020f9c3dc72482100dbd902a4831826cd34281@ec2-52-87-58-157.compute-1.amazonaws.com:5432/dbommplhkogg50')

dataDB = pd.read_sql_query('select a.description||b.description||c.description as key, c.id \
from api_supplier a \
join api_product_category b on a.id = b.supplier_id \
join api_product c on b.id = c.product_category_id ',con=engine)

importFile = pd.read_csv("D:\\Dev\\magicHolidays\\dataUpload\\rezBeatrizBernal2.csv") 

mergeData = importFile.merge(dataDB,how='left')

mergeData.to_csv("D:\\Dev\\magicHolidays\\dataUpload\\exportResults2.csv")