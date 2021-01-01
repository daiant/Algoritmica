# -*- coding: utf-8 -*-
import re
import numpy as np
from trie import Trie

class SpellSuggester:

    """
    Clase que implementa el Método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que admás se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary  = self.build_vocab(vocab_file_path, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)

    def suggest(self, term, distance="levenshtein", threshold=None):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate"]

        results = {} # diccionario termino:distancia
        # TODO
        for word in self.vocabulary:
            if distance == "levenshtein":
                dist = self.lev(word, term, threshold)
            elif distance == "restricted":
                dist = self.dam_lev(word, term, threshold)
            else:
                dist = self.intermedia(word, term, threshold)
            
            if(dist is not None):
                results[word] = dist
        return results

    def lev(self, a, b, threshold=None):
        if threshold is None: 
            threshold = 99
        d=dict()
        for i in range(len(a)+1):
            d[i]=dict()
            d[i][0] = i
        for j in range(len(b)+1):
            d[0][j] = j
        for i in range(1, len(a)+1):
            for j in range(1, len(b)+1):
                d[i][j] = min(d[i-1][j]  + 1,       #borrado
                             d[i][j-1]   + 1,       #insercion
                             d[i-1][j-1] + (not a[i-1]==b[j-1]))   #sustitucion
        dist = d[len(a)][len(b)]
        return dist if dist <= threshold else None ## Esto necesita mejora pero lo ponemos porque mira

    def dam_lev(self, a, b, threshold=None):
        d=dict()
        for i in range(len(a)+1):
            d[i]=dict()
            d[i][0] = i
        for j in range(len(b)+1):
            d[0][j] = j
        for i in range(1, len(a)+1):
            for j in range(1, len(b)+1):
                d[i][j] = min(d[i-1][j]  + 1,                             #borrado
                             d[i][j-1]   + 1,                             #insercion
                             d[i-1][j-1] + (not a[i-1]==b[j-1]))          #sustitucion
                if i>1 and j>1 and a[i-2] == b[j-1] and a[i-1] == b[j-2]: # condición restringida
                        d[i][j] = min(d[i][j], d[i-2][j-2] + 1)
        dist = d[len(a)][len(b)]
        return dist if dist <= threshold else None ## Esto necesita mejora pero lo ponemos porque mira
        
    def intermedia(self, a, b, threshold=None):
        CTE = 3
        d=dict()
        for i in range(len(a)+1):
            d[i]=dict()
            d[i][0] = i
        for j in range(len(b)+1):
            d[0][j] = j
        for i in range(1, len(a)+1):
            for j in range(1, len(b)+1):
                d[i][j] = min(d[i-1][j]  + 1,                             #borrado
                             d[i][j-1]   + 1,                             #insercion
                             d[i-1][j-1] + (not a[i-1]==b[j-1]))          #sustitucion
                if i>1 and j>1 and a[i-2] == b[j-1] and a[i-1] == b[j-2]: # condición restringida
                        d[i][j] = min(d[i][j], d[i-2][j-2] + 1)
                if i>2 and j>1 and a[i-3] == b[j-1] and a[i-1] == b[j-2]: # condición intermedia
                        d[i][j] = min(d[i][j], d[i-3][j-2] + 2)
                if i>1 and j>2 and a[i-1] == b[j-3] and a[i-2] == b[j-1]: # condición intermedia
                        d[i][j] = min(d[i][j], d[i-2][j-3] + 2)
        dist = d[len(a)][len(b)]
        return dist if dist <= threshold else None ## Esto necesita mejora pero lo ponemos porque mira

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el mtodo suggest para la búsqueda de términos y añade el trie
    """
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)
    
if __name__ == "__main__":
    spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    print(spellsuggester.suggest("alábese",distance="intermediate", threshold = 2))
    # cuidado, la salida es enorme print(suggester.trie)
