import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def grafico_itens_monitorados(df):
    data2 = df.groupby("CONSOLIDADO UNIDADE")["QTD ITENS MONITORADOS - 1º trimestre"].sum()

    data2 = pd.to_numeric(data2, errors='coerce')

    data2 = data2.dropna()

    fig, ax = plt.subplots(figsize=(7, 3.5))
    if len(data2) == 0:
        ax.text(0.5, 0.5, 'Sem dados numéricos para exibir!', ha='center', va='center')
    else:
        ax.pie(
            data2.values,
            labels=data2.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Blues(np.linspace(0.5, 1, len(data2)))
        )
        ax.axis('equal')
    fig.tight_layout()
    return fig