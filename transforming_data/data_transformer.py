import pandas as pd
import csv
import os

def csv_to_markdown(csv_file, output_file):
    try:
        df = pd.read_csv(
            csv_file,
            delimiter=',',
            quoting=csv.QUOTE_MINIMAL,
            on_bad_lines='skip',
            encoding='utf-8'
        )
    except pd.errors.ParserError as e:
        raise ValueError(f"Erro ao processar o arquivo CSV: {e}")

    with open(output_file, "w", encoding="utf-8") as md_file:
        for unidade, unidade_group in df.groupby("Unidade"):
            md_file.write(f"## Unidade: {unidade}\n\n")
            
            for diretoria, diretoria_group in unidade_group.groupby("Diretoria"):
                md_file.write(f"### Diretoria: {diretoria}\n\n")
                
                for objetivo, objetivo_group in diretoria_group.groupby("Objetivo Estratégico"):
                    md_file.write(f"### Objetivo Estratégico: {objetivo}\n\n")
                    
                    for perspectiva, perspectiva_group in objetivo_group.groupby("Perspectiva"):
                        md_file.write(f"#### Perspectiva: {perspectiva}\n\n")
                        
                        for _, row in perspectiva_group.iterrows():
                            iniciativa = row["Iniciativa"]
                            if "Risco Estratégico" in iniciativa:
                                md_file.write(f"- **Risco Estratégico**: {iniciativa}\n")
                            else:
                                md_file.write(f"- **Iniciativa**: {iniciativa}\n")
                        md_file.write("\n")
                md_file.write("\n")
            md_file.write("\n")

current_dir = os.path.dirname(__file__)
csv_file = os.path.join(current_dir, "documentation", "dados.csv")
output_file = os.path.join(current_dir, "dados.md")

csv_to_markdown(csv_file, output_file)
print(f"Arquivo Markdown gerado com sucesso: {output_file}")