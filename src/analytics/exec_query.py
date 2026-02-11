# %%
import argparse
import datetime
from tqdm import tqdm
from pathlib import Path
import pandas as pd
import sqlalchemy


def import_query(tb):
    # Busca universal de caminho
    current_dir = Path(__file__).parent
    sql_path = current_dir / f"{tb}"
    
    if not sql_path.exists():
        raise FileNotFoundError(f"Arquivo SQL não encontrado: {sql_path}")
    
    with open(sql_path, 'r', encoding='utf-8') as open_file:
        query = open_file.read()
    
    return query


def date_range(start, stop, monthly=False):
    dates = []
    while start <= stop:
        dates.append(start)
        dt_start = datetime.datetime.strptime(start, '%Y-%m-%d') + datetime.timedelta(days=1)
        start = datetime.datetime.strftime(dt_start, '%Y-%m-%d')
        
    if monthly:
        return [i for i in dates if i.endswith("01")]
    
    return dates


def exec_query(table, db_origin, db_target, dt_start, dt_stop, monthly, mode='append'):
    
    current_dir = Path(__file__).parent  # src/analytics/
    project_root = current_dir.parent.parent  # raiz do projeto
    
    db_origin_path = project_root / "data" / db_origin / "database.db"
    db_target_path = project_root / "data" / db_target / "database.db"
    
    # Cria diretórios se não existirem
    db_origin_path.parent.mkdir(parents=True, exist_ok=True)
    db_target_path.parent.mkdir(parents=True, exist_ok=True)
    
    engine_app = sqlalchemy.create_engine(f"sqlite:///{db_origin_path}")
    engine_analytical = sqlalchemy.create_engine(f"sqlite:///{db_target_path}")

    query = import_query(f"{table}.sql")
    dates = date_range(dt_start, dt_stop, monthly)

    for i in tqdm(dates):
        
        if mode == 'append':
            with engine_analytical.connect() as con:
                try:
                    query_delete = f"DELETE FROM {table} WHERE dtRef = date('{i}', '-1 day')"
                    con.execute(sqlalchemy.text(query_delete))
                    con.commit()
                except Exception as err:
                    print(err)
        
        query_format = query.format(date=i)
        df = pd.read_sql(query_format, engine_app)
        df.to_sql(table, engine_analytical, index=False, if_exists=mode)


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_origin", choices=['loyalty_system', 'education_platform', 'analytics'],
                        default='loyalty_system')
    
    parser.add_argument("--db_target", choices=['analytics'], default='analytics')
    parser.add_argument("--table", type=str, help="Tabela que será processada com o mesmo nome do arquivo.")

    now = datetime.datetime.now().strftime("%Y-%m-%d")
    parser.add_argument("--start", type=str, default=now)
    parser.add_argument("--stop", type=str, default=now)
    parser.add_argument("--monthly", action='store_true')
    parser.add_argument("--mode", choices=['append', 'replace'], default="append")
    args = parser.parse_args()
    
    exec_query(args.table, args.db_origin, args.db_target, args.start, args.stop, args.monthly)


if __name__ == "__main__":
    main()