class Quiz:
    def __init__(self, question, choices, answer):
        if (len(choices) != 4):
            raise ValueError(f"선택지는 반드시 4개여야합니다. 현재 {len(choices)}개")
        self.question = question
        self.choices = choices
        self.answer = answer

    def show_quiz(self):
        text = f"{self.question}\n"
        for i, choice in enumerate(self.choices, 1):
            text += f"{i}. {choice}\n"
        return text

    def check_answers(self, user_input):
        return True if user_input == self.answer else False
