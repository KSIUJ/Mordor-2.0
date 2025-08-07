from embeddings import SEARCHER
import time
if __name__ == "__main__":
    files = ["Files/wdm.pdf","Files/algebra.pdf","Files/analiza.pdf","Files/algorytmy.pdf","Files/java.pdf"]
    search = "inheritance and polymorphism"
    a = SEARCHER(files)
    s = time.time()
    a.get_result(search)
    e = time.time()
    print(e-s)

