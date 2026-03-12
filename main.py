import sys
import json
import random
import requests
import html

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QRadioButton,
)

from untitled import Ui_MainWindow


# ==========================
# API CLASS
# ==========================

class DataRequest:

    def __init__(self):

        self.category = {
            "Any": None,
            "General": 9,
            "Books": 10,
            "Film": 11,
            "Music": 12,
            "Science": 17,
            "Math": 19,
            "Computers": 18,
        }

        self.difficulty = {
            "Any": None,
            "easy": "easy",
            "medium": "medium",
            "hard": "hard",
        }

        self.type = {
            "Any": None,
            "MCQ": "multiple",
            "True/False": "boolean",
        }

    def get_questions(
        self,
        amount,
        category,
        difficulty,
        qtype,
    ):

        url = f"https://opentdb.com/api.php?amount={amount}"

        if category:
            url += f"&category={category}"

        if difficulty:
            url += f"&difficulty={difficulty}"

        if qtype:
            url += f"&type={qtype}"

        try:

            r = requests.get(url, timeout=10)
            data = r.json()

            if data["response_code"] != 0:
                return []

            result = []

            for q in data["results"]:

                question = html.unescape(q["question"])

                answers = (
                    q["incorrect_answers"]
                    + [q["correct_answer"]]
                )

                answers = [
                    html.unescape(a)
                    for a in answers
                ]

                random.shuffle(answers)

                correct = answers.index(
                    html.unescape(
                        q["correct_answer"]
                    )
                )

                result.append(
                    {
                        "question": question,
                        "answers": answers,
                        "correct": correct,
                        "category": q["category"],
                        "difficulty": q["difficulty"],
                    }
                )

            return result

        except:
            return []


# ==========================
# MAIN WINDOW
# ==========================

class QuizApp(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.api = DataRequest()

        self.questions = []
        self.current_index = 0
        self.score = 0

        self.radio_buttons = []

        self.setup_combobox()

        self.ui.btnFetch.clicked.connect(
            self.generate_quiz
        )

        self.ui.pushButton.clicked.connect(
            self.retry
        )

        self.ui.btnCheck.clicked.connect(
            self.check_answer
        )

        self.ui.btnNext.clicked.connect(
            self.next_question
        )

    # ======================
    # COMBOBOX
    # ======================

    def setup_combobox(self):

        self.ui.comboBox.addItems(
            self.api.category.keys()
        )

        self.ui.comboBox_2.addItems(
            self.api.difficulty.keys()
        )

        self.ui.comboBox_3.addItems(
            self.api.type.keys()
        )

    # ======================
    # GENERATE QUIZ
    # ======================

    def generate_quiz(self):

        subject = self.ui.comboBox.currentText()
        difficulty = self.ui.comboBox_2.currentText()
        qtype = self.ui.comboBox_3.currentText()

        amount = self.ui.spinBox.value()

        category_id = self.api.category[subject]
        diff_id = self.api.difficulty[difficulty]
        type_id = self.api.type[qtype]

        self.questions = self.api.get_questions(
            amount,
            category_id,
            diff_id,
            type_id,
        )

        if not self.questions:

            QMessageBox.warning(
                self,
                "Error",
                "Không lấy được câu hỏi",
            )
            return

        self.current_index = 0
        self.score = 0

        self.show_question()

        self.ui.toolBox.setCurrentIndex(1)

    # ======================
    # SHOW QUESTION
    # ======================

    def show_question(self):

        q = self.questions[
            self.current_index
        ]

        self.ui.plainTextEdit.setPlainText(
            q["question"]
        )

        # category + difficulty

        self.ui.lineEdit.setText(
            q["category"]
        )

        self.ui.lineEdit_2.setText(
            q["difficulty"]
        )

        # count

        total = len(self.questions)

        self.ui.question_count_label.setText(
            f"{self.current_index+1}/{total}"
        )

        # answers

        layout = (
            self.ui.answer_frame.layout()
        )

        # XÓA RADIO CŨ

        for i in reversed(
            range(layout.count())
        ):

            widget = layout.itemAt(i).widget()

            if widget:
                widget.setParent(None)

        self.radio_buttons = []

        for ans in q["answers"]:

            rb = QRadioButton(ans)

            layout.addWidget(rb)

            self.radio_buttons.append(rb)

    # ======================
    # GET SELECTED
    # ======================

    def get_selected(self):

        for i, rb in enumerate(
            self.radio_buttons
        ):

            if rb.isChecked():
                return i

        return None

    # ======================
    # CHECK
    # ======================

    def check_answer(self):

        selected = self.get_selected()

        if selected is None:

            QMessageBox.warning(
                self,
                "Warning",
                "Chưa chọn đáp án",
            )

            return

        correct = self.questions[
            self.current_index
        ]["correct"]

        if selected == correct:

            self.score += 1

            QMessageBox.information(
                self,
                "Result",
                "Đúng",
            )

        else:

            QMessageBox.information(
                self,
                "Result",
                "Sai",
            )

    # ======================
    # NEXT
    # ======================

    def next_question(self):

        self.current_index += 1

        if (
            self.current_index
            >= len(self.questions)
        ):

            QMessageBox.information(
                self,
                "Finish",
                f"Score {self.score}/{len(self.questions)}",
            )

            self.save_result()

            self.ui.toolBox.setCurrentIndex(0)

            return

        self.show_question()

    # ======================
    # RETRY
    # ======================

    def retry(self):

        self.show_question()

    # ======================
    # SAVE RESULT
    # ======================

    def save_result(self):

        data = {
            "score": self.score,
            "total": len(self.questions),
        }

        with open(
            "result.json",
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )


# ==========================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = QuizApp()
    window.show()

    sys.exit(app.exec())