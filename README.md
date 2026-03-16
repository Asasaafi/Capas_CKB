# Capas_CKB

This project consists of a **Frontend** built with **Vue 3 + Vite** and a **Backend** built with **FastAPI (Python)**.

---

## Requirements
Make sure the following software is installed:

- Node.js (v24 recommended)
- npm

---
## Frontend Setup (Vue 3 + Vite)

1. Go to the frontend folder

cd frontend

2. Install dependencies

npm install

3. Run the frontend

npm run dev

Frontend will run on:  
http://localhost:5173

---

## Backend Setup (FastAPI)

1. Go to the backend folder

cd backend

2. Create virtual environment

python -m venv venv

3. Activate virtual environment

Windows:  
venv\Scripts\activate  

Bash:
source venv/Scripts/activate

4. Install required libraries

pip install pandas numpy joblib fastapi uvicorn

5. Run the backend server

uvicorn main:app --reload

Backend will run on:  
http://127.0.0.1:8000

API documentation:  
http://127.0.0.1:8000/docs

---

## Notes

Make sure both **frontend and backend servers are running at the same time** for the application to work properly.