import pandas as pd
import os

def csv_to_markdown_processos(csv_file, output_file):
    try:
        df = pd.read_csv(
            csv_file,
            delimiter=',',
            on_bad_lines='skip',
            encoding='utf-8'
        )
    except pd.errors.ParserError as e:
        raise ValueError(f"Erro ao processar o arquivo CSV: {e}")

    expected_columns = [
        "Macroprocessos",
        "Processos",
        "Subprocessos"
    ]
    for col in expected_columns:
        if col not in df.columns:
            raise ValueError(f"O arquivo CSV não contém a coluna esperada: '{col}'.")

    grouped_macro = df.groupby("Macroprocessos")
    
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write("# Diagnóstico - Macroprocessos, Processos e Subprocessos\n\n")
        md_file.write("Este documento contém os dados extraídos do CSV de macroprocessos, processos e subprocessos.\n\n")
        for macro, macro_df in grouped_macro:
            md_file.write(f"## Macroprocesso: {macro}\n\n")
            grouped_proc = macro_df.groupby("Processos")
            for proc, proc_df in grouped_proc:
                md_file.write(f"### Processo: {proc}\n\n")
                subprocessos = proc_df["Subprocessos"].dropna().unique()
                for sub in subprocessos:
                    md_file.write(f"- {sub}\n")
                md_file.write("\n")
            md_file.write("---\n\n")
        print(f"✅ Arquivo Markdown gerado com sucesso: {output_file}")

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    csv_file = os.path.join(current_dir, "documentation", "processos.csv")
    output_file = os.path.join(current_dir, "processos_markdown.md")
    csv_to_markdown_processos(csv_file, output_file)