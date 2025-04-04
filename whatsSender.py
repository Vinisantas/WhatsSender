# -*- coding: utf-8 -*-

import sys
import pandas as pd
import pywhatkit as kit
import time
import pyautogui
import win32clipboard
import pyperclip
from PIL import Image
from io import BytesIO
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class WhatsAppSender(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.contacts = []
        self.image_path = None  

    def initUI(self):
        self.setWindowTitle('WhatsApp Sender - Instituto Mix')
        self.resize(550, 600)
        self.setStyleSheet("background-color: #FFFFFF; color: #333333;")  # Fundo branco, texto cinza escuro

        layout = QVBoxLayout()

        self.label = QLabel('Mensagem personalizada:')
        self.label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #D40000;")  # Texto vermelho
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Digite a mensagem aqui. Use {nome} para personalizar.")
        self.text_edit.setStyleSheet("background-color: #F9F9F9; color: #333333; border: 1px solid #D40000;")
        layout.addWidget(self.text_edit)

        self.btn_load = QPushButton('Carregar Contatos (CSV)')
        self.btn_load.setStyleSheet("background-color: #D40000; color: white; border-radius: 5px;")
        self.btn_load.clicked.connect(self.load_csv)
        layout.addWidget(self.btn_load)

        self.table = QTableWidget()
        self.table.setStyleSheet("background-color: #F9F9F9; color: #333333; border: 1px solid #D40000;")
        layout.addWidget(self.table)

        self.btn_image = QPushButton('Escolher Imagem')
        self.btn_image.setStyleSheet("background-color: #D40000; color: white; border-radius: 5px;")
        self.btn_image.clicked.connect(self.select_image)
        layout.addWidget(self.btn_image)

        self.image_label = QLabel('Nenhuma imagem selecionada')
        self.image_label.setStyleSheet("color: #333333;")
        layout.addWidget(self.image_label)

        self.btn_send = QPushButton('Enviar Mensagens')
        self.btn_send.setStyleSheet("background-color: #D40000; color: white; border-radius: 5px;")
        self.btn_send.clicked.connect(self.send_messages)
        layout.addWidget(self.btn_send)

        self.status_label = QLabel('Status: Aguardando ação...')
        self.status_label.setStyleSheet("color: #333333;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Abrir Arquivo CSV', '', 'CSV Files (*.csv)')
        if file_path:
            df = pd.read_csv(file_path, dtype=str , encoding='utf-8')
            if 'name' in df.columns and 'numero' in df.columns:
                self.contacts = df.to_dict(orient='records')
                self.update_table()
                self.status_label.setText('✅ Contatos carregados!')
            else:
                self.status_label.setText('⚠️ CSV inválido! Precisa ter colunas "name" e "numero".')

    def update_table(self):
        self.table.setRowCount(len(self.contacts))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Nome', 'Número'])
        for row, contact in enumerate(self.contacts):
            self.table.setItem(row, 0, QTableWidgetItem(contact['name']))
            self.table.setItem(row, 1, QTableWidgetItem(str(contact['numero'])))

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecionar Imagem', '', 'Imagens (*.png *.jpg *.jpeg *.bmp)')
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(200, 200))
            self.status_label.setText(f'✅ Imagem carregada!')

    def copy_image_to_clipboard(self, image_path):
        try:
            image = Image.open(image_path)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            return True
        except Exception as e:
            self.status_label.setText(f'⚠️ Erro ao copiar imagem: {e}')
            return False

    def send_messages(self):
        if not self.contacts:
            self.status_label.setText('⚠️ Nenhum contato carregado!')
            return

        message_template = self.text_edit.toPlainText()
        if not message_template:
            self.status_label.setText('⚠️ Mensagem vazia!')
            return

        if not self.image_path:
            self.status_label.setText('⚠️ Nenhuma imagem selecionada!')
            return

        for contact in self.contacts:
            nome = contact['name']
            numero = str(contact['numero']).strip()

            # Corrigir número para incluir o código do Brasil
            if not numero.startswith('+55'):
                numero = '+55' + numero

            # Personalizar a mensagem
            mensagem = message_template.replace('{nome}', nome)

            try:
                self.status_label.setText(f'📤 Enviando para {nome}...')
                
                # Enviar mensagem inicial para abrir o chat no WhatsApp
                kit.sendwhatmsg_instantly(numero, "", wait_time=10, tab_close=False)
                time.sleep(5)

                # Copiar a imagem para a área de transferência
                if not self.copy_image_to_clipboard(self.image_path):
                    self.status_label.setText(f'⚠️ Erro ao copiar imagem para {nome}!')
                    continue

                pyautogui.hotkey("ctrl", "v")  # Cola a imagem
                time.sleep(2)

                # Limpar a área de transferência e copiar a mensagem
                pyperclip.copy("")  # Limpa a área de transferência
                pyperclip.copy(mensagem)  # Copia a mensagem personalizada
                pyautogui.hotkey("ctrl", "v")  # Cola a mensagem
                pyautogui.press("enter")  # Envia a mensagem
                self.status_label.setText(f'✅ Enviado para {nome} ({numero})')
            except Exception as e:
                self.status_label.setText(f'❌ Erro ao enviar para {nome}: {e}')
            
            time.sleep(10)  # Espera entre mensagens

        self.status_label.setText('✅ Todas as mensagens foram enviadas!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WhatsAppSender()
    window.show()
    sys.exit(app.exec())
