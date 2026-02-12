import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox
)

# Directory base corretta per build frozen
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "ai_settings.json")


class AIConfigurator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Configurator")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Provider
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["ollama", "openai", "groq", "together", "hugging", "mlvoca"])
        provider_layout.addWidget(self.provider_combo)
        layout.addLayout(provider_layout)

        # Modello
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Modello:"))
        self.model_combo = QComboBox()
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)

        self.provider_models = {
            "ollama": ["llama3", "llama2"],
            "openai": ["gpt-4", "gpt-4-32k", "gpt-3.5-turbo"],
            "together": ["Inserisci modello disponibile sul tuo account"],
            "groq": ["Inserisci modello disponibile sul tuo account"],
            "hugging": ["mistralai/Mistral-7B-Instruct-v0.2"],
            "mlvoca": ["tinyllama"]
        }

        self.provider_combo.currentTextChanged.connect(self.update_models)

        # API Key
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("API Key:"))
        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.Password)
        key_layout.addWidget(self.key_edit)
        layout.addLayout(key_layout)

        # URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Endpoint URL:"))
        self.url_edit = QLineEdit()
        url_layout.addWidget(self.url_edit)
        layout.addLayout(url_layout)

        # Bottone salva
        self.save_button = QPushButton("Salva impostazioni")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.load_settings()
        self.update_models()

    def update_models(self):
        provider = self.provider_combo.currentText()
        self.model_combo.clear()

        if provider in ["hugging", "mlvoca"]:
            # Modello fisso
            self.model_combo.addItem(self.provider_models[provider][0])
            self.model_combo.setCurrentText(self.provider_models[provider][0])
            self.model_combo.setDisabled(True)

            # Blocca URL e key
            self.url_edit.setText(
                "https://router.huggingface.co/v1/chat/completions" if provider == "hugging" else "https://mlvoca.com/api/generate"
            )
            self.url_edit.setDisabled(True)
            self.key_edit.setDisabled(True)
        else:
            # Provider generici
            self.model_combo.addItems(self.provider_models.get(provider, []))
            self.model_combo.setDisabled(False)
            self.url_edit.setDisabled(False)
            self.key_edit.setDisabled(False)

        # Mantieni modello salvato se esiste
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
                saved_model = config.get("model", "")
                if saved_model in self.provider_models.get(provider, []):
                    self.model_combo.setCurrentText(saved_model)
            except Exception:
                pass

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.provider_combo.setCurrentText(config.get("provider", "ollama"))
                self.key_edit.setText(config.get("api_key", ""))
                self.url_edit.setText(config.get("url", ""))
            except Exception:
                pass
        else:
            self.provider_combo.setCurrentText("ollama")
            self.model_combo.setCurrentText(self.provider_models["ollama"][0])
            self.url_edit.setText("http://localhost:11434/api/chat")
            self.key_edit.setText("")

    def save_settings(self):
        provider = self.provider_combo.currentText().strip()
        model = self.model_combo.currentText().strip()
        url = self.url_edit.text().strip().replace("\n", "")

        if provider == "hugging":
            model = "mistralai/Mistral-7B-Instruct-v0.2"
            url = "https://router.huggingface.co/v1/chat/completions"
            config = {"provider": provider, "model": model, "url": url}
        elif provider == "mlvoca":
            model = "tinyllama"
            url = "https://mlvoca.com/api/generate"
            config = {"provider": provider, "model": model, "url": url}
        else:
            api_key = self.key_edit.text().strip()
            if not model:
                models = self.provider_models.get(provider, [])
                if models:
                    model = models[0]
            config = {"provider": provider, "model": model, "api_key": api_key, "url": url}

        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            QMessageBox.information(self, "Successo", "Impostazioni salvate correttamente!")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIConfigurator()
    window.show()
    sys.exit(app.exec())
