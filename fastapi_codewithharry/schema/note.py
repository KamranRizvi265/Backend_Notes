def noteEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "description": item["description"],
        "important": item["important"]
    }

def notesEntity(items: list[dict]) -> list:
    return [noteEntity(item) for item in items]