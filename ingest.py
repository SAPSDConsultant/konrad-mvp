import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Constantes
PDF_PATH = "data/Base_Pricing.pdf" # IMPORTANTE: Reemplaza esto con el nombre exacto de tu archivo PDF
DB_FAISS_PATH = 'faiss_index'

def main():
    """
    Función principal para crear la base de datos vectorial.
    """
    # 1. Validar la API Key
    if not os.getenv("GOOGLE_API_KEY"):
        print("La variable de entorno GOOGLE_API_KEY no está configurada.")
        return

    # 2. Cargar el documento PDF
    print("Cargando documento PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    if not documents:
        print("No se pudo cargar el documento. Verifica la ruta del archivo.")
        return
    print(f"Documento cargado. {len(documents)} página(s) encontradas.")

    # 3. Dividir el texto en fragmentos (chunks)
    print("Dividiendo el texto en fragmentos...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    print(f"Texto dividido en {len(docs)} fragmentos.")

    # 4. Crear los embeddings y la base de datos vectorial
    print("Creando embeddings y la base de datos FAISS...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(docs, embeddings)

    # 5. Guardar la base de datos localmente
    db.save_local(DB_FAISS_PATH)
    print(f"La base de datos vectorial ha sido creada y guardada en '{DB_FAISS_PATH}'.")

if __name__ == "__main__":
    main()