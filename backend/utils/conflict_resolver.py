def resolve_conflicts(existing_note, new_data):
    if existing_note.timestamp > new_data['timestamp']:
        return {"title": existing_note.title, "content": existing_note.content}
    elif existing_note.timestamp < new_data['timestamp']:
        return {"title": new_data['title'], "content": new_data['content']}
    else:
        return {
            "title": new_data['title'],
            "content": f"{existing_note.content}\n{new_data['content']}"
        }