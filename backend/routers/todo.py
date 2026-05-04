from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.todo import TodoCreate, TodoResponse
from services.todo_services import create_new_todo, get_all_todos, delete_todo
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@router.post("/", response_model=str)
def add_todo(
    todo: TodoCreate, 
    user_id: str = Depends(get_current_user)
):
    try:
        task_id = create_new_todo(user_id, todo)
        return task_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TodoResponse])
def read_todos(user_id: str = Depends(get_current_user)): 
    return get_all_todos(user_id)

@router.delete("/{todo_id}")
def remove_todo(todo_id: str, user_id: str = Depends(get_current_user)):
    try:
        delete_todo(user_id, todo_id)
        return {"message": "Đã xóa công việc thành công"}
    except Exception as e:
        if str(e) == "Không tìm thấy công việc":
            raise HTTPException(status_code=404, detail=str(e))
        elif str(e) == "Bạn không có quyền xóa công việc này":
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{todo_id}/toggle")
def toggle_todo(todo_id: str, user_id: str = Depends(get_current_user)):
    try:
        from services.todo_services import toggle_todo_status
        new_status = toggle_todo_status(user_id, todo_id)
        return {"message": "Đã cập nhật", "completed": new_status}
    except Exception as e:
        if str(e) == "Không tìm thấy công việc":
            raise HTTPException(status_code=404, detail=str(e))
        elif str(e) == "Bạn không có quyền sửa công việc này":
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{todo_id}")
def edit_todo(todo_id: str, todo: TodoCreate, user_id: str = Depends(get_current_user)):
    try:
        from services.todo_services import update_todo
        update_todo(user_id, todo_id, todo.model_dump())
        return {"message": "Đã cập nhật thành công"}
    except Exception as e:
        if str(e) == "Không tìm thấy công việc":
            raise HTTPException(status_code=404, detail=str(e))
        elif str(e) == "Bạn không có quyền sửa công việc này":
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))