# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QTableWidget
)
from PyQt6.QtGui import QFont, QIcon
from utils.constants import APP_TITLE, ICON_PATH, WINDOW_HEIGHT, WINDOW_WIDTH


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))  # Define o ícone da janela
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("background-color: #FFFFFF; color: #333333;")

        self.layout = QVBoxLayout()

        self.label = QLabel('Mensagem personalizada:')
        self.label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #D40000;")
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Digite a mensagem aqui. Use {nome} para personalizar o nome e {valor} para acessar o valor.")
        self.text_edit.setStyleSheet("background-color: #F9F9F9; color: #333333; border: 1px solid #D40000;")
        self.layout.addWidget(self.text_edit)

        self.btn_load = QPushButton('Carregar Contatos (CSV)')
        self.btn_load.setStyleSheet("background-color: #D40000; color: white; border-radius: 5px;")
        self.layout.addWidget(self.btn_load)

        self.table = QTableWidget()
        self.table.setStyleSheet("background-color: #F9F9F9; color: #333333; border: 1px solid #D40000;")
        self.layout.addWidget(self.table)

        self.btn_image = QPushButton('Escolher Imagem')
        self.btn_image.setStyleSheet("background-color: #D40000; color: white; border-radius: 5px;")
        self.layout.addWidget(self.btn_image)

        self.image_label = QLabel('Nenhuma imagem selecionada')
        self.image_label.setStyleSheet("color: #333333;")
        self.layout.addWidget(self.image_label)

        self.btn_send = QPushButton('Enviar Mensagens')
        self.btn_send.setStyleSheet("background-color: #D40000; color: white; border-radius: 5px;")
        self.layout.addWidget(self.btn_send)

        self.status_label = QLabel('Status: Aguardando ação...')
        self.status_label.setStyleSheet("color: #333333;")
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)