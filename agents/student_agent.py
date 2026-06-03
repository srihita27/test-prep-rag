import pandas as pd


class StudentAgent:

    def __init__(self):

        self.students = pd.read_csv(
            "database/students.csv"
        )

    def get_student(
        self,
        student_id
    ):

        row = self.students[
            self.students.student_id
            == student_id
        ]

        return row.iloc[0].to_dict()

    def get_all_students(self):

        return self.students[
            ["student_id", "name"]
        ].to_dict("records")

    def enroll_student(
        self,
        name
    ):

        new_id = (
            self.students.student_id.max()
            + 1
        )

        new_row = {
            "student_id": new_id,
            "name": name,
            "avg_score": 0
        }

        self.students.loc[
            len(self.students)
        ] = new_row

        self.students.to_csv(
            "database/students.csv",
            index=False
        )

        return new_id

    def get_weak_topics(
        self,
        student_id,
        subject
    ):

        try:

            perf = pd.read_csv(
                "database/performance.csv"
            )

            filtered = perf[
                (perf.student_id == student_id)
                &
                (perf.subject == subject)
            ]

            weak = filtered[
                filtered.score < 50
            ]

            return weak.topic.tolist()

        except:

            return []

    def suggest_difficulty(
        self,
        student_id
    ):

        row = self.students[
            self.students.student_id
            == student_id
        ]

        avg = row.iloc[0]["avg_score"]

        if avg < 50:
            return "Easy"

        elif avg < 75:
            return "Medium"

        return "Hard"