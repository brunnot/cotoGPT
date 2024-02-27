from langchain_community.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

class CotoGPT:

    db = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="llama2")
        self.textSplitter = RecursiveCharacterTextSplitter(chunk_size=1040, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template("""
            <s> [INST] Você é um assistente para tarefas de resposta a perguntas. Use os seguintes trechos de contexto 
            recuperado para responder à pergunta. Se você não souber a resposta, apenas diga que não sabe. 
            Use no máximo três frases e mantenha a resposta concisa [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

    def ingest(self, pdfFilePath: str):
        docs = PyPDFLoader(file_path=pdfFilePath).load()

        chunks = self.textSplitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        text = ""
        i = 0
        for chunk in chunks:
            i = i + 1
            print( "Chunk ", i )
            print( chunk.page_content )
            print( "================" )

        db = Chroma.from_documents( documents=chunks, embedding=FastEmbedEmbeddings() )
        self.retriever = db.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": 3,
                    "score_threshold": 0.5
                }
        )

        self.chain = ( {"context": self.retriever, "question": RunnablePassthrough()}
                       | self.prompt
                       | self.model
                       | StrOutputParser()
                     )
    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        return self.chain.invoke(query)

    def clear(self):
        self.db = None
        self.retriever = None
        self.chain = None