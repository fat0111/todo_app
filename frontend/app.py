import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(override=True)

BACKEND_URL = "http://localhost:8000"

FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")

st.set_page_config(page_title="To-Do App", page_icon="📝", layout="centered")

st.markdown("""
<style>
    /* Ẩn Header, Menu (dấu ba chấm) và nút Deploy */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}

    /* Giao diện tổng thể */
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        margin-bottom: 30px;
    }
    
    /* Card cho công việc */
    .todo-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out;
        border-left: 5px solid #3498db;
    }
    
    .todo-card:hover {
        transform: translateY(-5px);
    }
    
    .todo-title {
        color: #2c3e50;
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .todo-desc {
        color: #7f8c8d;
        font-size: 0.95rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-pending {
        background-color: #f39c12;
        color: white;
    }
    
    .status-completed {
        background-color: #2ecc71;
        color: white;
    }

</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📝 To-Do App</h1>", unsafe_allow_html=True)


if "token" in st.query_params:
    st.session_state.token = st.query_params["token"]
    st.query_params.clear()

if "token" not in st.session_state:
    st.session_state.token = None


if not st.session_state.token:
    st.markdown("### 🔑 Đăng nhập / Đăng ký")
    
    if not FIREBASE_WEB_API_KEY:
        st.warning("⚠️ Vui lòng cập nhật `FIREBASE_WEB_API_KEY` trong file `.env` để sử dụng tính năng xác thực bằng Firebase.")
    
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mật khẩu", type="password", key="login_pass")
        if st.button("Đăng nhập", use_container_width=True, type="primary"):
            if FIREBASE_WEB_API_KEY:
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
                payload = {"email": email, "password": password, "returnSecureToken": True}
                res = requests.post(url, json=payload)
                if res.status_code == 200:
                    st.session_state.token = res.json()["idToken"]
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Sai email hoặc mật khẩu!")
            else:
                st.error("Chưa cấu hình API Key.")
                
        st.markdown("---")
        st.markdown("<p style='text-align: center;'>Hoặc</p>", unsafe_allow_html=True)
    

        st.link_button(
            "Đăng nhập bằng Google",
            "http://localhost:8000/auth/google/start",
            use_container_width=True
        )
                
    with tab2:
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Mật khẩu (ít nhất 6 ký tự)", type="password", key="reg_pass")
        if st.button("Đăng ký", use_container_width=True):
            if FIREBASE_WEB_API_KEY:
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
                payload = {"email": reg_email, "password": reg_password, "returnSecureToken": True}
                res = requests.post(url, json=payload)
                if res.status_code == 200:
                    st.session_state.token = res.json()["idToken"]
                    st.success("Đăng ký thành công!")
                    st.rerun()
                else:
                    st.error("Lỗi đăng ký: " + res.json().get("error", {}).get("message", "Unknown error"))
            else:
                st.error("Chưa cấu hình API Key.")

else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    @st.cache_data(ttl=300, show_spinner=False)
    def fetch_user_info(token):
        try:
            res = requests.get(f"{BACKEND_URL}/auth/me", headers={"Authorization": f"Bearer {token}"})
            if res.status_code == 200:
                return res.json().get("email", "Người dùng")
        except:
            pass
        return "Người dùng"

    @st.cache_data(ttl=60, show_spinner=False)
    def fetch_todos(token):
        try:
            res = requests.get(f"{BACKEND_URL}/todos/", headers={"Authorization": f"Bearer {token}"})
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None

    user_email = fetch_user_info(st.session_state.token)
    st.markdown(f"**👤 Đang đăng nhập:** `{user_email}`")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 📋 Danh sách công việc của bạn")
    with col2:
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.token = None
            st.rerun()

    if "show_add" not in st.session_state:
        st.session_state.show_add = False

    if not st.session_state.show_add:
        if st.button("➕ Thêm công việc mới", use_container_width=True):
            st.session_state.show_add = True
            st.rerun()
    else:
        if st.button("➖ Đóng Form", use_container_width=True):
            st.session_state.show_add = False
            st.rerun()
            
        with st.form("add_todo"):
            title = st.text_input("Tiêu đề công việc", placeholder="Vd: Mua đồ ăn sáng...")
            description = st.text_area("Mô tả chi tiết", placeholder="Vd: Gồm bánh mì, trứng...")
            submitted = st.form_submit_button("Thêm ngay", type="primary")
            
            if submitted:
                if title:
                    res = requests.post(
                        f"{BACKEND_URL}/todos/", 
                        headers=headers, 
                        json={"title": title, "description": description}
                    )
                    if res.status_code == 200:
                        fetch_todos.clear()
                        st.session_state.show_add = False
                        st.rerun()
                    else:
                        st.error("Lỗi khi thêm công việc! " + str(res.text))
                else:
                    st.warning("Vui lòng nhập tiêu đề!")
                    
    st.divider()
    

    try:
        def toggle_todo(todo_id):
            requests.put(f"{BACKEND_URL}/todos/{todo_id}/toggle", headers=headers)
            fetch_todos.clear()
            
        todos = fetch_todos(st.session_state.token)
        if todos is not None:
            if len(todos) == 0:
                st.info("🎉 Bạn chưa có công việc nào. Hãy thêm công việc mới!")
            else:
                for t in todos:
                    is_completed = t.get('completed', False)
                    status_class = "status-completed" if is_completed else "status-pending"
                    status_text = "✅ Đã xong" if is_completed else "⏳ Chờ xử lý"
                    title_style = "text-decoration: line-through; color: #95a5a6;" if is_completed else ""
                    
                    created_at_str = t.get('created_at')
                    time_html = ""
                    if created_at_str:
                        try:
                            dt = datetime.fromisoformat(created_at_str)
                            time_html = f"<div style='font-size: 0.85rem; color: #95a5a6;'>🕒 {dt.strftime('%H:%M - %d/%m/%Y')}</div>"
                        except:
                            pass
                    
                    if st.session_state.get('edit_id') == t['id']:
                        with st.form(key=f"edit_form_{t['id']}"):
                            st.markdown("### ✏️ Chỉnh sửa công việc")
                            edit_title = st.text_input("Tiêu đề", value=t['title'])
                            edit_desc = st.text_area("Mô tả (kéo góc dưới để xem rộng hơn)", value=t.get('description') or '', height=200)
                            col_e1, col_e2 = st.columns(2)
                            if col_e1.form_submit_button("💾 Lưu lại", type="primary", use_container_width=True):
                                res = requests.put(
                                    f"{BACKEND_URL}/todos/{t['id']}", 
                                    headers=headers, 
                                    json={"title": edit_title, "description": edit_desc}
                                )
                                if res.status_code == 200:
                                    fetch_todos.clear()
                                    st.session_state.edit_id = None
                                    st.rerun()
                                else:
                                    st.error("Lỗi cập nhật: " + res.text)
                            if col_e2.form_submit_button("❌ Hủy", use_container_width=True):
                                st.session_state.edit_id = None
                                st.rerun()
                    else:
                        col1, col2, col3 = st.columns([0.5, 4.0, 1.5])
                        with col1:
    
                            st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)
                            st.checkbox(" ", value=is_completed, key=f"chk_{t['id']}", on_change=toggle_todo, args=(t['id'],))
                            
                        with col2:
                            html_content = f"""
<div class="todo-card">
    <h4 class="todo-title" style="{title_style}">{t['title']}</h4>
    <p class="todo-desc" style="{title_style}">{t.get('description') or '<i>Không có mô tả</i>'}</p>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
        <div class="{status_class} status-badge">{status_text}</div>
        {time_html}
    </div>
</div>
"""
                            st.markdown(html_content, unsafe_allow_html=True)
                        with col3:
                            
                            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                            if st.button("👁️ Xem / Sửa", key=f"edit_{t['id']}", use_container_width=True):
                                st.session_state.edit_id = t['id']
                                st.rerun()
                            if st.button("🗑️ Xóa", key=f"del_{t['id']}", use_container_width=True, type="secondary"):
                                del_res = requests.delete(f"{BACKEND_URL}/todos/{t['id']}", headers=headers)
                                if del_res.status_code == 200:
                                    fetch_todos.clear()
                                    st.rerun()
                                else:
                                    st.error("Lỗi xóa: " + del_res.text)
        elif res.status_code == 401:
            st.error(" Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.")
            st.session_state.token = None
            if st.button("Tải lại trang"):
                st.rerun()
        else:
            st.error(f"Lỗi khi tải danh sách: {res.status_code}")
    except Exception as e:
        st.error(f"Không thể kết nối đến server backend! Lỗi: {e}")
