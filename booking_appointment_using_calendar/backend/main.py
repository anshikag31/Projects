from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent, memory

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat_with_agent(message: Message):
    try:
        # Use agent.invoke (recommended in latest LangChain versions)
        response = agent.invoke({
            "input": message.text,
            "chat_history": memory.chat_memory.messages  # send actual memory
        })

        return {"response": response["output"]}
    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}
