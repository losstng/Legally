# Legally

Legally is an experimental legal Q&A assistant built as a personal learning project. The backend uses **FastAPI** while the frontend in `legally/` is a **Next.js** application. The project demonstrates OTP based authentication, session handling and vector database retrieval for answering questions from uploaded documents.

## Requirements

- Python 3.12+
- Node.js (for the frontend)

## Quick Start

### Backend
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the API:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend
1. Install packages:
   ```bash
   cd legally
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev
   ```

Visit `http://localhost:8000` for the API and `http://localhost:3000` for the UI.

## About

This repository started as a portfolio experiment by Hoang Hai Long Do to explore full‑stack development. It brings together legal document processing and modern web frameworks to create a chat style interface for legal questions. The code is for demonstration and educational use only and should not be relied upon as legal advice.
