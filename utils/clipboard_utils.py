from PIL import Image
from io import BytesIO
import win32clipboard

def copy_image_to_clipboard(image_path):
    """Copia uma imagem para a área de transferência."""
    try:
        image = Image.open(image_path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # Remove o cabeçalho do BMP

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        print(f"✅ Imagem copiada para a área de transferência: {image_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao copiar imagem para a área de transferência: {e}")
        return False

