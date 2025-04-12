from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.db.session import Base, engine


def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)

    user = get_user_by_email(db, email="test@example.com")
    if not user:
        user_in = UserCreate(
            email="test@example.com",
            password="test123"
        )
        user = create_user(db, email=user_in.email, password=user_in.password)
        print(f"Created test user: {user.email}")

    # Add sample financial data
    from app.models.financial import Debt, Expense, Income
    from app.models.chat import ChatMessage
    from datetime import datetime, timedelta

    # Add sample debts
    debts = [
        {
            "user_id": user.id,
            "type": "CREDIT_CARD",
            "amount": 5000.00,
            "interest_rate": 18.99,
            "minimum_payment": 100.00,
            "due_date": datetime.now() + timedelta(days=15),
            "description": "Main credit card",
        },
        {
            "user_id": user.id,
            "type": "STUDENT_LOAN",
            "amount": 25000.00,
            "interest_rate": 5.50,
            "minimum_payment": 250.00,
            "due_date": datetime.now() + timedelta(days=30),
            "description": "Federal student loan",
        },
    ]

    for debt_data in debts:
        debt = db.query(Debt).filter_by(
            user_id=debt_data["user_id"],
            type=debt_data["type"]
        ).first()
        if not debt:
            debt = Debt(**debt_data)
            db.add(debt)
            print(f"Created debt: {debt.type} - ${debt.amount}")

    # Add sample expenses
    expenses = [
        {
            "user_id": user.id,
            "category": "HOUSING",
            "amount": 1200.00,
            "date": datetime.now(),
            "description": "Monthly rent",
        },
        {
            "user_id": user.id,
            "category": "FOOD",
            "amount": 500.00,
            "date": datetime.now(),
            "description": "Groceries",
        },
        {
            "user_id": user.id,
            "category": "TRANSPORTATION",
            "amount": 200.00,
            "date": datetime.now(),
            "description": "Gas and maintenance",
        },
    ]

    for expense_data in expenses:
        expense = db.query(Expense).filter_by(
            user_id=expense_data["user_id"],
            category=expense_data["category"],
            date=expense_data["date"]
        ).first()
        if not expense:
            expense = Expense(**expense_data)
            db.add(expense)
            print(f"Created expense: {expense.category} - ${expense.amount}")

    # Add sample income
    incomes = [
        {
            "user_id": user.id,
            "amount": 4000.00,
            "source": "Salary",
            "date": datetime.now(),
            "is_recurring": True,
        },
    ]

    for income_data in incomes:
        income = db.query(Income).filter_by(
            user_id=income_data["user_id"],
            source=income_data["source"],
            date=income_data["date"]
        ).first()
        if not income:
            income = Income(**income_data)
            db.add(income)
            print(f"Created income: {income.source} - ${income.amount}")

    # Add sample chat messages
    chat_messages = [
        {
            "user_id": user.id,
            "content": "Hello, I need help managing my debt.",
            "message_type": "user",
            "created_at": datetime.now() - timedelta(hours=1),
        },
        {
            "user_id": user.id,
            "content": "I'll help you analyze your financial situation and provide personalized advice. I see you have $30,000 in total debt. Let's create a plan to manage this effectively.",
            "message_type": "assistant",
            "created_at": datetime.now() - timedelta(hours=1),
        },
    ]

    for message_data in chat_messages:
        message = db.query(ChatMessage).filter_by(
            user_id=message_data["user_id"],
            content=message_data["content"],
            created_at=message_data["created_at"]
        ).first()
        if not message:
            message = ChatMessage(**message_data)
            db.add(message)
            print(f"Created chat message: {message.message_type}")

    db.commit()
    print("Database initialization completed!")
