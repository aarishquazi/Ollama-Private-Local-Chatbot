import ollama

class OllamaManager:
    def __init__(self, default_model: str = "llama3"):
        self.client = ollama.Client()
        self.available_models = []
        self.current_model = default_model
        self.refresh_models()
        if self.current_model not in self.available_models:
            self.download_model(self.current_model)

    def refresh_models(self):
        try:
            models = self.client.list()
            self.available_models = [m['name'] for m in models.get('models', [])]
        except Exception:
            self.available_models = []

    def download_model(self, model_name: str) -> bool:
        try:
            self.client.pull(model_name)
            self.refresh_models()
            return True
        except Exception:
            return False

    def get_response(self, prompt: str, model: str = None) -> str:
        model = model or self.current_model
        try:
            response = self.client.generate(model=model, prompt=prompt, stream=False)
            return response.get('response', 'No response returned.')
        except Exception as e:
            return f"Error: {e}"
