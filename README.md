# 📝 To-Do App

## 👤 Thông tin sinh viên
- **Họ và tên:** Đinh Tiến Phát
- **MSSV:** 24120405
- **Lớp/Môn học:** Tư duy tính toán

## 🌟 Tên feature
- **Quản lý công việc (To-Do List) và Xác thực người dùng qua Google (OAuth 2.0)**

## 💡 Mô tả ngắn về chức năng của hệ thống
Hệ thống là một ứng dụng phân tán hoàn chỉnh bao gồm Backend (FastAPI) và Frontend (Streamlit), sử dụng cơ sở dữ liệu đám mây Firebase Firestore. Các chức năng cốt lõi bao gồm:
- **Xác thực:** Đăng nhập, đăng ký bằng Email/Password, hoặc đăng nhập một chạm qua Google (chuẩn Server-Side OAuth 2.0). Hệ thống cung cấp API kiểm tra Token để định danh người dùng một cách bảo mật.
- **Quản lý công việc (Feature chính):** Người dùng có thể thêm công việc mới, tải danh sách công việc đã lưu, xem chi tiết mô tả, chỉnh sửa nội dung, xóa công việc và đánh dấu hoàn thành/chưa hoàn thành.
- **Tính năng nổi bật:** Giao diện trực quan, tốc độ cực nhanh nhờ công nghệ Caching (bộ nhớ đệm) trên frontend. Bảo mật chặt chẽ bằng Middleware, chống lỗi IDOR, đảm bảo mỗi người dùng chỉ thao tác được trên dữ liệu do chính mình tạo ra.

## 🛠️ Hướng dẫn cài đặt và cấu hình

### Bước 1: Cài đặt môi trường
1. Yêu cầu cài đặt **Python 3.9** trở lên.
2. Mở terminal tại thư mục gốc của dự án và chạy lệnh sau để tải các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

