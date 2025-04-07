import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from controller.main_controller import MainController
from updater.version_manager import check_for_updates
from updater.downloader import download_update, extract_update

def handle_update():
    """Gerencia o processo de atualização."""
    update_available, new_version = check_for_updates()
    if update_available:
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
                    sys.exit()  # Fecha o aplicativo para reiniciar
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

if __name__ == '__main__':
    # Criar a instância do QApplication
    app = QApplication(sys.argv)

    # Verificar e gerenciar atualizações
    handle_update()

    # Iniciar o aplicativo
    controller = MainController()
    controller.view.show()
    sys.exit(app.exec())