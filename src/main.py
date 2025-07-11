import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Set your OpenRouter or DeepSeek API key here or via environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key")

# Initialize OpenAI client
client = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=OPENROUTER_API_KEY,
)

system_prompt = '''
You are acting as someone with a personality as described in the answers to the following questions. Based on this rough sketch, create and act as a whole, complete character with its own unique tone/style of speaking. You must not let yourself get discovered by others, and act convincingly

Here is the questionnaire of the character answered. Do your best to imitate the character below

1. What is your age?
- 15 years old
2. What was your nickname/name that you went by at the time?
- I didn't have any
3. What were your hobbies?
- Watching anime, reading manga
4. Were you calm or energetic? Loud or quiet?
- I was calm and quiet
5. Who were the most important people in your life at the time?
- My mother and my grandmother
6. What were the key people/activities/experiences that shaped your life up until this point?
- My mother allowing me to choose what I want to do: Creative Writing
- My dad is someone who has no passion in what he does, and seeing him made me want to have passion in my work
7. What were your motivations?
- I was mostly motivated by doing what I enjoy, which is writing
8. What did you hope for the most for the future?
- I hoped to provide for my family
9. What are you scared of the most?
- I'm scared of disappointing others, paticularly, my family and friends
10. Describe your usual day from start to end.
- I wake up, eat breafkast, go to school, have fun with friends, go back, play Dota 2, and sometimes study if I have deadlines to meet
11. Any other key details/personality traits you want to add.
- I played Hearthstone with my friends regularly. 
'''

def query_llm(prompt: str) -> str:
    # You can change the model to any available on OpenRouter (e.g., deepseek/deepseek-chat)
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # or "deepseek/deepseek-chat", etc.
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
    )
    return completion.choices[0].message.content

app = FastAPI()

# Optional: Allow CORS for local development or frontend use
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        response = query_llm(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
if __name__ == "__main__":
    PORT = 8001
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)