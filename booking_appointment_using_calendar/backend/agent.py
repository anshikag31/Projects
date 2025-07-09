from langchain_community.chat_models import ChatTogether
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from datetime import datetime, timedelta
from dateparser.search import search_dates
import re
import os

from backend.calendar_utils import check_availability, book_appointment

# Initialize Together.ai LLM (API key must be set in Render environment)
llm = ChatTogether(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.7,
    max_tokens=512
)

def parse_future_datetime(text: str):
    results = search_dates(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.now()
        }
    )
    if not results:
        return None
    return results[0][1]

def book_appointment_wrapper(text: str) -> str:
    try:
        summary = "Meeting"
        parts = text.lower().split(" for ")
        time_part = parts[0].replace("book", "").strip()
        duration_phrase = parts[1] if len(parts) == 2 else "30 minutes"

        start_dt = parse_future_datetime(time_part)
        if not start_dt:
            return "❌ Sorry, I couldn't understand the time you mentioned. Try: 'Book a meeting tomorrow at 4pm for 1 hour'."

        minutes = 30
        match = re.search(r"(\d+)\s*min", duration_phrase)
        if match:
            minutes = int(match.group(1))
        elif "hour" in duration_phrase:
            match = re.search(r"(\d+)", duration_phrase)
            if match:
                minutes = int(match.group(1)) * 60

        end_dt = start_dt + timedelta(minutes=minutes)
        return book_appointment(summary, start_dt.isoformat(), end_dt.isoformat())

    except Exception as e:
        return f"❌ Error while booking: {e}"

def check_availability_wrapper(text: str) -> str:
    try:
        start_dt = parse_future_datetime(text)
        if not start_dt:
            return "❌ Sorry, I couldn't understand the time. Try: 'Is tomorrow at 3pm available?'."

        end_dt = start_dt + timedelta(minutes=30)
        return check_availability(start_dt.isoformat(), end_dt.isoformat())

    except Exception as e:
        return f"❌ Error while checking availability: {e}"

tools = [
    Tool(
        name="CheckAvailability",
        func=check_availability_wrapper,
        description="Use this tool to check if a time slot is available."
    ),
    Tool(
        name="BookAppointment",
        func=book_appointment_wrapper,
        description="Use this tool to book a calendar meeting."
    )
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    memory=memory,
    verbose=True
)
