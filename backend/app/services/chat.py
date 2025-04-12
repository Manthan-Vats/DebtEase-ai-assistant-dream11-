from typing import List, Optional
from sqlalchemy.orm import Session
import openai
from app.core.config import settings
from app.models.chat import ChatMessage
from app.crud import crud_debt, crud_expense, crud_income


class ChatService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def get_response(
        self,
        message: str,
        user_id: int,
        db: Session
    ) -> str:
        """
        Get AI response based on user message and financial context
        """
        # Get user's financial context
        debts = crud_debt.get_multi_by_user(db, user_id=user_id)
        expenses = crud_expense.get_multi_by_user(db, user_id=user_id)
        incomes = crud_income.get_multi_by_user(db, user_id=user_id)

        # Create context for the AI
        context = self._create_financial_context(debts, expenses, incomes)

        # Get chat history
        chat_history = self.get_chat_history(db, user_id, limit=5)
        conversation_history = self._format_chat_history(chat_history)

        # Prepare the prompt
        prompt = f"""
        You are a debt management AI assistant. Use the following financial context to provide personalized advice:
        
        {context}
        
        Previous conversation:
        {conversation_history}
        
        User: {message}
        Assistant:"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful debt management assistant. Provide clear, actionable advice based on the user's financial situation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content.strip()

            # Save the conversation
            self._save_conversation(db, user_id, message, ai_response)

            return ai_response

        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

    def get_chat_history(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[ChatMessage]:
        """
        Get chat history for a user
        """
        return db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).order_by(
            ChatMessage.created_at.desc()
        ).offset(skip).limit(limit).all()

    def _create_financial_context(
        self,
        debts: List,
        expenses: List,
        incomes: List
    ) -> str:
        """
        Create a context string from financial data
        """
        total_debt = sum(debt.amount for debt in debts)
        total_expenses = sum(expense.amount for expense in expenses)
        total_income = sum(income.amount for income in incomes)

        context = f"""
        Current Financial Summary:
        - Total Debt: ${total_debt:,.2f}
        - Monthly Expenses: ${total_expenses:,.2f}
        - Monthly Income: ${total_income:,.2f}
        
        Debt Breakdown:
        {self._format_debt_breakdown(debts)}
        
        Expense Categories:
        {self._format_expense_categories(expenses)}
        """

        return context

    def _format_debt_breakdown(self, debts: List) -> str:
        breakdown = []
        for debt in debts:
            breakdown.append(
                f"- {debt.type}: ${debt.amount:,.2f} (Interest: {debt.interest_rate}%)")
        return "\n".join(breakdown)

    def _format_expense_categories(self, expenses: List) -> str:
        categories = {}
        for expense in expenses:
            if expense.category not in categories:
                categories[expense.category] = 0
            categories[expense.category] += expense.amount

        breakdown = []
        for category, amount in categories.items():
            breakdown.append(f"- {category}: ${amount:,.2f}")
        return "\n".join(breakdown)

    def _format_chat_history(self, chat_history: List[ChatMessage]) -> str:
        formatted_history = []
        for message in reversed(chat_history):
            role = "User" if message.message_type == "user" else "Assistant"
            formatted_history.append(f"{role}: {message.content}")
        return "\n".join(formatted_history)

    def _save_conversation(
        self,
        db: Session,
        user_id: int,
        user_message: str,
        ai_response: str
    ) -> None:
        """
        Save the conversation to the database
        """
        # Save user message
        user_chat = ChatMessage(
            user_id=user_id,
            content=user_message,
            message_type="user"
        )
        db.add(user_chat)

        # Save AI response
        ai_chat = ChatMessage(
            user_id=user_id,
            content=ai_response,
            message_type="assistant"
        )
        db.add(ai_chat)

        db.commit()
