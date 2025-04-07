import requests
import zipfile
import os

DOWNLOAD_URL = "https://github.com/Vinisantas/WhatsSender/archive/refs/heads/main.zip"

def download_update():
    """Faz o download da nova versão do GitHub."""
    try:
        response = requests.get(DOWNLOAD_URL, stream=True)
        if response.status_code == 200:
            with open("update.zip", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print("✅ Atualização baixada com sucesso!")
            return True
        else:
            print(f"⚠️ Não foi possível baixar a atualização. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro ao baixar a atualização: {e}")
        return False

def extract_update():
    """Extrai o arquivo update.zip e substitui os arquivos antigos."""
    try:
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        print("✅ Atualização extraída com sucesso!")
        os.remove("update.zip")  # Remove o arquivo zip após a extração
        return True
    except Exception as e:
        print(f"Erro ao extrair a atualização: {e}")
        return False