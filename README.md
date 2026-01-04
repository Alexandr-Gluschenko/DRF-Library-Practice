# 📚 DRF Library Management

Online library system to manage books, borrowings, users, payments, and notifications. Fully API-driven; no frontend required.

---

## ⚡ Features

- Books: CRUD + inventory management  
- Users: Registration, JWT auth, profile  
- Borrowings: Borrow, return, track active/overdue  
- Payments: Stripe integration (PAYMENT / FINE)  
- Notifications: Telegram alerts (new borrowing, overdue, payment)  

Supports ~5 concurrent users, 1000 books, 50k borrowings/year.

---

## 🏗 Architecture

Book: title, author, cover(HARD|SOFT), inventory, daily_fee  
User: email, first_name, last_name, password, is_staff  
Borrowing: borrow_date, expected_return_date, actual_return_date, book_id, user_id  
Payment: status(PENDING|PAID), type(PAYMENT|FINE), borrowing_id, session_url, money_to_pay  

---

## 🚀 API Endpoints

Books: `POST /books/`, `GET /books/`, `GET /books/<id>/`, `PUT/PATCH /books/<id>/`, `DELETE /books/<id>/`  
Users: `POST /users/`, `POST /users/token/`, `POST /users/token/refresh/`, `GET /users/me/`, `PUT/PATCH /users/me/`  
Borrowings: `POST /borrowings/`, `GET /borrowings/?user_id=&is_active=`, `GET /borrowings/<id>/`, `POST /borrowings/<id>/return/`  
Payments: `GET /success/`, `GET /cancel/`  

---

## ⚙ Setup (Docker)

1. .env
SECRET_KEY=your_secret_key
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
BOT_TOKEN=your_bot_token
ADMIN_CHAT_ID=your_chat_id

## Сreate superuser

docker compose exec app python manage.py createsuperuser

## API 
http://localhost:8000/

