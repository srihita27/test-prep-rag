import pandas as pd

class StudentAgent:

    def __init__(self):
        self.students = pd.read_csv(
            "database/students.csv"
        )

        self.performance = pd.read_csv(
            "database/performance.csv"
        )

    def get_student(self, student_id):

        row = self.students[
            self.students.student_id == student_id
        ]

        return row.iloc[0].to_dict()

    def get_weak_topics(
        self,
        student_id,
        subject
    ):

        filtered = self.performance[
            (self.performance.student_id == student_id)
            &
            (self.performance.subject == subject)
        ]

        weak = filtered[
            filtered.score < 50
        ]

        return weak.topic.tolist()

    def suggest_difficulty(
        self,
        student_id
    ):

        row = self.students[
            self.students.student_id == student_id
        ]

        avg = row.iloc[0]["avg_score"]

        if avg < 50:
            return "Easy"
        elif avg < 75:
            return "Medium"

        return "Hard"