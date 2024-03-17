import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np

cnx = mysql.connector.connect(user='root', password='XMJsql123456',
                              host='127.0.0.1',
                              database='penguins')

specie = (
    "create table specie("
    "`id`  int Not null auto_increment,"
    "`species` char(32) not null,"
    "`island` char(32) not null,"
    "`blen` decimal(4,1) null,"
    "`bdep` decimal(4,1) null,"
    "`flen` SMALLINT null,"
    "`mass` SMALLINT null,"
    "`sex` bool null,"
    "primary key (id)"
    ") engine=InnoDB"
)
add_sp = "insert into specie (species, island, blen, bdep, flen, mass, sex) VALUES "

data = pd.read_csv("penguins.csv")

data = np.array(data)
data[data == "MALE"] = 1
data[data == "FEMALE"] = 0
data = data.tolist()

for item in data:
    sp = "("
    for it in item:
        if type(it) == float and np.isnan(it):
            sp += "null,"
        else:
            sp += f"'{it}',"
    sp = sp[:-1] + "),"
    add_sp += sp
add_sp = add_sp[:-1] + ";"

cursor = cnx.cursor()

# 创建表
try:
    cursor.execute(specie)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
    else:
        print(err.msg)
else:
     print("OK")

# 插入数据
try:
    cursor.execute(add_sp)
except mysql.connector.Error as err:
    print(err.msg)
else:
     print("OK")

cnx.commit()        # 提交数据到数据库

cursor.close()
cnx.close()