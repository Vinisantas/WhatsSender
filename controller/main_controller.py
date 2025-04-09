# type: ignore
import sys
import os
import win32clipboard

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.contact_model import ContactModel
from views.main_view import MainView
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt6.QtGui import QPixmap
import pywhatkit as kit
import pyautogui
import pyperclip
import time


class MainController:
    def __init__(self):
        self.model = ContactModel()
        self.view = MainView()

        # Conectar os botões da visão às funções do controlador
        self.view.btn_load.clicked.connect(self.load_contacts)
        self.view.btn_image.clicked.connect(self.select_image)
        self.view.btn_send.clicked.connect(self.send_messages)
        self.image_path = None

    def load_contacts(self):
        """Carrega os contatos de um arquivo CSV."""
        file_path, _ = QFileDialog.getOpenFileName(self.view, 'Abrir Arquivo CSV', '', 'CSV Files (*.csv)')
        if file_path:
            success, message = self.model.load_contacts_from_csv(file_path)
            self.view.status_label.setText(message)
            if success:
                self.update_table()

    def update_table(self):
        """Atualiza a tabela de contatos na interface."""
        contacts = self.model.get_contacts()
        self.view.table.setRowCount(len(contacts))
        self.view.table.setColumnCount(3)
        self.view.table.setHorizontalHeaderLabels(['Nome', 'Número', 'Valor'])
        for row, contact in enumerate(contacts):
            self.view.table.setItem(row, 0, QTableWidgetItem(contact['name']))
            self.view.table.setItem(row, 1, QTableWidgetItem(contact['numero']))
            self.view.table.setItem(row, 2, QTableWidgetItem(contact.get('valor', '')))

    def select_image(self):
        """Seleciona uma imagem para enviar junto com as mensagens."""
        file_path, _ = QFileDialog.getOpenFileName(self.view, 'Selecionar Imagem', '', 'Imagens (*.png *.jpg *.jpeg *.bmp)')
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.view.image_label.setPixmap(pixmap.scaled(200, 200))
            self.view.status_label.setText('✅ Imagem carregada!')

    def send_messages(self):
        """Envia mensagens personalizadas para os contatos carregados."""
        if not self.model.get_contacts():
            self.view.status_label.setText('⚠️ Nenhum contato carregado!')
            return

        message_template = self.view.text_edit.toPlainText()
        if not message_template:
            self.view.status_label.setText('⚠️ Mensagem vazia!')
            return

        if not self.image_path:
            self.view.status_label.setText('⚠️ Nenhuma imagem selecionada!')
            return

        for contact in self.model.get_contacts():
            nome = contact['name']
            numero = str(contact['numero']).strip()
            valor = (contact['valor']) if 'valor' in contact else ''

            # Corrigir número para incluir o código do Brasil
            if not numero.startswith('+55'):
                numero = '+55' + numero

            # Personalizar a mensagem
            personalized_message = message_template.replace("{nome}", nome)
            personalized_message = personalized_message.replace("{valor}", valor)

            try:
                self.view.status_label.setText(f'📤 Enviando para {nome}...')
                
                # Enviar mensagem inicial para abrir o chat no WhatsApp
                kit.sendwhatmsg_instantly(numero, "", wait_time=30, tab_close=False)
                time.sleep(5)

                # Copiar a imagem para a área de transferência
                if not self.copy_image_to_clipboard(self.image_path):
                    self.view.status_label.setText(f'⚠️ Erro ao copiar imagem para {nome}!')
                    continue

                pyautogui.hotkey("ctrl", "v")  # Cola a imagem
                time.sleep(2)

                # Limpar a área de transferência e copiar a mensagem
                pyperclip.copy("")  # Limpa a área de transferência
                pyperclip.copy(personalized_message)  # Copia a mensagem personalizada
                pyautogui.hotkey("ctrl", "v")  # Cola a mensagem
                pyautogui.press("enter")  # Envia a mensagem
                self.view.status_label.setText(f'✅ Enviado para {nome} ({numero})')
            except Exception as e:
                self.view.status_label.setText(f'❌ Erro ao enviar para {nome}: {e}')
            
            time.sleep(10)  # Espera entre mensagens

        self.view.status_label.setText('✅ Todas as mensagens foram enviadas!')

    def copy_image_to_clipboard(self, image_path):
        """Copia uma imagem para a área de transferência."""
        try:
            from PIL import Image
            from io import BytesIO
            import win32clipboard

            image = Image.open(image_path)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]  # Remove o cabeçalho do BMP

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            return True
        except Exception as e:
            self.view.status_label.setText(f'⚠️ Erro ao copiar imagem: {e}')
            return False