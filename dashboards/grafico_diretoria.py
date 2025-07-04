import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def gerar_grafico_unidades_por_diretoria(
    df_completo, 
    diretoria_selecionada,
    coluna_diretoria_principal="DIR", 
    coluna_unidade="CONSOLIDADO UNIDADE", 
    coluna_iniciativas="Nº INICIATIVAS", 
    theme_colors=None, 
    figsize=(12, 8)
):
    if theme_colors is None:
        theme_colors = {
            'PRIMARY': "#00529B", 'SECONDARY': "#0078D4", 'ACCENT': "#00A9E0",
            'BACKGROUND': "#0A192F", 'TEXT_PRIMARY': "#FFFFFF", 
            'TEXT_SECONDARY': "#E0E0E0", 'TEXT_TERTIARY': "#A0AEC0",
            'BORDER_LIGHT': "#4A5568", 'SUCCESS': "#38A169",
            'CHART_BACKGROUND': "#0A192F", 'CHART_AXES_FACE': "#1A2B44",
        }

    df_diretoria = df_completo[df_completo[coluna_diretoria_principal] == diretoria_selecionada].copy()

    if df_diretoria.empty:
        fig, ax = plt.subplots(figsize=figsize, dpi=120)
        fig.patch.set_facecolor(theme_colors.get('CHART_BACKGROUND', '#0A192F'))
        ax.set_facecolor(theme_colors.get('CHART_AXES_FACE', '#102A4C'))
        ax.text(0.5, 0.5, f"Não há dados de iniciativas para\na Diretoria: {diretoria_selecionada}",
                horizontalalignment='center', verticalalignment='center',
                fontsize=14, color=theme_colors.get('TEXT_TERTIARY', '#A0AEC0'), transform=ax.transAxes,
                linespacing=1.5)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(theme_colors.get('BORDER_LIGHT', '#4A5568'))
        return fig

    iniciativas_por_unidade = df_diretoria.groupby(coluna_unidade, as_index=False)[coluna_iniciativas].sum()
    
    total_iniciativas_diretoria = iniciativas_por_unidade[coluna_iniciativas].sum()

    plot_data = iniciativas_por_unidade.sort_values(by=coluna_iniciativas, ascending=True)
    
    total_label = "Total"
    total_row = pd.DataFrame([{coluna_unidade: total_label, coluna_iniciativas: total_iniciativas_diretoria}])
    
    plot_data = pd.concat([plot_data, total_row], ignore_index=True)
    
    if plot_data.empty or (len(plot_data) == 1 and plot_data.iloc[0][coluna_unidade] == total_label and plot_data.iloc[0][coluna_iniciativas] == 0):
        fig, ax = plt.subplots(figsize=figsize, dpi=120)
        fig.patch.set_facecolor(theme_colors.get('CHART_BACKGROUND', '#0A192F'))
        ax.set_facecolor(theme_colors.get('CHART_AXES_FACE', '#102A4C'))
        ax.text(0.5, 0.5, f"Sem iniciativas agregadas para\na Diretoria: {diretoria_selecionada}",
                horizontalalignment='center', verticalalignment='center',
                fontsize=14, color=theme_colors.get('TEXT_TERTIARY', '#A0AEC0'), transform=ax.transAxes,
                linespacing=1.5)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(theme_colors.get('BORDER_LIGHT', '#4A5568'))
        return fig

    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    fig.patch.set_facecolor(theme_colors.get('CHART_BACKGROUND', '#0A192F'))
    ax.set_facecolor(theme_colors.get('CHART_AXES_FACE', '#1A2B44'))

    num_bars = len(plot_data)
    bar_palette = [theme_colors.get('ACCENT', '#00A9E0'), 
                   theme_colors.get('SECONDARY', '#0078D4'), 
                   theme_colors.get('PRIMARY', '#00529B'),
                   theme_colors.get('ACCENT_LIGHT', '#71C5E8')]
    
    colors_for_bars = [bar_palette[i % len(bar_palette)] for i in range(num_bars -1)] 
    colors_for_bars.append(theme_colors.get('SUCCESS', '#38A169'))

    bars = ax.barh(plot_data[coluna_unidade], plot_data[coluna_iniciativas], 
                   color=colors_for_bars, 
                   edgecolor=theme_colors.get('BACKGROUND_ALT', '#102A4C'), 
                   height=0.7, zorder=3, linewidth=1.5)

    for i, bar in enumerate(bars):
        width = bar.get_width()
        is_total_bar = (plot_data[coluna_unidade].iloc[i] == total_label)
        label_color = theme_colors.get('TEXT_PRIMARY', '#FFFFFF') if is_total_bar else theme_colors.get('TEXT_SECONDARY', '#E0E0E0')
        font_weight = 'bold' if is_total_bar else 'normal'
        font_size = 11 if is_total_bar else 9
        
        ax.text(width + (ax.get_xlim()[1] * 0.015), 
                bar.get_y() + bar.get_height() / 2,
                f'{width:.0f}', 
                ha='left', va='center',
                color=label_color, fontsize=font_size, fontweight=font_weight, zorder=4)

    ax.set_xlabel("Número de Iniciativas", fontsize=13, color=theme_colors.get('TEXT_SECONDARY', '#E0E0E0'), labelpad=12, weight="bold")
    ax.set_ylabel("Unidade Consolidada", fontsize=13, color=theme_colors.get('TEXT_SECONDARY', '#E0E0E0'), labelpad=12, weight="bold")
    
    chart_title = f"Iniciativas por Unidade da Diretoria: {diretoria_selecionada}"
    ax.set_title(chart_title, fontsize=18, color=theme_colors.get('TEXT_PRIMARY', '#FFFFFF'), loc='center', fontweight='bold', pad=25)

    ax.tick_params(axis='x', colors=theme_colors.get('TEXT_TERTIARY', '#A0AEC0'), labelsize=11)
    ax.tick_params(axis='y', colors=theme_colors.get('TEXT_TERTIARY', '#A0AEC0'), labelsize=11, length=0)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(theme_colors.get('BORDER_LIGHT', '#4A5568'))
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_color(theme_colors.get('BORDER_LIGHT', '#4A5568'))
    ax.spines['bottom'].set_linewidth(1.5)

    ax.grid(axis='x', linestyle=':', alpha=0.25, color=theme_colors.get('BORDER_LIGHT', '#4A5568'), zorder=0)
    ax.axvline(0, color=theme_colors.get('BORDER_LIGHT', '#4A5568'), linewidth=1, zorder=1)
    
    max_val = plot_data[coluna_iniciativas].max()
    ax.set_xlim(0, max_val * 1.20)

    fig.tight_layout(pad=2)
    return fig

