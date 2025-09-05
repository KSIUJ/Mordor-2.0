import numpy as np
import torch
import PyPDF2
import chromadb
from sentence_transformers import SentenceTransformer, util
from langchain_text_splitters import RecursiveCharacterTextSplitter
class SEARCHER:
    # code file id and embedding id as one hash
    def codePair(self,a:int, b:int)->int:
        return (a + b) * (a + b + 1) // 2 + b
    # decode hash into file id and embedding id 
    def uncodePair(self,z:int)->int:
        w = int(((8*z + 1)**0.5 - 1) // 2)
        t = w * (w+1) // 2
        b = z - t
        a = w - b
        return a, b
    # adds chunk of text with it's id into database
    def addChunk(self,text:str,id:str)->None:
        self.collection.add(
            documents = text,
            ids = str(id),
            embeddings = np.array(self.model.encode(text))
        )
    # embeds file chunks based on given arguments
    # path - path to a PDF file
    # chunkSize - maximum number of characters in single chunk
    # sep - list of chunk separators as characters
    def EmbedFile(self, path:str, chunkSize:int, sep:list)->None:
        pdf_text=""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunkSize,
            chunk_overlap=50,
            length_function=len,
            separators = sep
        )
        # extracting all file text into pdf_text variable
        with open(path,'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pages_text = []
            for page in reader.pages:
                pages_text.append(page.extract_text())
                pdf_text = "".join(pages_text)
                # if no text extracted throw an error
                if(pdf_text==""):
                    raise TypeError(f"file ({path})  has no extractable data")
                    return
        
        self.numOfFiles+=1
        #list of strings represanting each chunk in given file 
        text = [file.page_content for file in splitter.create_documents([pdf_text])]
        for i in range(0,len(text)):
            # adding chunk into database
            self.addChunk(text[i],self.codePair(self.numOfFiles,i))



    def __init__(self):
        #initializing data base
        from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

        chroma_client = chromadb.HttpClient(
            host="chromadb",
            port=8000,
            ssl=False,
            headers=None,
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )
        #chroma_client = chromadb.Client()
        self.collection = chroma_client.get_or_create_collection(name="books")
        #initializing embedding model
        self.model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v4_MiniLM-L6')
        #number of propare files
        self.numOfFiles = 0

    def get_result(self,search:str):
        if(self.numOfFiles==0):
            print("No proper files added")
            return
        #embedding search from user
        word = np.array(self.model.encode(search))
        SIZE = self.numOfFiles
        #getting most matching files
        query = self.collection.query(
                    query_embeddings = word,
                    n_results = 10
                )
            
        return query;