### Bước 2: Cấu hình cơ sở dữ liệu Firebase
1. Truy cập [Firebase Console](https://console.firebase.google.com/).
2. Bật dịch vụ **Firestore Database** và **Authentication** (Bật phương thức Đăng nhập bằng Google & Email/Password). Đảm bảo thêm `localhost` vào mục *Authorized domains* trong cài đặt Authentication.
3. Cấp quyền truy cập cho Backend (`serviceAccountKey.json`):
   - Vào mục **Project settings** (Cài đặt dự án) > **Service accounts** (Tài khoản dịch vụ) > Nhấn **Generate new private key** (Tạo khóa riêng tư mới).
   - Lưu file JSON vừa tải về vào thư mục `backend/` và đổi tên chính xác thành `serviceAccountKey.json`. File này sẽ có cấu trúc mẫu như sau:
     ```json
     {
       "type": "service_account",
       "project_id": "tên-project-của-bạn",
       "private_key_id": "...",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
       "client_email": "...",
       "client_id": "...",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       "auth_provider_x509_cert_url": "...",
       "client_x509_cert_url": "..."
     }
     ```

### Bước 3: Cấu hình biến môi trường (.env)
Dự án được phân tách rõ ràng nên yêu cầu 2 file `.env` khác nhau cho Backend và Frontend.

**1. Cấu hình Backend (`backend/.env`):**
Tạo file `.env` trong thư mục `backend/` với đầy đủ 5 biến số sau:
```env
GOOGLE_CLIENT_ID="Lấy_tại_Google_Cloud_Console"
GOOGLE_CLIENT_SECRET="Lấy_tại_Google_Cloud_Console"
GOOGLE_REDIRECT_URI="http://localhost:8000/auth/google/callback"
FIREBASE_WEB_API_KEY="Lấy_tại_Firebase_Console"
FRONTEND_URL="http://localhost:8501"
```
*🔎 Hướng dẫn lấy Key:*
- **GOOGLE_CLIENT_ID** & **SECRET**: Truy cập [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials), chọn dự án tương ứng. Vào mục *OAuth 2.0 Client IDs* (loại Web application) để sao chép. Phải thêm `http://localhost:8000/auth/google/callback` vào mục *Authorized redirect URIs*.
- **FIREBASE_WEB_API_KEY**: Truy cập [Firebase Console](https://console.firebase.google.com/) > **Project settings** > **General** > Sao chép mã ở dòng **Web API Key**.

**2. Cấu hình Frontend (`frontend/.env`):**
Tạo file `.env` trong thư mục `frontend/` với nội dung sau:
```env
FIREBASE_WEB_API_KEY="Dán_chung_mã_Web_API_Key_của_Firebase_vào_đây"
```
*(Lưu ý: API Key của Frontend chỉ có tác dụng hỗ trợ gọi hàm đăng nhập Email/Mật khẩu).*

## 🚀 Hướng dẫn chạy chương trình

Hệ thống yêu cầu chạy song song Backend và Frontend trên 2 cửa sổ terminal riêng biệt.

**1. Khởi chạy Backend (Máy chủ API):**
Mở terminal 1, di chuyển vào thư mục backend và chạy:
```bash
cd backend
uvicorn main:app --reload
```
*(Backend sẽ chạy tại `http://localhost:8000`. Có thể xem tài liệu API Swagger UI tại `http://localhost:8000/docs`)*

**2. Khởi chạy Frontend (Giao diện người dùng):**
Mở terminal 2, di chuyển vào thư mục frontend và chạy:
```bash
cd frontend
streamlit run app.py
```
*(Ứng dụng web sẽ tự động mở trên trình duyệt tại `http://localhost:8501`)*

## 📡 Hướng dẫn gọi API và ví dụ request/response

Bạn có thể test API trực tiếp qua giao diện Swagger UI tại `http://localhost:8000/docs` hoặc dùng Postman.
*Lưu ý: Các endpoint thao tác với dữ liệu đều yêu cầu đính kèm header `Authorization: Bearer <TOKEN>` để xác minh người dùng.*

### 1. Kiểm tra trạng thái hệ thống
- **Endpoint:** `GET /health`
- **Mục đích:** Đảm bảo Backend đang chạy bình thường.
- **Response (200 OK):**
  ```json
  {
      "status": "healthy",
      "message": "Backend is running smoothly!"
  }
  ```

### 2. Xem thông tin người dùng hiện tại
- **Endpoint:** `GET /auth/me`
- **Header:** `Authorization: Bearer <TOKEN>`
- **Response (200 OK):**
  ```json
  {
      "status": "success",
      "user_id": "8xYzabc123KjL...",
      "email": "student@gmail.com",
      "name": "Người dùng"
  }
  ```

### 3. Thêm công việc mới (Feature chính)
- **Endpoint:** `POST /todos/`
- **Header:** `Authorization: Bearer <TOKEN>`
- **Request Body (JSON):**
  ```json
  {
      "title": "Hoàn thiện bài tập cuối kỳ",
      "description": "Viết file README.md, quay video demo và nộp bài trên hệ thống."
  }
  ```
- **Response (200 OK):** Trả về ID của tài liệu vừa được tạo trên Firestore.
  ```json
  "todo_DocId_12345xyz"
  ```

### 4. Đọc danh sách công việc
- **Endpoint:** `GET /todos/`
- **Header:** `Authorization: Bearer <TOKEN>`
- **Response (200 OK):**
  ```json
  [
      {
          "id": "todo_DocId_12345xyz",
          "title": "Hoàn thiện bài tập cuối kỳ",
          "description": "Viết file README.md, quay video demo và nộp bài trên hệ thống.",
          "completed": false,
          "user_id": "8xYzabc123KjL...",
          "created_at": "2026-05-01T21:45:00.000"
      }
  ]
  ```

### 5. Cập nhật và Xóa công việc
- **Sửa nội dung:** `PUT /todos/{todo_id}` (Truyền Body là JSON chứa `title` và `description` mới).
- **Cập nhật trạng thái:** `PUT /todos/{todo_id}/toggle` (Đánh dấu hoàn thành/chưa hoàn thành).
- **Xóa ghi chú:** `DELETE /todos/{todo_id}`.
- **Response chung (200 OK) khi thành công:**
  ```json
  {
      "message": "Đã thực hiện thành công"
  }
  ```

## 🎥 Liên kết video demo

https://github.com/user-attachments/assets/ead9bf9b-f311-4a4b-a81c-d111b46c9e02


