import pandas as pd
import matplotlib.pyplot as plt

notas = pd.read_csv("ml-latest-small/ratings.csv")
notas.columns = ["usuarioId", "filmeId", "nota", "momento"]

res = notas['nota'].unique() #valores unicos das notas
res = notas['nota'].value_counts() # quantidade por nota
# res = notas.nota.plot()

print(res)