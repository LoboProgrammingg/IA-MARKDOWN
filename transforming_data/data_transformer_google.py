from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import csv
import os

def download_xlsx_from_drive(file_id, output_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(output_path)

def xlsx_to_csv(xlsx_file, csv_file):
    df = pd.read_excel(xlsx_file, engine='openpyxl')
    df.to_csv(csv_file, index=False, encoding='utf-8')

def csv_to_markdown(csv_file, output_file):
    try:
        df = pd.read_csv(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, on_bad_lines='warn', encoding='utf-8')
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
                            if "Plano de Negócio" in iniciativa:
                                md_file.write(f'- **Plano de Negócio**: {iniciativa}\n')
                            else:
                                md_file.write(f"- **Iniciativa**: {iniciativa}\n")
                        md_file.write("\n")
                md_file.write("\n")
            md_file.write("\n")

current_dir = os.path.dirname(__file__)
documentation_dir = os.path.join(current_dir, "documentation")
xlsx_local_path = os.path.join(documentation_dir, "dados.xlsx")
csv_local_path = os.path.join(documentation_dir, "dados.csv")
output_md_path = os.path.join(documentation_dir, "dados.md")
file_id = "SEU_ARQUIVO_ID_AQUI"
os.makedirs(documentation_dir, exist_ok=True)
download_xlsx_from_drive(file_id, xlsx_local_path)
xlsx_to_csv(xlsx_local_path, csv_local_path)
csv_to_markdown(csv_local_path, output_md_path)