import zipfile
import os
import sys

def create_update_zip(output_filename="update.zip", base_dir="."):
    """Cria um arquivo ZIP contendo todos os arquivos necessários para a atualização."""
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Exclua o script de empacotamento e o arquivo ZIP anterior, se existirem
                if file_path != os.path.abspath(__file__) and file_path != os.path.abspath(output_filename):
                    zipf.write(file_path, os.path.relpath(file_path, base_dir))

if __name__ == "__main__":
    print("Criando update.zip...")
    # Adapte 'base_dir' para o diretório raiz da sua aplicação.
    # Se o seu 'main.py' está na raiz, você pode usar "."
    # Se os seus arquivos buildados estão em uma pasta específica (ex: 'dist'), use "dist"
    base_dir_to_zip = "."
    create_update_zip(base_dir=base_dir_to_zip)
    print("update.zip criado com sucesso!")