# type: ignore
import sys
import os
import win32clipboard
from PyQt6.QtGui import QFont

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap
import pywhatkit as kit
import pyautogui
import pyperclip
import time
from models.contact_model import ContactModel
from views.main_view import MainView
from utils.message_utils import format_number, personalize_message
from utils.clipboard_utils import copy_image_to_clipboard
from utils.constants import DEFAULT_TIME_BETWEEN_MESSAGES, CSV_FILE_FILTER, IMAGE_FILE_FILTER

# Configuração do log para registrar erros
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(message)s')

class MainController:
    def __init__(self):
        self.model = ContactModel()
        self.view = MainView()

        # Conectar os botões da visão às funções do controlador
        self.view.btn_load.clicked.connect(self.load_contacts)
        self.view.btn_image.clicked.connect(self.select_image)
        self.view.btn_send.clicked.connect(self.send_messages)

        self.image_path = None
        self.time_between = DEFAULT_TIME_BETWEEN_MESSAGES

    def load_contacts(self):
        """Carrega os contatos de um arquivo CSV."""
        file_path, _ = QFileDialog.getOpenFileName(self.view, 'Abrir Arquivo CSV', '', CSV_FILE_FILTER)
        if file_path:
            success, message = self.model.load_contacts_from_csv(file_path)
            if not success:
                QMessageBox.critical(self.view, "Erro", message)
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
        file_path, _ = QFileDialog.getOpenFileName(self.view, 'Selecionar Imagem', '', IMAGE_FILE_FILTER)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.view.image_label.setPixmap(pixmap.scaled(200, 200))
            self.view.status_label.setText('✅ Imagem carregada!')

    def timer_input(self):
        """Define o tempo entre os envios de mensagens."""
        try:
            time_between = int(self.view.timer_input.toPlainText())
            if time_between > 0:
                self.time_between = time_between
                self.view.timer_label.setText(f'Tempo definido: {time_between} segundos')
                self.view.status_label.setText('✅ Tempo definido!')
            else:
                raise ValueError("O tempo deve ser maior que 0.")
        except ValueError:
            self.view.timer_label.setText('⚠️ Tempo inválido! Usando valor padrão de 10 segundos.')
            self.time_between = 10  # Valor padrão

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
            numero = format_number(contact['numero'])
            valor = contact.get('valor', '')

            # Personalizar a mensagem
            personalized_message = personalize_message(message_template, nome, valor)

            try:
                self.view.status_label.setText(f'📤 Enviando para {nome}...')

                # Enviar mensagem inicial para abrir o chat no WhatsApp
                kit.sendwhatmsg_instantly(numero, "", wait_time=10, tab_close=False)
                time.sleep(5)

                # Copiar a imagem para a área de transferência
                if not copy_image_to_clipboard(self.image_path):
                    self.view.status_label.setText(f'⚠️ Erro ao copiar imagem para {nome}! Pulando...')
                    continue

                pyautogui.hotkey("ctrl", "v")  # Cola a imagem
                time.sleep(2)

                # Limpar a área de transferência e copiar a mensagem
                pyperclip.copy("")  # Limpa a área de transferência
                pyperclip.copy(personalized_message)  # Copia a mensagem personalizada
                pyautogui.hotkey("ctrl", "v")  # Cola a mensagem
                pyautogui.press("enter")  # Envia a mensagem
                self.view.status_label.setText(f'✅ Enviado para {nome} ({numero})')

                # Aguarda o tempo configurado entre mensagens
                print(f"Aguardando {self.time_between} segundos antes de enviar a próxima mensagem...")
                time.sleep(self.time_between)
            except Exception as e:
                error_message = f'❌ Erro ao enviar para {nome}: {e}'
                self.view.status_label.setText(error_message)
                logging.error(error_message)

        self.view.status_label.setText('✅ Todas as mensagens foram enviadas!')