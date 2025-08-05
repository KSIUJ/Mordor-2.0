from embeddings import SEARCHER

if __name__ == "__main__":
    files = ["Files/algebra","Files/analiza"]
    search = "ekstrema lokalne i globalne"
    a = SEARCHER(files,search)
    a.get_result()

