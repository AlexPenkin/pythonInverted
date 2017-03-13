import csv
import collections
import functools


def removePunctuation(string):
    return "".join(c for c in string if c not in ('!', '.', ':', ',', '`', "'", '"'))


class Searcher:
    inverted_index = collections.defaultdict(set)
    parsedDoc = {}

    def __init__(self, tsv):
        with open(tsv) as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for line in tsvreader:
                self.parsedDoc[line[0]] = line[1]
        for key, value in self.parsedDoc.items():
            out = removePunctuation(value).lower().split(" ")
            for word in out:
                self.inverted_index[word].add(key)

    def search(self, query):
        response = []
        buf = []
        parsedQuery = removePunctuation(query).lower().strip()
        parsedQuery = ' '.join(parsedQuery.split()).split()
        queryLength = len(parsedQuery)
        if queryLength == 1 and self.inverted_index[parsedQuery[0]]:
            for value in self.inverted_index[parsedQuery[0]]:
                t = (value, self.parsedDoc[value], 1)
                response.append(t)
        elif queryLength > 1:
            i = 0
            while i < queryLength:
                if self.inverted_index[parsedQuery[i]]:
                    buf.append(self.inverted_index[parsedQuery[i]])
                i = i + 1
            union = functools.reduce((lambda x, y: x | y), buf)
            for value in union:
                ocassions = 0
                b = 0
                while b < queryLength:
                    if parsedQuery[b] in self.parsedDoc[value].lower():
                        ocassions = ocassions + 1
                    b = b + 1
                tupl = (value, self.parsedDoc[value], ocassions)
                response.append(tupl)
        response = sorted(response, key=lambda x: x[2], reverse=True)       
        return response

searcher = Searcher("cooking_books.tsv")
result = searcher.search('verdure recipes')
assert result[0][1] == 'Verdure: Simple Recipes in the Italian Style', 'Houston we`ve got a problem'
result = searcher.search('')
assert result[0][1] == None, 'Houston we`ve got a problem'
