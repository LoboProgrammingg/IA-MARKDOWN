import json
from passlib.context import CryptContext
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE_IN = os.path.join(BASE_DIR, "user.json")
USERS_FILE_OUT = os.path.join(BASE_DIR, "user_hashed.json")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def convert_passwords():

    print("Iniciando a conversão de senhas...")

    if not os.path.exists(USERS_FILE_IN):
        print(f"ERRO: Arquivo de entrada '{USERS_FILE_IN}' não encontrado. Certifique-se de que ele está na mesma pasta que este script.")
        return

    try:
        with open(USERS_FILE_IN, "r", encoding="utf-8") as f:
            users_data = json.load(f)
        print(f"Sucesso: {len(users_data)} usuários carregados de '{USERS_FILE_IN}'.")
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERRO: Falha ao ler ou decodificar o arquivo JSON. Detalhes: {e}")
        return

    new_users_data = {}
    converted_count = 0
    for username, details in users_data.items():
        new_user_details = details.copy()
        
        if "password" in details and isinstance(details["password"], str):
            plain_password = details["password"]
            
            hashed_password = pwd_context.hash(plain_password)
            
            del new_user_details["password"]
            
            new_user_details["password_hash"] = hashed_password
            
            print(f"  - Senha para o usuário '{username}' convertida para hash.")
            converted_count += 1
        elif "password_hash" in details:
            print(f"  - Usuário '{username}' já parece ter um hash. Mantendo o existente.")
        else:
            print(f"  - AVISO: Usuário '{username}' não possui campo 'password'. Pulando.")
        
        new_users_data[username] = new_user_details

    try:
        with open(USERS_FILE_OUT, "w", encoding="utf-8") as f:
            json.dump(new_users_data, f, indent=4, ensure_ascii=False)
        print("\nConversão concluída com sucesso!")
        print(f"{converted_count} senhas foram convertidas.")
        print(f"--> Um novo arquivo foi criado: '{USERS_FILE_OUT}'")
        print("\nPRÓXIMOS PASSOS:")
        print("1. Exclua ou renomeie seu antigo arquivo 'user.json'.")
        print("2. Renomeie o novo arquivo 'user_hashed.json' para 'user.json'.")
        print("3. Execute seu ChatBot.py novamente. O login agora funcionará perfeitamente.")

    except IOError as e:
        print(f"ERRO: Falha ao salvar o novo arquivo JSON. Detalhes: {e}")


if __name__ == "__main__":
    convert_passwords()
