class DifficultyAgent:

    def build_instruction(
        self,
        difficulty
    ):

        if difficulty == "Easy":
            return (
                "Generate simple "
                "definition-based questions."
            )

        if difficulty == "Medium":
            return (
                "Generate conceptual "
                "questions."
            )

        return (
            "Generate analytical "
            "and scenario-based questions."
        )