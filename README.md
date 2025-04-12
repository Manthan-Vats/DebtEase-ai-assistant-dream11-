# Debt Management AI Assistant

A conversational AI tool that helps users manage their debt through personalized recommendations and visualizations.

## Features

- 🤖 AI-powered debt management conversations
- 📊 Interactive financial visualizations
- 📈 Predictive analytics for debt scenarios
- 💼 Comprehensive financial dashboard
- 🔒 Secure authentication system
- 📱 Responsive neo-noir themed UI

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Chart.js
- Backend: Python, FastAPI
- Database: PostgreSQL
- AI: OpenAI API
- Authentication: JWT

## Project Structure

```
debt-management-ai/
├── frontend/           # Frontend application
├── backend/           # FastAPI backend
├── database/          # Database migrations and schemas
└── docs/             # Documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL
- OpenAI API key

### Backend Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run migrations:

   ```bash
   alembic upgrade head
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for the interactive API documentation.

## Testing

- Backend tests: `pytest`
- API testing: Use the provided Postman collection in `docs/postman/`

## License

MIT License
