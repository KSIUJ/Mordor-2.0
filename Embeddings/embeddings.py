import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
from langchain_text_splitters import RecursiveCharacterTextSplitter
class SEARCHER:

    def get_biggest(self,angle):
        return torch.argmax(angle)

    def find_file_index(self,angles):
        SIZE = len(angles)
        biggest = torch.empty(SIZE,dtype = torch.float32)
        for i in range(0,SIZE):
            biggest[i] = torch.max(angles[i])
        return torch.max(biggest),self.get_biggest(biggest)

    def __init__(self, files_paths:list, search:str):
        model = SentenceTransformer('flax-sentence-embeddings/all_datasets_v4_MiniLM-L6')
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=150,
            chunk_overlap=50,
            length_function=len,
            separators = ['.','?','!']
        )
        data = []
        self.files = []
        for path in files_paths:
            with open(path,'r') as file:
                self.files.append(file)
                data.append(splitter.create_documents([file.read()]))
        self.text = [[item.page_content for item in data[i]] for i in range(0,len(self.files))]
        self.embeddings = [model.encode(d) for d in self.text]
        self.word = model.encode(search)
        self.cos_sim = [util.cos_sim(self.embeddings[i], self.word).squeeze() for i in range(0,len(self.text))]
        self.COS, self.IND = self.find_file_index(self.cos_sim)

    def get_result(self):
        print("file: " + str(self.files[self.IND].name))
        print("similarity index: " + str(float(self.COS)))
        return self.IND


'''
#print(get_biggest(cos_sim))
#print(cos_sim[0][get_biggest(cos_sim[0])])
#print(cos_sim[1][get_biggest(cos_sim[1])])
all_sentence_combinations = []
for i in range(len(cos_sim)-1):
    for j in range(i+1, len(cos_sim)):
        all_sentence_combinations.append([cos_sim[i][j], i, j])

all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)
print("sentence pairs similarity ranked:")
for score, i, j in all_sentence_combinations:
    print("{} \t {} \t {:.4f}".format(sentences[i], sentences[j], cos_sim[i][j]))
'''
