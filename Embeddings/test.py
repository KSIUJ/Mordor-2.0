from embeddings import SEARCHER
import time
if __name__ == "__main__":
    files = ["Files/algebra.pdf","Files/wdm.pdf","Files/java.pdf","Files/analiza.pdf"]
    search = "inheritance and polymorphism"
    a = SEARCHER()
    p = time.time()
    for file in files:
        a.EmbedFile(file,150,['.','?','!'])
    print(time.time()-p)
    p = time.time()
    a.get_result(search)
    print(time.time()-p)

