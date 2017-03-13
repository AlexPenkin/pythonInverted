import sys
from search import Searcher

if __name__ == "__main__":
    queryStr = str(input())
    searcher = Searcher("cooking_books.tsv")
    result = searcher.search(queryStr)
    print(queryStr)
    i = 0
    for title in result:
        print(title[1] + "\n")
        i = i + 1
        if i == 25:
            break
