import SAR_lib
import spellsuggest
import collections
import re
import time
import statistics
import math
output = ""

def write_vocab(vocab):
    f = open("vocabulario.txt", "w", encoding="utf-8")
    s = ""
    for word in vocab:
        s += word + " "
    f.write(s)
    f.close()
    return "vocabulario.txt"

def measureTime(functionName, palabra, cutVocab, threshold, repetitions):
    listaVal = []
    vocabulary_file_path = write_vocab(cutVocab)
    ss = spellsuggest.TrieSpellSuggester(vocabulary_file_path)

    for i in range(repetitions):
        t1 = time.process_time()
        valActual = ss.suggest(palabra, functionName, threshold)
        t2 = time.process_time() - t1
        listaVal.append(t2)
    media = statistics.mean(listaVal)
    mediana = statistics.median(listaVal)
    desvTip = statistics.stdev(listaVal)
    #print("media, mediana y desviación típica:", listaVal)
    return (media, mediana, desvTip)
def generateTable(inputWord, divisorTalla, maxThreshold, reps=1):
    #Este código se encarga de ordenar el vocabulario que se va a usar
    #print("palabra: ", inputWord)
    vocab_file_path = "./corpora/quijote.txt"
    tokenizer = re.compile("\W+")
    with open(vocab_file_path, "r", encoding='utf-8') as fr:
        c = collections.Counter(tokenizer.split(fr.read().lower()))
        if '' in c:
            del c['']
        reversed_c = [(freq, word) for (word,freq) in c.items()]
        sorted_reversed = sorted(reversed_c, reverse=True)
        sorted_vocab = [word for (freq,word) in sorted_reversed]
        #Vocabulario ya ordenado
    functions = ["levenshtein", "lev_trie", "restricted", "intermediate"]
    measures = {}
    for funcname in functions:
        measures[funcname] = {} # asocia a cada talla una lista de (tiempo, estados)
    for funcname in functions:
        for n in range(1, divisorTalla+1):
            #print("El divisor de la talla es ", n)
            for thr in range(0, maxThreshold+1):
                if thr == 0:
                    thr = None
                tallaF = sorted_vocab[:(math.ceil(len(sorted_vocab)/n))]
                #print("Función", funcname, "- talla de diccionario:", math.ceil(len(sorted_vocab)/n), "- margen:", thr)
                measures[funcname] = measureTime(funcname, inputWord, tallaF, None, reps)
    #print(measures)



#código prueba para asegurar que funciona
if __name__ == "__main__":
    generateTable("casa",2,2,3)
