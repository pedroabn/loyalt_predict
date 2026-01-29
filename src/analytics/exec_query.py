#%%
import pandas as pd
import datetime
import sqlalchemy
import argparse
#%%
def import_query(path):
    with open(path) as open_file:
        query = open_file.read()
        return query
    
def date_range(start, stop):
    dates = []
    while start <= stop:
        dates.append(start)
        dt_start = datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(days=1)
        start = datetime.datetime.strftime(dt_start, "%Y-%m-%d")
    return dates


#%%
def exec_query(table, db_origin, db_target, date_start, date_stop):
    engine_app = sqlalchemy.create_engine(f"sqlite:///../../data/{db_origin}/database.db")
    engine_analytics = sqlalchemy.create_engine(f"sqlite:///../../data/{db_target}/database.db")
    query = import_query(f'{table}.sql')
    dates = date_range(date_start, date_stop)

    for i in tqdm(dates):
        with engine_analytics.connect() as con:
            try:
                query_delete = f"DELETE FROM {table} WHERE dtRef = date('{i}', '-1 day')"
                con.execute(sqlalchemy.text(query_delete))
                con.commit()
            except Exception as err:
                print(err)
                
        query_format = query.format(date=i)
        df = pd.read_sql(query_format, engine_app)
        df.to_sql("life_cycle", engine_analytics, index=False, if_exists="append")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_origin', choices=['loyalt_system', 'education_plataform'],
                        default='loyalt_system')
    parser.add_argument('--db_target', choices=['analytics'])
    parser.add_argument('--table', type=str)
    parser.add_argument('--start', type=str, default="2025-12-01")

    stop = datetime.datetime.now().strftime('%Y-%m-%d')
    db_origin = 'loyalt_system'
    db_target = 'analytics'
    table = "life_cycle"
    date_start = "2025-12-01"
    date_stop = "2026-01-01"
