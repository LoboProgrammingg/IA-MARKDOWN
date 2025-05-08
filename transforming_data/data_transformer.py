import pandas as pd
import os

def csv_to_markdown(csv_file, output_file):
    try:
        df = pd.read_csv(
            csv_file,
            delimiter=',',
            on_bad_lines='skip',
            encoding='utf-8'
        )
    except pd.errors.ParserError as e:
        raise ValueError(f"Erro ao processar o arquivo CSV: {e}")
    
    if not {"CRITERIO VALOR PUBLICO", "PRATICAS DE GESTAO"}.issubset(df.columns):
        raise ValueError("O arquivo CSV não contém as colunas esperadas: 'CRITERIOS DE GOVERNANCA' e 'PRATICAS DE GESTAO'.")

    with open(output_file, "w", encoding="utf-8") as md_file:
        for _, row in df.iterrows():
            criterio = row["CRITERIO VALOR PUBLICO"]
            pratica = row["PRATICAS DE GESTAO"]

            if pd.isna(pratica) or pratica.strip() == "":
                pratica = "Não há informações disponíveis sobre esta prática de gestão."

            md_file.write(f"## CRITÉRIO: {criterio}\n\n")
            md_file.write(f"### PRÁTICA DE GESTÃO:\n{pratica}\n\n")
        
        print(f"✅ Arquivo Markdown gerado com sucesso: {output_file}")

current_dir = os.path.dirname(__file__)
csv_file = os.path.join(current_dir, "documentation", "teste6.csv")
output_file = os.path.join(current_dir, "dados.md")

csv_to_markdown(csv_file, output_file)