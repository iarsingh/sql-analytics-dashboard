import re

TABLES = {"revenue": "SELECT region, SUM(revenue) FROM orders GROUP BY region", "tickets": "SELECT status, COUNT(*) FROM tickets GROUP BY status"}
FORBIDDEN = {"drop", "delete", "update", "insert", "alter"}


class InputError(ValueError):
    pass


def generate(question):
    if not isinstance(question, str) or not question.strip() or len(question) > 2000:
        raise InputError("question must contain 1 to 2000 characters")
    tokens = set(re.findall(r"[a-z]+", question.lower()))
    if tokens & FORBIDDEN:
        raise InputError("write statements are refused")
    matches = [name for name in TABLES if name in tokens]
    if len(matches) > 1:
        raise InputError("ambiguous question: choose revenue or tickets")
    if not matches:
        raise InputError("no table mapping: choose revenue or tickets")
    name = matches[0]
    return {"sql": TABLES[name], "read_only": True, "template": name, "executed": False}
