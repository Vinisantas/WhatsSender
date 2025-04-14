import pandas as pd

class ContactModel:
    def __init__(self):
        self.contacts = []

    def load_contacts_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path, dtype=str, encoding='utf-8')
            if 'name' in df.columns and 'numero' in df.columns and 'valor' in df.columns:
                self.contacts = df.to_dict(orient='records')
                return True, "✅ Contatos carregados!"
            else:
                return False, "⚠️ CSV inválido! Precisa ter colunas 'name' , 'numero' e 'valor'."
        except Exception as e:
            return False, f"⚠️ Erro ao carregar CSV: {e}"

    def get_contacts(self):
        return self.contacts