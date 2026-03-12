import json
import datetime
import os

def save_result(self):

    result = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": self.score,
        "total": len(self.questions)
    }

    try:

        with open("results.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    except:
        data = []

    data.append(result)

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)