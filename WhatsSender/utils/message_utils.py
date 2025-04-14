def format_number(numero):
    """Adiciona o código do Brasil ao número, se necessário."""
    numero = str(numero).strip()
    if not numero.startswith('+55'):
        return '+55' + numero
    return numero

def personalize_message(template, nome, valor):
    """Substitui os placeholders na mensagem."""
    return template.replace("{nome}", nome).replace("{valor}", valor)