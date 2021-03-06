#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#
#Caio Roberto Ramos da Silva 00279459
#Lucas Romagnoli 00194235
#Trie inspirada no código que está disponível em http://www.geeksforgeeks.org/trie-insert-and-search/

import csv
import re
import tokenize
import io
import copy
import unidecode

def menu():
    """MENU DE OPÇÕES"""

    print("\n\n\n")
    print("1 - Abrir arquivo para dicionário")
    print("2 - Abrir arquivo para determinar sentimentos")
    print("3 - Buscar tweets por palavra - com problemas")
    print("4 - Buscar tweets por palavra e polaridade (+.-.0) - com problemas")
    print("5 - Sair do programa")
    print("\n\n\n")
    option = int(input("Digite a opção desejada: "))

    while option < 1 or option > 5:
        print("\n\nOpção Inválida, digite sua opção novamente!".upper())
        print("\n\n")
        print("1 - Abrir arquivo para dicionário")
        print("2 - Abrir arquivo para determinar sentimentos")
        print("3 - Buscar tweets por palavra")
        print("4 - Buscar tweets por palavra e polaridade (+.-.0)")
        print("5 - Sair do programa")
        print("\n\n\n")
        option = int(input("Digite a opção desejada: "))

    return option

class TrieNode:
    """Classe que define um nodo"""


    def __init__(self):
        # inicializa os filhos com vazio
        self.children = [None] * 26

        # se for T é uma folha, se F é um nodo intermediário
        self.isEndOfWord = False

        #sentimento inicializado com 0
        self.score = 0
        #sentimento acumulado inicializado com 0
        self.acc_score = 0
        #aparição em tweets inicializado com 0
        self.tweets_in = 0

class Trie:
    """Classe que contém funções para uma Trie"""

    def __init__(self):
        self.root = self.getNode()

    def getNode(self):

        # Retorna um nodo
        return TrieNode()

    def _charToIndex(self, ch):

        # Converte o caractere atual em deslocamento (para chaves minúsculas)

        return ord(ch) - ord('a')

    def insert(self, key, tweet_score):

        # Se a chave é um prefixo de um nodo, só marca ele como folha

        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            # adiciona o caractere atual na árvore, se nao estiver
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        # marca ultimo nodo como folha
        pCrawl.isEndOfWord = True
        pCrawl.acc_score = pCrawl.acc_score + int(tweet_score)
        pCrawl.tweets_in = pCrawl.tweets_in + 1
        pCrawl.score = pCrawl.acc_score / pCrawl.tweets_in

    def search(self, key):

        # Busca uma chave na trie, retorna T ou F
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl != None and pCrawl.isEndOfWord

    def editNode(self, key, tweet_score):

        # Buscar palavra na arvore
        # quando achar, alterar informações do último nodo (última letra da palavra)

        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        pCrawl.acc_score = pCrawl.acc_score + int(tweet_score)
        pCrawl.tweets_in = pCrawl.tweets_in + 1
        pCrawl.score = pCrawl.acc_score / pCrawl.tweets_in

    def searchScore(self, key):

        # Busca uma chave na trie, retorna T ou F
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return 0
            pCrawl = pCrawl.children[index]

        return pCrawl.score

class arquivoInvertido:
    """Classe relativa ao arquivo invertido"""
    def __init__(self):
        self.lista = []
        
    def insertWord(self):
        # Adiciona nova lista de documentos ao final da lista existente
        # para ser relacionado a nova palavra e retorna o indice de tal palavra no arquivo invertido
        novalista = []
        self.lista.append(novalista)
        return len(self.lista) - 1
        
    def insertDoc(self, indice, document):
        # Insere novo documento em que a palavra aparece na lista relativa a palavra
        self.lista[indice].append(document)
    
    def returnTweets(self, file, indice):
        # Retorna lista de tweets no indice passado
        listaTweets = []
        with open(file) as fp:
            print("\n{}\n".format(self.lista[indice]))
            for document in self.lista[indice]:
                for i, line in enumerate(fp):
                    if i == document:
                        listaTweets.append(line)
                    elif i > document:
                        break
        return listaTweets
    
    def returnTweetsFeel(self, file, indice, sentimento):
        # Retorna lista de tweets no indice com sentimento específico
        # file é o nome do arquivo com tweets com sentimento, indice é o indice dado pra palavra, sentimento é o desejado para pesquisa
        listaTweets = []
        with open(file) as fp:
            for document in self.lista[indice]:
                for i, line in enumerate(fp):
                    if i == document:
                        tweetAndFeel = line.split(';')
                        if tweetAndFeel[1] == sentimento:
                            listaTweets.append(line)
                    elif i > document:
                        break
        
        return listaTweets

class TrieNodeArquivo:
    """Classe que define um nodo na estrutura de acesso ao arquivo invertido"""

    def __init__(self):
        # inicializa os filhos com vazio
        self.children = [None] * 26

        # se for T é uma folha, se F é um nodo intermediário
        self.isEndOfWord = False

        #indice inicializado como -1
        self.indice = -1

