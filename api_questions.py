import requests
import random
import html


def get_questions(amount=5):

    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"

    try:
        response = requests.get(url, timeout=10)

        data = response.json()

    except Exception as e:
        print("API ERROR:", e)
        return []

    # kiểm tra API có trả về đúng không
    if "results" not in data:
        print("API trả về lỗi:", data)
        return []

    questions = []

    for item in data["results"]:

        question = html.unescape(item["question"])

        correct = html.unescape(item["correct_answer"])

        incorrect = [
            html.unescape(x)
            for x in item["incorrect_answers"]
        ]

        answers = incorrect + [correct]

        random.shuffle(answers)

        questions.append(
            {
                "question": question,
                "answers": answers,
                "correct": correct,
            }
        )

    return questions