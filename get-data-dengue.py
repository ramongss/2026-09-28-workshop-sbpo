import pandas as pd
from pyarrow import dataset as ds
# from pysus.online_data.SINAN import download
from tqdm import tqdm

# # baixa dados de dengue do SINAN de 2015 a 2026
# files = download(
#     diseases="DENG", years=[year for year in range(2015, 2027, 1)]
# )

root = "/home/ramon/pysus"
files = [f"{root}/DENGBR{yy}.parquet" for yy in range(15, 27, 1)]


ibge_to_uf = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
    "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA",
    "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
    "41": "PR", "42": "SC", "43": "RS",
    "50": "MS", "51": "MT", "52": "GO", "53": "DF"
}

uf_to_regiao = {
    "RO": "Norte", "AC": "Norte", "AM": "Norte", "RR": "Norte",
    "PA": "Norte", "AP": "Norte", "TO": "Norte",
    "MA": "Nordeste", "PI": "Nordeste", "CE": "Nordeste", "RN": "Nordeste",
    "PB": "Nordeste", "PE": "Nordeste", "AL": "Nordeste", "SE": "Nordeste", "BA": "Nordeste",
    "MT": "Centro-Oeste", "MS": "Centro-Oeste", "GO": "Centro-Oeste", "DF": "Centro-Oeste",
    "MG": "Sudeste", "ES": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "SC": "Sul", "RS": "Sul"
}

resultados = []
for file in tqdm(files):
    # le parquet dataset
    dataset = ds.dataset(file, format="parquet")
    # df = pd.read_parquet(file, engine='pyarrow')

    table = dataset.to_table(columns=["DT_NOTIFIC", "SG_UF_NOT"])
    df = table.to_pandas()

    # transforma colunas em lowercase
    df.columns = [col.lower() for col in df.columns]
    
    # transforma data
    df['dt_notific'] = pd.to_datetime(df['dt_notific'], format='%Y%m%d')
    
    df['sem_epi'] = df['dt_notific'].dt.isocalendar().week
    df['ano_epi'] = df['dt_notific'].dt.isocalendar().year
    df['data_epi'] = pd.to_datetime(
        df['ano_epi'].astype(str) + "-W" + df['sem_epi'].astype(str) + "-7",
        format="%G-W%V-%u",
    )
    df = df[df.sem_epi <= 52]

    # formata coluna uf
    df['sg_uf_not'] = df['sg_uf_not'].str.upper()
    df["uf"] = df["sg_uf_not"].map(ibge_to_uf).fillna(df["sg_uf_not"])

    # agrupa por sigla_estado e semana epidemiológica
    df = (
        df
        .groupby(['uf', 'ano_epi', 'sem_epi', 'data_epi'])
        .size()
        .reset_index(name='casos')
    )

    # renomeia ibge para uf
    df["regiao"] = df["uf"].map(uf_to_regiao)

    # append casos
    resultados.append(df)

# concat dfs    
df_total = pd.concat(resultados, ignore_index=True)
df_total['pais'] = 'Brasil'

# salva df
df_total.to_csv('data-dengue.csv', index=False)