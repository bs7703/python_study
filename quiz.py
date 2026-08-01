class Quiz:
    def __init__(self, question, choices, answer, hint = None, explanation = None, answer_score = None):
        if (len(choices) != 4):
            raise ValueError(f"선택지는 반드시 4개여야합니다. 현재 {len(choices)}개")
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint
        self.explanation = explanation
        self.answer_score = answer_score
    def show_quiz(self):
        text = f"{self.question}\n"
        for i, choice in enumerate(self.choices, 1):
            text += f"{i}. {choice}\n"
        return text

    def show_hint(self):
        return self.hint if self.hint is not None else "힌트가 없습니다"

    def get_explanation(self):
        return f" 해설: {self.explanation}" if self.explanation else "해설이 없습니다."

    def check_answers(self, user_input):
        return (user_input == self.answer) * self.answer_score
