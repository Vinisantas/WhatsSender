import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PyQt6.QtWidgets import QApplication, QMessageBox
from controller.main_controller import MainController
from updater.version_manager import check_for_updates
from updater.downloader import download_update, extract_update
from utils.constants import DEFAULT_TIME_BETWEEN_MESSAGES
import pygetwindow as gw
import time

def get_version_file_path():
    """Retorna o caminho absoluto do arquivo version.txt."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.txt")

def get_local_version():
    """Lê a versão local do arquivo version.txt."""
    try:
        with open(get_version_file_path(), "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("⚠️ Arquivo version.txt não encontrado. Usando versão padrão 0.0.0.")
        return "0.0.0"  # Retorna uma versão padrão se o arquivo não existir
    except Exception as e:
        print(f"Erro ao ler o arquivo version.txt: {e}")
        return "0.0.0"

def update_local_version(new_version):
    """Atualiza o arquivo version.txt com a nova versão."""
    try:
        with open(get_version_file_path(), "w") as file:
            file.write(new_version)
        print(f"✅ Versão local atualizada para {new_version}")
    except Exception as e:
        print(f"Erro ao atualizar a versão local: {e}")

def show_error_message(title, message):
    """Exibe uma mensagem de erro e registra no log."""
    print(f"❌ {title}: {message}")
    QMessageBox.critical(None, title, message)

def process_update_step(step_function, error_message):
    """Executa uma etapa do processo de atualização e exibe uma mensagem de erro em caso de falha."""
    try:
        if not step_function():
            show_error_message("Erro na Atualização", error_message)
            return False
        return True
    except Exception as e:
        show_error_message("Erro na Atualização", f"{error_message}: {e}")
        return False

def handle_update():
    """Gerencia o processo de atualização."""
    try:
        update_available, new_version = check_for_updates()
        if update_available:
            reply = QMessageBox.question(
                None,
                "Atualização Disponível",
                f"Uma nova versão ({new_version}) está disponível! Deseja baixar e instalar agora?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if download_update() and extract_update():
                    QMessageBox.information(None, "Atualização", "Atualização concluída com sucesso! Reinicie o aplicativo.")
                    sys.exit(0)
                else:
                    QMessageBox.critical(None, "Erro", "Falha ao atualizar o aplicativo.")
    except Exception as e:
        print(f"Erro ao verificar atualizações: {e}")
        QMessageBox.critical(None, "Erro", f"Erro ao verificar atualizações: {e}")

def focus_whatsapp_web():
    """Garante que a janela do WhatsApp Web esteja em foco."""
    try:
        # Procura por uma janela com "WhatsApp" no título
        whatsapp_window = next(win for win in gw.getAllTitles() if "WhatsApp" in win)
        window = gw.getWindowsWithTitle(whatsapp_window)[0]
        window.activate()  # Traz a janela para o foco
        time.sleep(0.5)  # Pequeno atraso para garantir que o foco seja aplicado
    except StopIteration:
        print("❌ Janela do WhatsApp Web não encontrada.")
    except Exception as e:
        print(f"Erro ao focar na janela do WhatsApp Web: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Verificar atualizações antes de iniciar o aplicativo
    handle_update()

    # Iniciar o controlador principal
    controller = MainController()
    controller.view.show()

    sys.exit(app.exec())