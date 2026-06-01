class EvaluatorAgent:

    def calculate_score(
        self,
        answers,
        correct_answers
    ):

        score = 0

        for a, b in zip(
            answers,
            correct_answers
        ):
            if a == b:
                score += 1

        return score