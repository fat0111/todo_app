from core.config import db
from schemas.todo import TodoCreate
from datetime import datetime

def create_new_todo(user_id: str, todo_data: TodoCreate):
    doc_ref = db.collection("todos").document()

    data_to_save = todo_data.model_dump() 
    data_to_save["user_id"] = user_id
    data_to_save["completed"] = False 
    data_to_save["created_at"] = datetime.now().isoformat()
    doc_ref.set(data_to_save)
    return doc_ref.id

def get_all_todos(user_id: str):
    docs = db.collection("todos").where("user_id", "==", user_id).stream()
    
    todo_list = []
    for doc in docs:
        todo_data = doc.to_dict()
        todo_data["id"] = doc.id 
        todo_list.append(todo_data)
        
    todo_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
    return todo_list

def delete_todo(user_id: str, todo_id: str):
    doc_ref = db.collection("todos").document(todo_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise Exception("Không tìm thấy công việc")
        
    if doc.to_dict().get("user_id") != user_id:
        raise Exception("Bạn không có quyền xóa công việc này")
        
    doc_ref.delete()
    return True

def toggle_todo_status(user_id: str, todo_id: str):
    doc_ref = db.collection("todos").document(todo_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise Exception("Không tìm thấy công việc")
        
    data = doc.to_dict()
    if data.get("user_id") != user_id:
        raise Exception("Bạn không có quyền sửa công việc này")
        
    new_status = not data.get("completed", False)
    doc_ref.update({"completed": new_status})
    return new_status

def update_todo(user_id: str, todo_id: str, update_data: dict):
    doc_ref = db.collection("todos").document(todo_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise Exception("Không tìm thấy công việc")
        
    if doc.to_dict().get("user_id") != user_id:
        raise Exception("Bạn không có quyền sửa công việc này")
        
    doc_ref.update({
        "title": update_data.get("title"),
        "description": update_data.get("description")
    })
    return True