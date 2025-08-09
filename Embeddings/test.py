from embeddings1 import SEARCHER
import time
if __name__ == "__main__":
    files = ["Files/wdm.pdf","Files/algebra.pdf","Files/analiza.pdf","Files/algorytmy.pdf","Files/java.pdf"]
    search = "inheritance and polymorphism"
    a = SEARCHER(files)
    ans = []
    for i in range(20):
        s = time.time()
        a.get_result(search)
        e = time.time()
        ans.append(round(e-s,4))
    print(ans)
