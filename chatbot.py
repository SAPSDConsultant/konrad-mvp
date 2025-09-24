import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Cargar variables de entorno
load_dotenv()

# Constantes
DB_FAISS_PATH = 'faiss_index'

def main():
    """
    Función principal para ejecutar el chatbot.
    """
    # Cargar la base de datos vectorial
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # Configurar el modelo de lenguaje
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5)

    # Crear el prompt template
    prompt_template = """
    Actúa como "Konrad", un asistente experto en procesos de SAP SD. Tu objetivo es ayudar a los usuarios finales a ejecutar sus tareas diarias.

- Tu tono debe ser claro, directo y amigable.
- Cuando un proceso lo requiera, formatea tus respuestas usando viñetas (bullets) o tablas para que sean fáciles de seguir.
- Responde a la pregunta basándote únicamente en el siguiente contexto. No inventes información.
- Si la respuesta no se encuentra en el contexto, simplemente di: "No he encontrado esa información en la base de conocimiento".

Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Crear la cadena RAG (Retrieval-Augmented Generation)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("Hola, soy Konrad y mi objetivo es ayudarte en los Procesos de SAP SD. ¿Qué te gustaría consultar?")
    print("Escribe 'salir' para terminar.")

    while True:
        question = input("\nPregunta: ")
        if question.lower() == 'salir':
            break

        # Invocar la cadena y mostrar la respuesta
        response = rag_chain.invoke(question)
        print("\nRespuesta de Konrad:")
        print(response)

if __name__ == '__main__':
    main()