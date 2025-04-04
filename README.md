# WhatsSender

WhatsSender é um aplicativo desenvolvido em Python para envio em massa de mensagens personalizadas no WhatsApp. Ele permite automatizar o envio de mensagens para múltiplos contatos, com suporte a personalização de texto, envio de imagens e integração com arquivos CSV para gerenciamento de contatos.

## Funcionalidades

- **Envio em Massa**: Envie mensagens para vários contatos de forma automatizada.
- **Personalização de Mensagens**: Use placeholders como `{nome}` para personalizar as mensagens com base nos contatos.
- **Envio de Imagens**: Anexe imagens às mensagens enviadas.
- **Importação de Contatos**: Carregue contatos a partir de arquivos CSV.
- **Interface Gráfica**: Interface amigável desenvolvida com PyQt6.
- **Automação com WhatsApp Web**: Integração com o WhatsApp Web para envio automático.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **PyQt6**: Para a criação da interface gráfica.
- **PyWhatKit**: Para automação do envio de mensagens no WhatsApp.
- **Pyperclip**: Para copiar mensagens e imagens para a área de transferência.
- **Pandas**: Para manipulação de arquivos CSV.
- **PyAutoGUI**: Para automação de interações no WhatsApp Web.

## Como Funciona

1. **Carregue os Contatos**:
   - Prepare um arquivo CSV com os contatos no seguinte formato:
     ```csv
     name,numero
     João,+5511999999999
     Maria,+5511988888888
     ```
   - Use o botão "Carregar Contatos" para importar o arquivo.

2. **Escreva a Mensagem**:
   - Digite a mensagem no campo de texto. Use `{nome}` para personalizar a mensagem com o nome do contato.
   - Exemplo:
     ```
     Olá {nome}, tudo bem? Esta é uma mensagem personalizada!
     ```

3. **Selecione uma Imagem (Opcional)**:
   - Escolha uma imagem para enviar junto com a mensagem.

4. **Envie as Mensagens**:
   - Clique no botão "Enviar Mensagens" para iniciar o envio.
   - O aplicativo abrirá o WhatsApp Web e enviará as mensagens automaticamente.

## Requisitos

- **Python 3.8 ou superior**
- **Bibliotecas Python**:
  - PyQt6
  - PyWhatKit
  - Pyperclip
  - Pandas
  - PyAutoGUI

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/WhatsSender.git
   cd WhatsSender


   ![alt text](image.png)

2. Instale as dependências:

pip install -r requirements.txt

3. Execute o aplicativo:

python whats_sender.py




## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.


## Licença
Este projeto está licenciado sob a MIT License.

## Capturas de Tela

![image](https://github.com/user-attachments/assets/1c013d41-2357-49e4-9c45-9c5bdb0e4ef1)


Autor
Desenvolvido por Vinícius Santana.
Entre em contato: viniciuspereirasantana@gmail.com
