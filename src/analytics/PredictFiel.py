#%%
import pandas as pd
import sqlalchemy
import mlflow
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]  # src/analytics -> src -> raiz
DB_PATH = ROOT_DIR / "data" / "analytics" / "database.db"
OUT_PATH = ROOT_DIR / "data" / "processed" / "top10_fieis.parquet"


def DBPredict():
    con = sqlalchemy.create_engine(f"sqlite:///{DB_PATH.as_posix()}")
    mlflow.set_tracking_uri("http://localhost:5000")

    versions = mlflow.search_model_versions(filter_string="name='model_fiel'")
    last_version = max(int(i.version) for i in versions)

    model = mlflow.sklearn.load_model(f"models:///model_fiel/{last_version}")

    data = pd.read_sql(
        "SELECT * FROM fs_all WHERE descLifeCycleFoto = '03-TURISTA'",
        con
    )

    data["predictFiel"] = model.predict_proba(data[model.feature_names_in_])[:, 1]

    data_output = data[["dtRef", "IdCliente", "predictFiel"]].copy()
    data_output["predictFiel"] = (f'{round((data_output["predictFiel"] * 100),2)}%')

    return data_output


def follow():
    con = sqlalchemy.create_engine(f"sqlite:///{DB_PATH.as_posix()}")
    return pd.read_sql("SELECT * FROM clients", con)


def info_flw():
    d = DBPredict()
    f = follow()

    df = d.merge(f, on="IdCliente", how="left")
    df = df.sort_values("predictFiel", ascending=False).head(10)

    return df


if __name__ == "__main__":
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = info_flw()
    df.to_parquet(OUT_PATH, index=False)
    print(f"[OK] Gerado: {OUT_PATH}")