class TrieArquivo:
    """Classe que contém funções para Trie de acesso ao arquivo invertido"""

    def __init__(self):
        self.root = self.getNode()
        self.lastIndex = 0
        
    def getNode(self):

        # Retorna um nodo
        return TrieNodeArquivo()

    def _charToIndex(self, ch):

        # Converte o caractere atual em deslocamento (para chaves minúsculas)

        return ord(ch) - ord('a')

    def insert(self, key):

        # Se a chave é um prefixo de um nodo, só marca ele como folha

        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            # adiciona o caractere atual na árvore, se nao estiver
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        # Retorna true para chave nova
        if not pCrawl.isEndOfWord:
            pCrawl.isEndOfWord = True
            pCrawl.indice = self.lastIndex
            self.lastIndex = self.lastIndex + 1
            return True, pCrawl.indice
        return False, pCrawl.indice

    def search(self, key):

        # Busca uma chave na trie, retorna T ou F
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl != None and pCrawl.isEndOfWord


    def searchIndice(self, key):

        # Busca uma chave na trie, retorna o indice
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return -1
            pCrawl = pCrawl.children[index]

        return pCrawl.indice

def leCSVDict(filename):

    try:
        with open(filename) as csvfile:
            tweet_reader = csv.reader(csvfile)
            content_list = list(tweet_reader)

        return content_list
    except IOError:
        print("Erro ao abrir o arquivo especificado!!!")
        exit(1)

def leCSVTweet(filename):

    try:
        with open(filename) as csvfile:
            tweet_reader = csv.reader(csvfile)
            content_list = list(tweet_reader)

        return content_list
    except IOError:
        print("Erro ao abrir o arquivo especificado!!!")
        exit(1)

def writeCSVTweet(filename, orig_tweet, tweet_score):

    if len(orig_tweet) == len(tweet_score):
        out_file = filename.strip(".csv")+"_out.csv"
        with open(out_file, 'w') as f:
            for item in range(len(orig_tweet)):
                f.write(orig_tweet[item]+";"+str(tweet_score[item])+"\n")
    else:
        print("Erro ao escrever csv, numero de tweets e numero de sentimentos é diferente")
        exit(1)

def writeCSVOrigTweet(orig_tweet):

    with open("todosTweets.csv", 'a') as f:
        for item in range(len(orig_tweet)):
            f.write(orig_tweet[item]+"\n")
        print("Caractere separador é ';'")

def writeCSVSearchResults(filename, tweets):
    out_file = filename.strip(".csv")+"_search.csv"
    with open(out_file, 'w') as f:
        for item in range(len(tweets)):
            f.write(tweets[item])

def tweetnScore(content, scores):



    if scores:
        tweets = []
        score = []
        for line in content:
            tweets.append(line[0])
            score.append(line[1])
        return tweets, score

    else:
        tweets = []
        for line in content:
            tweets.append(line[0])
        return tweets

def formatTweet(tweets, total_tweets):

    for tweet in range(total_tweets):
        # remove acentos das palavras e converte caracteres utf8 pra asc
        tweets[tweet] = unidecode.unidecode(tweets[tweet])
        # Troca caracteres especificados por espaço
        tweets[tweet] = tweets[tweet].translate({ord(i): ' ' for i in "?!#@$.,;:-\'\"`(){}[]~*^%&1234567890=|/+\\<>"}).lower()
        # Remove palavras de tamanho <= 2
        tweets[tweet] = re.sub(r'\b\w{1,2}\b', '', tweets[tweet])

        # tweets estão sem palavras de tamanho <= 2, sem caracteres especiais soltos e foram transformados para minúsculo

    return tweets

def addDict(tweets, trie, tweet_score):

    tokens = []

    for tweet in range(len(tweets)):
        readline = io.StringIO(tweets[tweet]).readline
        for token in tokenize.generate_tokens(readline):
            if len(token[1]) > 2 and len(token[1].split()) > 0:
                tokens.append(token[1])
                # adicionar tokens ao dicionario, se nao existir
                if not trie.search(token[1]):
                    trie.insert(token[1], tweet_score[tweet])
                else:
                    # alterar informações do token no dicionário caso já exista
                    trie.editNode(token[1], tweet_score[tweet])


def calculateSentiment(tweets, trie, trieArquivo, arqInvert):

    sum = [0]*len(tweets)
    index = 0
    for tweet in range(len(tweets)):
        
        tweets[tweet] = tweets[tweet].split()
        for word in tweets[tweet]:
            Nexistia, indice = trieArquivo.insert(word)
            if Nexistia:
                indexxx = arqInvert.insertWord()
            arqInvert.insertDoc(indice, index)
            found = trie.searchScore(word)
            if (found != 0):
                # se achou a palavra e score não é zero, somar o score dela
                sum[tweet] = sum[tweet] + found
        index = index + 1
    # normaliza sentimentos para -1, 0, 1
    for soma in range(len(sum)):
        if sum[soma] > 0.1:
            sum[soma] = 1
        elif sum[soma] < -0.1:
            sum[soma] = -1
        else:
            sum[soma] = 0
            # se não achou a palavra ou score é zero, não fazer nada (somar 0)

    return sum, trieArquivo, arqInvert


