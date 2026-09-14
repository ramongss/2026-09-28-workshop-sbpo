# 2026-sbpo-workshop

Workshop de previsão de séries temporais epidemiológicas usando dados do SINAN (DATASUS).

## Conteúdo

- `get-data-dengue.py` / `arruma-dataset-dengue.py` — baixa e trata dados de dengue → `data-dengue.csv`
- `get-chik-data.py` / `arruma-dataset-chick.py` — baixa e trata dados de chikungunya → `chik.csv`
- `forecast-dengue.py` / `forecast-dengue.ipynb` — previsão hierárquica (StatsForecast, MLForecast) e reconciliação

## Uso

```bash
uv sync
uv run python get-data-dengue.py
uv run python arruma-dataset-dengue.py
uv run python forecast-dengue.py
```

Os dados brutos são baixados via [pysus](https://github.com/AlertaDengue/PySUS) e cacheados em `~/pysus`.

## Licença

MIT — veja [LICENSE](LICENSE).
