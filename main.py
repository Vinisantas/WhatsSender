import sys
import requests
import zipfile
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from controller.main_controller import MainController

# URLs do GitHub
VERSION_URL = "https://raw.githubusercontent.com/Vinisantas/WhatsSender/main/version.txt"
DOWNLOAD_URL = "https://github.com/Vinisantas/WhatsSender/archive/refs/heads/main.zip"

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

def check_for_updates():
    """Compara a versão local com a remota e notifica o usuário."""
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

if __name__ == '__main__':
    # Criar a instância do QApplication
    app = QApplication(sys.argv)

    # Verificar atualizações antes de iniciar o aplicativo
    update_available, new_version = check_for_updates()
    if update_available:
        # Exibir uma mensagem para o usuário
        reply = QMessageBox.question(
            None,
            "Atualização Disponível",
            f"Uma nova versão ({new_version}) está disponível! Deseja baixar e instalar agora?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if download_update():
                if extract_update():
                    QMessageBox.information(
                        None,
                        "Atualização Concluída",
                        "A atualização foi instalada com sucesso! Reinicie o aplicativo para aplicar as mudanças."
                    )
                    sys.exit()  # Fecha o aplicativo para que o usuário possa reiniciá-lo
                else:
                    QMessageBox.critical(
                        None,
                        "Erro na Atualização",
                        "Não foi possível extrair a atualização."
                    )
            else:
                QMessageBox.critical(
                    None,
                    "Erro no Download",
                    "Não foi possível baixar a atualização."
                )

    # Iniciar o aplicativo
    controller = MainController()
    controller.view.show()
    sys.exit(app.exec())