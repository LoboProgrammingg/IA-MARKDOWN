import matplotlib.pyplot as plt
import numpy as np

def grafico_indicadores(df_indicador, meses, indicador_nome, meta, resultado_acumulado, figsize=(8, 3.5)):
    """
    Gera um gráfico de barras dos valores mensais do indicador,
    mostra a meta e o resultado acumulado no título.
    """
    # Limpeza dos valores mensais para float, mesmo que venham como "85,75%" ou "85.75"
    valores_mensais = []
    for v in df_indicador[meses]:
        if isinstance(v, str):
            v_clean = v.replace('%', '').replace(',', '.').strip()
        else:
            v_clean = v
        try:
            valores_mensais.append(float(v_clean))
        except:
            valores_mensais.append(np.nan)
    fig, ax = plt.subplots(figsize=figsize, dpi=120)
    bars = ax.bar(meses, valores_mensais, color="#4da3ff", edgecolor="#003366", alpha=0.86)
    ax.set_ylabel("Valor", color="#003366", fontsize=12, weight="bold")
    ax.set_title(
        f'{indicador_nome}\nMeta 2025: {meta} | Resultado Acumulado: {resultado_acumulado}',
        fontsize=13, color="#001f3f", weight='bold', loc='center'
    )
    ax.tick_params(axis='x', rotation=45)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        if not np.isnan(height):
            ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, color="#003366", fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#003366")
    ax.spines['bottom'].set_color("#003366")
    ax.set_facecolor("#e6f1fb")
    fig.patch.set_facecolor("#e6f1fb")
    fig.tight_layout(pad=1)
    return fig