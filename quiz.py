class Quiz:
    def __init__(self, question, choices, answer, hint=None, explanation=None, answer_point=1):
        self.answer = answer
        self.answer_point = answer_point
        self.choices = choices
        self.explanation = explanation
        self.answer_point = answer_point
        self.question = question
        self.hint = hint
        
    def show_quiz(self):
        text = f"{self.question}\n"
        for i, choice in enumerate(self.choices, 1):
            text += f"{i}. {choice}\n"
        return text

    def check_answers(self, user_input):
        return self.answer_point if user_input == self.answer else -1 * self.answer_point

    def get_answer(self):
        return self.answer

    def get_explanation(self):
        return f" 해설: {self.explanation}" if not (self.explanation is None or self.explanation == "") else "해설이 없습니다."

    def show_hint(self):
        return self.hint if self.hint is not None and self.hint != "" else None

    def show_score(self):
        return self.answer_point