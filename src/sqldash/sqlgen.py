TABLES = {"revenue": 'SELECT region, SUM(revenue) FROM orders GROUP BY region', "tickets": 'SELECT status, COUNT(*) FROM tickets GROUP BY status'}
FORBIDDEN = ("drop", "delete", "update", "insert", "alter")


class InputError(ValueError):
    pass


def generate(question):
    if not isinstance(question, str) or not question.strip():
        raise InputError("question is empty")
    lowered = question.lower()
    if any(word in lowered for word in FORBIDDEN):
        raise InputError("write statements are refused")
    for needle, sql in TABLES.items():
        if needle in lowered:
            return {"sql": sql, "read_only": True}
    raise InputError("no table mapping for that question")
