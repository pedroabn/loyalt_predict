# %%
from exec_query import exec_query
import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d")

steps = [
    {
        "table":"life_cycle",
        "db_origin":"loyalty_system",
        "db_target":"analytics",
        "dt_start":'2025-01-01',
        "dt_stop":now,
        "monthly":False,
        "mode":"append"

    },
    {
        "table":"fs_transacional",
        "db_origin":"loyalty_system",
        "db_target":"analytics",
        "dt_start":'2025-01-01',
        "dt_stop":now,
        "monthly":False,
        "mode":"append"

    },
    {
        "table":"fs_educational",
        "db_origin":"education_platform",
        "db_target":"analytics",
        "dt_start":'2025-01-01',
        "dt_stop":now,
        "monthly":False,
        "mode":"append"
    },
    {
        "table":"clients",
        "db_origin":"loyalty_system",
        "db_target":"analytics",
        "dt_start":'2025-01-01',
        "dt_stop":now,
        "monthly":False,
        "mode":"append"

    },
    {
        "table":"fs_life_cycle",
        "db_origin":"analytics",
        "db_target":"analytics",
        "dt_start":'2025-01-01',
        "dt_stop":now,
        "monthly":False,

    },
    {
        "table":"fs_all",
        "db_origin":"analytics",
        "db_target":"analytics",
        "dt_start":now,
        "dt_stop":now,
        "monthly":False,

    },
    {
        "table":"sau",
        "db_origin":"loyalty_system",
        "db_target":"analytics",
        "dt_start":now,
        "dt_stop":now,
        "monthly":False,
    },
    {
        "table":"plot_sau",
        "db_origin":"analytics",
        "db_target":"analytics",
        "dt_start":now,
        "dt_stop":now,
        "monthly":False,
    },
    {
        "table":"meta_ciclo",
        "db_origin":"analytics",
        "db_target":"analytics",
        "dt_start":now,
        "dt_stop":now,
        "monthly":False,
    },     
    {
        "table":"dia_venda",
        "db_origin":"analytics",
        "db_target":"analytics",
        "dt_start":now,
        "dt_stop":now,
        "monthly":False,
    },        
    {
        "table":"qtd_ciclo",
        "db_origin":"analytics",
        "db_target":"analytics",
        "dt_start":now,
        "dt_stop":now,
        "monthly":False,
    },  
]

for s in steps:
    exec_query(**s)