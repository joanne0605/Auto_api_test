import sqlalchemy as sqla
import pandas as pd
from configparser import ConfigParser
import os

cp = ConfigParser()
current_path = os.path.dirname(__file__)
cp.read(current_path+'/db_config/db.cfg')

def get_mysql(db,sql):
    # root:123456@172.22.1.170:32205  test环境
    host = cp.get('mysql_k8s_test',"host")
    port = cp.get('mysql_k8s_test', "port")
    user = cp.get('mysql_k8s_test', "user")
    password = cp.get('mysql_k8s_test', "password")

    engine = sqla.create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}')
    df = pd.read_sql('{}'.format(sql),engine)
    return df

def get_postgres(db,sql):
    cp.items('postgres_k8s_test')
    host = cp.get('postgres_k8s_test', "host")
    port = cp.get('postgres_k8s_test', "port")
    user = cp.get('postgres_k8s_test', "user")
    password = cp.get('postgres_k8s_test', "password")

    engine = sqla.create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df = pd.read_sql('{}'.format(sql), engine)
    return df

if __name__ == '__main__':
    df = get_mysql('playlist','select title from playlist_data limit 1')
    print(df['title'][0])

    df2 = get_postgres('cpl_service','select *from cpl limit 1')
    print(df2['uuid'][0])
