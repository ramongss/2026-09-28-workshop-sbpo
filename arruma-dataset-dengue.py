import pandas as pd

data = pd.read_csv('data-dengue.csv')
data['data_epi'] = pd.to_datetime(data['data_epi'])

# 1. Ordena por semana epidemiológica
data = data.sort_values(["uf", "ano_epi", "sem_epi"]).reset_index(drop=True)

# 2. Remove duplicatas de (uf, data_epi) somando os casos
uf_meta = data[["uf", "regiao", "pais"]].drop_duplicates()
data = data.groupby(["uf", "data_epi"], as_index=False)["casos"].sum()

# 3. Preenche semanas faltantes com ffill por UF
all_weeks = pd.date_range(data["data_epi"].min(), data["data_epi"].max(), freq="W-SUN")
filled = []
for uf, grp in data.groupby("uf"):
    grp = grp.set_index("data_epi").reindex(all_weeks)
    grp["casos"] = grp["casos"].ffill()
    grp["uf"] = uf
    filled.append(grp.reset_index().rename(columns={"index": "data_epi"}))

data = pd.concat(filled, ignore_index=True).merge(uf_meta, on="uf").dropna(subset=["casos"])

data.to_csv('data-dengue.csv', index=False)