def main():

    # inicializa uma Trie
    trie = Trie()
    trieArquivo = TrieArquivo()
    arqInvert = arquivoInvertido()

    flag_end = 0
    while flag_end == 0:
        option = menu()

        if option == 1:
            print("\n\nAbertura de CSV para adicionar ao dicionário")
            input_file = input("Digite o nome do arquivo CSV (para dicionario): ")
            content_list = leCSVDict(input_file)
        elif option == 2:
            print("\n\nAbertura de CSV para classificação de tweets")
            input_file = input("Digite o nome do arquivo CSV (para calculo de sentimento): ")
            content_list = leCSVTweet(input_file)
        elif option == 3:
            print("\n\nAbertura de CSV para pesquisa por palavra")
            input_file = input("Digite o nome do arquivo CSV no qual deseja pesquisar: ")
            searchWord = input("\nDigite a palavra que deseja pesquisar: ")
            content_list = leCSVTweet(input_file)
        elif option == 4:
            print("\n\nAbertura de CSV para pesquisa por palavra e sentimento")
            input_file = input("Digite o nome do arquivo CSV no qual deseja pesquisar: ")
            searchWord = input("\nDigite a palavra que deseja pesquisar: ")
            searchFeel = float(input("\nDigite o sentimento dos tweets para pesquisar: "))
            content_list = leCSVTweet(input_file)
        elif option == 5:
            flag_end = 1

        if option == 1:
            scores = 1
            # tweets em uma lista e scores em outra
            tweet_content, tweet_score = tweetnScore(content_list, scores)
            writeCSVOrigTweet(tweet_content)

            # número de tweets no arquivo
            total_tweets = len(tweet_content)

            #formata os tweets (minúsculo, sem pontuação e somente palavras de tamanho > 2)
            formatted_tweets = formatTweet(tweet_content, total_tweets)

            # verifica se as palavras estão na trie
            # se estiver, altera as informações (acc_score, tweets_in, score)
            # se não estiver, adiciona à árvore com as informações do tweet (acc_score = score do tweet, tweets_in = 1, score = acc_score / tweets_in)
            addDict(formatted_tweets, trie, tweet_score)

        if option == 2:

            scores = 0
            # tweets em uma lista e scores em outra
            tweet_content = tweetnScore(content_list, scores)
            writeCSVOrigTweet(tweet_content)

            tweets_copy = copy.deepcopy(tweet_content)

            total_tweets = len(tweet_content)

            formatted_tweets = formatTweet(tweet_content, total_tweets)

            # lista de somas referentes ao tweet. Por exemplo o tweet da linha 0 terá sua soma em tweet_sum[0]
            tweet_sum, trieArquivo, arqInvert = calculateSentiment(formatted_tweets, trie, trieArquivo, arqInvert)

            writeCSVTweet(input_file, tweets_copy, tweet_sum)

        if option == 3:
            scores = 0
            searchResults = []
            #if not (trieArquivo and arqInvert):

            scores = 0
            # tweets em uma lista e scores em outra
            tweet_content = tweetnScore(content_list, scores)
            total_tweets = len(tweet_content)
            formatted_tweets = formatTweet(tweet_content, total_tweets)
            tweet_sum, trieArquivo, arqInvert = calculateSentiment(formatted_tweets, trie, trieArquivo, arqInvert)
            
            indice = trieArquivo.searchIndice(searchWord)
            if indice != -1:
                searchResults = arqInvert.returnTweets(input_file, indice)
            
            
            writeCSVSearchResults(input_file, searchResults)

        if option == 4:
            scores = 0
            searchResults = []
            scores = 0
            # tweets em uma lista e scores em outra
            tweet_content = tweetnScore(content_list, scores)
            total_tweets = len(tweet_content)
            formatted_tweets = formatTweet(tweet_content, total_tweets)
            tweet_sum, trieArquivo, arqInvert = calculateSentiment(formatted_tweets, trie, trieArquivo, arqInvert)
            indice = trieArquivo.searchIndice(searchWord)
            if indice != -1:
                if searchFeel > 0.1:
                    searchFeel = 1;
                if searchFeel < -0.1:
                    searchFeel = -1;
                if -0.1 < searchFeel < 0.1:
                    searchFeel = 0;
                searchResults = arqInvert.returnTweetsFeel(input_file, indice, searchFeel)
            
            
            writeCSVSearchResults(input_file, searchResults)
    exit(0)

if __name__ == "__main__":
    main()