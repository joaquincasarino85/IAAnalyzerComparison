from datetime import datetime

class Question:
    def __init__(self, text: str):
        self.text = text
        self.date = datetime.now()

    def get_text(self) -> str:
        return self.text

    def __str__(self):
        return f"[{self.date}] {self.text}"
