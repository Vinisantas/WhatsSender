import requests

<<<<<<< HEAD
VERSION_URL = "https://raw.githubusercontent.com/Vinisantas/WhatsSender/main/version.txt"

=======
VERSION_URL = "https://github.com/Vinisantas/WhatsSender/raw/refs/heads/main/version.txt"
>>>>>>> 69b8bec16fdcf81a9345fbb476d4ad677bce8ed8

def get_local_version():
    """Lê a versão local do arquivo version.txt."""
    try:
        with open("version.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "0.0.0"  # Retorna uma versão padrão se o arquivo não existir

def get_remote_version():
    """Obtém a versão mais recente do GitHub."""
    try:
        response = requests.get(VERSION_URL) 
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"⚠️ Não foi possível acessar a versão remota. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao verificar a versão remota: {e}")
        return None

def check_for_updates():
    """Compara a versão local com a remota e retorna o status."""
    local_version = get_local_version()
    remote_version = get_remote_version()

    if remote_version and remote_version != local_version:
        print(f"⚠️ Atualização disponível! Versão atual: {local_version}, Nova versão: {remote_version}")
        return True, remote_version
    elif remote_version == local_version:
        print("✅ Você já está usando a versão mais recente.")
        return False, None
    else:
        print("⚠️ Não foi possível verificar atualizações.")
        return False, None