if __name__ == '__main__':
    sample_theme_colors = {
        'PRIMARY': "#00529B", 'SECONDARY': "#0078D4", 'ACCENT': "#00A9E0", 
        'ACCENT_LIGHT': "#71C5E8", 'BACKGROUND': "#0A192F", 'BACKGROUND_ALT': "#102A4C",
        'CARD_BG': "#1A2B44", 'CHART_BACKGROUND': "#0A192F", 'CHART_AXES_FACE': "#1A2B44",
        'TEXT_PRIMARY': "#FFFFFF", 'TEXT_SECONDARY': "#E0E0E0", 'TEXT_TERTIARY': "#A0AEC0",
        'BORDER_LIGHT': "#4A5568", 'SUCCESS': "#38A169"
    }
    
    example_data = {
        'DIR': ['DAFI', 'DIRC', 'DTIC', 'GADP', 'DAFI', 'DTIC', 'DIRC', 'GADP', 'DTIC', 'DAFI', 'DAFI', 'DIRC', 'DTIC', 'GADP', 'DAFI'],
        'Nº INICIATIVAS': [5, 8, 12, 3, 7, 13, 10, 5, 10, 6, 4, 9, 11, 2, 10],
        'CONSOLIDADO UNIDADE': ['UGOFF', 'UGVEN', 'UGSTI', 'UGGOV', 'UGPES', 'UGITI', 'UGEPV', 'UGPRO', 'UGSDG', 'UGACO', 'UGOFF', 'UGVEN', 'UGITI', 'UGGOV', 'UGADM']
    }
    df_exemplo = pd.DataFrame(example_data)

    fig1 = gerar_grafico_unidades_por_diretoria(df_exemplo, "DAFI", 
                                                coluna_diretoria_principal="DIR",
                                                coluna_unidade="CONSOLIDADO UNIDADE", 
                                                coluna_iniciativas="Nº INICIATIVAS", 
                                                theme_colors=sample_theme_colors)


    fig2 = gerar_grafico_unidades_por_diretoria(df_exemplo, "DTIC", 
                                                coluna_diretoria_principal="DIR",
                                                coluna_unidade="CONSOLIDADO UNIDADE", 
                                                coluna_iniciativas="Nº INICIATIVAS", 
                                                theme_colors=sample_theme_colors)
