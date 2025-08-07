import numpy as np
import torch
import PyPDF2
from sentence_transformers import SentenceTransformer, util
from langchain_text_splitters import RecursiveCharacterTextSplitter
class SEARCHER:
    # finds file index with the most matching sentence
    def find_file_index(self,angles):
        SIZE = len(angles)
        biggest = torch.empty(SIZE,dtype = torch.float32)
        biggest_ind = torch.empty(SIZE,dtype = torch.int32)
        for i in range(0,SIZE):
            biggest[i] = torch.max(angles[i])
            biggest_ind[i] = torch.argmax(angles[i])
        IND = torch.argmax(biggest)
        return torch.max(biggest),IND,biggest_ind[IND]

    def __init__(self, files_paths:list):
        self.numOfFiles = 0
        self.model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v4_MiniLM-L6')
        #splits file into sentences
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=150,
            chunk_overlap=50,
            length_function=len,
            separators = ['.','?','!']
        )
        #contains lists of sentences
        self.text = []
        #contains PDF files paths
        self.files = []
        for path in files_paths:
            with open(path,'rb') as pdf:
                #extracting text from PDF file into pdf_text
                reader = PyPDF2.PdfReader(pdf, strict=False)
                pages_text = []
                for page in reader.pages:
                    pages_text.append(page.extract_text())

                pdf_text = "".join(pages_text)
                if(pdf_text==""):
                    continue
                self.files.append(pdf)
                self.numOfFiles+=1
                self.text.append([sentence.page_content for sentence in splitter.create_documents([pdf_text])])
        if(self.numOfFiles==0):
            print("No proper files added")
            return
        #list containing list of embeddings of each sentence e.g. embeddings[i][j] - embeddings of jth sentence in ith file
        self.embeddings = [self.model.encode(d) for d in self.text]

    def get_result(self,search:str):
        if(self.numOfFiles==0):
            print("No proper files added")
            return
        #embedding search from user
        word = self.model.encode(search)
        #calculating embedding similarities between user search and files text
        cos_sim = [util.cos_sim(self.embeddings[i], word).squeeze() for i in range(0,self.numOfFiles)]
        #biggest cosine, index of the most matching file and index of best matching sentence in this file
        COS, F_IND,S_IND  = self.find_file_index(cos_sim)

        print("file: " + str(self.files[F_IND].name))
        print("sentence: " + str(self.text[F_IND][S_IND]))
        print("similarity index: " + str(float(COS)))
        #returns index of most matching file
        return F_IND

