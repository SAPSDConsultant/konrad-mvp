from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Cargar variables de entorno
load_dotenv()

# --- Lógica del Chatbot (similar a chatbot.py) ---

# Constantes
DB_FAISS_PATH = 'faiss_index'

# Cargar la base de datos vectorial
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Configurar el modelo de lenguaje
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5)

# Crear el prompt template
prompt_template = """
Responde a la pregunta basándote únicamente en el siguiente contexto:
{context}

Pregunta: {question}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

# Crear la cadena RAG (Retrieval-Augmented Generation)
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- Configuración de la API ---

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configurar CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir el modelo de datos para la pregunta
class Query(BaseModel):
    question: str

# Definir el endpoint de la API
@app.post("/ask")
def ask_question(query: Query):
    """
    Recibe una pregunta y devuelve la respuesta del chatbot.
    """
    response = rag_chain.invoke(query.question)
    return {"answer": response}