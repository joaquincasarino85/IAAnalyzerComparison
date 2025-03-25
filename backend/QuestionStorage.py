class QuestionStorage:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.questions = []  # Se inicializa una única vez
        return cls._instance  # Siempre devuelve la misma instancia

    def save_question(self, question):
        self.questions.append(question)

    def get_history(self):
        return self.questions
