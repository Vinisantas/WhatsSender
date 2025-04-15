import requests
import zipfile
import os
import shutil  # Import para operações de arquivo mais avançadas

DOWNLOAD_URL = "https://github.com/Vinisantas/WhatsSender/releases/latest/download/update.zip"


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
    """Extrai o arquivo update.zip e tenta substituir os arquivos antigos."""
    update_dir = "update_temp"  # Cria um diretório temporário para extração
    try:
        os.makedirs(update_dir, exist_ok=True)
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall(update_dir)
        print(f"✅ Atualização extraída para {update_dir}")

        # Agora vamos substituir os arquivos
        current_dir = os.getcwd()
        updated_files_count = 0
        for item_name in os.listdir(update_dir):
            source_path = os.path.join(update_dir, item_name)
            dest_path = os.path.join(current_dir, item_name)

            try:
                if os.path.isfile(source_path):
                    if os.path.exists(dest_path):
                        os.remove(dest_path)  # Remove o arquivo antigo
                    shutil.copy2(source_path, dest_path)  # Copia o novo arquivo (mantém metadados)
                    updated_files_count += 1
                    print(f"🔄 Substituído arquivo: {item_name}")
                elif os.path.isdir(source_path):
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)  # Remove o diretório antigo
                    shutil.copytree(source_path, dest_path)  # Copia o novo diretório
                    print(f"🔄 Substituído diretório: {item_name}")
            except Exception as e:
                print(f"⚠️ Erro ao substituir {item_name}: {e}")

        print(f"✅ {updated_files_count} arquivos/diretórios atualizados.")
        os.remove("update.zip")  # Remove o arquivo zip após a extração
        shutil.rmtree(update_dir)  # Remove o diretório temporário
        return True

    except zipfile.BadZipFile:
        print("❌ Erro ao extrair a atualização: Arquivo ZIP inválido.")
        if os.path.exists("update.zip"):
            os.remove("update.zip")
        if os.path.exists(update_dir):
            shutil.rmtree(update_dir)
        return False
    except Exception as e:
        print(f"❌ Erro ao extrair a atualização: {e}")
        if os.path.exists("update.zip"):
            os.remove("update.zip")
        if os.path.exists(update_dir):
            shutil.rmtree(update_dir)
        return False