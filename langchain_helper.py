from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.llms import OpenAI 
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS   #for effiecient similarity search
from dotenv import load_dotenv
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os


load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#embeddings=OpenAIEmbeddings()

video_url="https://www.youtube.com/watch?v=8JJ101D3knE"

def create_vectordb_from_yt_url(video_url:str)->FAISS:
    loader=YoutubeLoader.from_youtube_url(video_url)
    transcript=loader.load()

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    docs=text_splitter.split_documents(transcript)

    db=FAISS.from_documents(docs,embeddings)
    return db
#the above fn splies text insto smaller chunk, bcuz each open ai has a limit, to tye amount of words we can send at a time
# print(create_vectordb_from_yt_url(video_url))

def get_response_from_query(db,query,k=4):  
    #text-davinci can handle 4097 tokens

    docs=db.similarity_search(query, k=k)
    docs_page_content=" ".join([d.page_content for d in docs]) # joined all 4 documents

    #llm=OpenAI(model="gpt-3.5-turbo-instruct", organization="org-0TriDsgOFTjJK91ndIjkq7mh")
    llm = ChatGoogleGenerativeAI(
    #model="models/gemini-pro",
    model="models/gemini-1.5-pro-latest",

    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    )


    prompt=PromptTemplate(
        input_variables=["question","docs"],
        template="""
        You are a helpful YouTube assistant that can answer questions about videos based on the video's
        transcript.
        Answer the following question: {question}
        By searching the following video transcript:{docs}
        Only use the factual information from the transcript to answer the question.
        If you feel like you don't have enough information to answer the question, say "I don't know".
        Your answer should be detailed.
        """,
    )

    chain=LLMChain(llm=llm,prompt=prompt)
    response=chain.run(question=query, docs=docs_page_content)
    response= response.replace("\n","")
    return response


    
