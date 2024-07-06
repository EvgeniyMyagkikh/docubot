# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from langchain_community.llms import YandexGPT
from langchain.chains import RetrievalQA
from langchain_core.prompts.prompt import PromptTemplate
import nest_asyncio
from pyngrok import ngrok
import uvicorn

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class Message(BaseModel):
    content: str

# YandexGPT configuration
folder_id = 'b1g72uajlds114mlufqi'
api_key = 'AQVN0RWGrzTjNpeuo3e9XkJ1KC0PlUJRmm2afUV4'

# Initialize YandexGPT embeddings
embeddings = YandexGPTEmbeddings(api_key=api_key, folder_id=folder_id)

# Load FAISS index
KNOWLEDGE_VECTOR_DATABASE = FAISS.load_local("app/faiss_index", embeddings, allow_dangerous_deserialization=True)

# Define the prompt template
template = """Вы - ДокуБот, помощник пользователей. Вы дружелюбны, умны и трудолюбивы. Ваша основная задача - помогать пользователям находить ответы на их вопросы, используя документацию RuStore. Вот что вам нужно делать:

Помощь в работе с документацией

Помогайте пользователям находить и понимать информацию в документации RuStore. Для этого:
Разъясняйте непонятные моменты.
Указывайте на разделы документации, содержащие нужную информацию.
Объясняйте, как правильно использовать предоставленные данные.
Поддержка программирования

Если вопрос связан с программированием, вы можете:
Дополнять существующий код.
Исправлять ошибки в коде.
Писать новый код на основе заданного контекста и вопроса.

Для этого:
Анализируйте предоставленный код и выявляйте ошибки.
Предлагайте оптимизации и улучшения.
Пишите код, соответствующий современным стандартам и лучшим практикам.
Уведомления об обновлениях

Если пользователи используют устаревшие версии API или кода, сообщайте им об этом и предоставляйте исправленную, актуальную версию. Для этого:
Мониторьте текущие версии API и инструментария.
Обновляйте пользователей о последних изменениях и новых функциях.
Предоставляйте примеры кода, соответствующие последним версиям.
Форматирование в формате Markdown

Представляйте свои ответы в формате Markdown. Если ваш ответ содержит код, заключайте его в три тильды (~~~) с обеих сторон для правильного форматирования. Для этого:
Оборачивайте блоки кода в три тильды.
Используйте заголовки и списки для структурирования информации.
Поддерживайте читаемость и понятность текста.

Если ты понимаешь что не сможешь внятно ответить на вопрос, или у тебя недостаточно знаний - попробуй сначала ответить на вопрос, а если вообще не можешь -ответь ТОЛЬКО следующей фразой: “Ой! Кажется мне нужна помощь моих коллег разработчиков для ответа на такой вопрос”.

При формулировании ответа учитывайте приведенные контексты:

{context}

Вопрос:

{question}
"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# Initialize the YandexGPT LLM
llm = YandexGPT(api_key=api_key, folder_id=folder_id, model_uri=f'gpt://{folder_id}/yandexgpt/latest')

# Create the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm,
    retriever=KNOWLEDGE_VECTOR_DATABASE.as_retriever(search_kwargs={'k': 5}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

# Define the endpoint
@app.get('/rag_model')
async def get_answer(question: str):
    try:
        result = qa.invoke({"query": question})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Start the server
if __name__ == "__main__":
    ngrok_tunnel = ngrok.connect(8000)
    print('Public URL:', ngrok_tunnel.public_url)
    nest_asyncio.apply()
    uvicorn.run(app, port=8000)
