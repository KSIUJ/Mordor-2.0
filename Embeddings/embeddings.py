import numpy as np
import torch
import PyPDF2
import chromadb
from sentence_transformers import SentenceTransformer, util
from langchain_text_splitters import RecursiveCharacterTextSplitter
class SEARCHER:
    # finds file index with the most matching sentence
    def codePair(self,a:int, b:int)->int:
        return (a + b) * (a + b + 1) // 2 + b
    def uncodePair(self,z:int)->int:
        w = int(((8*z + 1)**0.5 - 1) // 2)
        t = w * (w+1) // 2
        b = z - t
        a = w - b
        return a, b
    def addChunk(self,text:str,id:str)->None:
        self.collection.add(
            documents = text,
            ids = str(id),
            embeddings = np.array(self.model.encode(text))
        )
    def EmbedFile(self, path:str, chunkSize:int, sep:list)->None:
        pdf_text=""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunkSize,
            chunk_overlap=50,
            length_function=len,
            separators = sep
        )
        # extracting all file text into pdf_text
        with open(path,'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pages_text = []
            for page in reader.pages:
                pages_text.append(page.extract_text())
                pdf_text = "".join(pages_text)
                if(pdf_text==""):
                    raise TypeError(f"file ({path})  has no extractable data")
                    return
        
        self.numOfFiles+=1
        text = [file.page_content for file in splitter.create_documents([pdf_text])]
        # if last chunk is smaller than half of chunkSize then merge last two chunks
        #if(len(text)>=2 and len(text[-1])<chunkSize/2):
        #    text[-2]+=text.pop()
        for i in range(0,len(text)):
            self.addChunk(text[i],self.codePair(self.numOfFiles,i))



    def __init__(self):
        #initializing data base
        chroma_client = chromadb.Client()
        self.collection = chroma_client.get_or_create_collection(name="books")
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
        for code in query['ids'][0]:
            print("file nr. " + str(self.uncodePair(int(code))[0]))
            
        return query;

