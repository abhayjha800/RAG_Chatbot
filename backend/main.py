import os
from dotenv import load_dotenv
import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import QueryRequest, HistoryRequest, UserRequest

#RAG
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables from .env file
load_dotenv(dotenv_path='../.env')
DB_URL = os.getenv("DATABASE_URL")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

#RAG Setup
FAISS_INDEX_PATH="../faiss_index"

print("Loading FAISS index...")
embeddings =HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

print("FAISS index loaded successfully.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})

SYSTEM_PROMPT = '''
You are a helpful assistant.
Use the context to answer the question in max three sentences.
If you don't know , just say don't know.
Context: {context}
Chat History: {chat_history}
'''

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
])

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)

print("RAG chain created successfully.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

#api endpoints and logic would go here

#login/signup
@app.post("/get_or_create_user")
def get_or_create_user(user_request: UserRequest):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (user_request.username,))
    user = cur.fetchone()

    if user:
        user_id = user[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (user_request.username,))
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return {"user_id": user_id, "username": user_request.username}

#chat history
@app.post("/get_history")
def get_history(history_request: HistoryRequest):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT prompt, answer FROM chat_history WHERE user_id = %s ORDER BY id ASC", (history_request.user_id,))
    history = cur.fetchall()

    cur.close()
    conn.close()

        # Format for frontend
    formatted_history = []
    for p, a in history:
        formatted_history.append({"role": "human", "content": p})
        formatted_history.append({"role": "ai", "content": a})

    #[{"role": "human", "content": "hi"}, {"role": "ai", "content": "hello how i can help you"}, {"role": "human", "content": "hi"}, {"role": "ai", "content": "hello how i can help you"}]
    return {"history": formatted_history}

#chat endpoint
@app.post("/query")
def query(query_request: QueryRequest):
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch chat history for context
    cur.execute("SELECT prompt, answer FROM chat_history WHERE user_id = %s ORDER BY id ASC", (query_request.user_id,))
    history = cur.fetchall()

    chat_history = []
    for p, a in history:
        chat_history.append(HumanMessage(content=p))
        chat_history.append(AIMessage(content=a))

    # Generate response using RAG chain
    response = rag_chain.invoke({"input": query_request.text, "chat_history": chat_history})
    answer = response.get("answer", "no answer generated")
    # Store the new interaction in the database
    cur.execute("INSERT INTO chat_history (user_id, prompt, answer) VALUES (%s, %s, %s)", 
                (query_request.user_id, query_request.text, answer))
    conn.commit()

    cur.close()
    conn.close()

    return {"answer": answer}

@app.get("/")
def read_root():
    return {"message": "welcome to fastapi.go to /docs to get started"}
