#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import csv
import re
import tokenize
import io
import copy
import unidecode


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


        # Busca uma chave na trie, retorna T ou F
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

        print("PALAVRA: {} --- ACC_SCORE: {} --- TWEETS_IN: {} --- SCORE: {}".format(key, pCrawl.acc_score, pCrawl.tweets_in, pCrawl.score))




def leCSVDict():

    input_file = input("Digite o nome do arquivo CSV (para dicionario): ")

    with open(input_file) as csvfile:
        tweet_reader = csv.reader(csvfile)
        content_list = list(tweet_reader)

    return content_list

def leCSVTweet():
    input_file = input("Digite o nome do arquivo CSV (para calculo de sentimento): ")

    with open(input_file) as csvfile:
        tweet_reader = csv.reader(csvfile)
        content_list = list(tweet_reader)

    return content_list

def tweetnScore(content):

    tweet = []
    score = []

    for line in content:
        tweet.append(line[0])
        score.append(line[1])

    return tweet, score


def formatTweet(tweets, total_tweets):

    for tweet in range(total_tweets):
        # Troca caracteres especificados por espaço
        tweets[tweet] = tweets[tweet].translate({ord(i): ' ' for i in "?!#@$.,;:-\'\"`(){}[]~*^%&1234567890=|/+\\<>“”…"}).lower()
        # Remove palavras de tamanho <= 2
        tweets[tweet] = re.sub(r'\b\w{1,2}\b', '', tweets[tweet])
        #remove acentos das palavras
        tweets[tweet] = unidecode.unidecode(tweets[tweet])


        # tweets estão sem palavras de tamanho <= 2, sem caracteres especiais soltos e foram transformados para minúsculo


    return tweets

def tokenizer(tweets, trie, tweet_score):

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
                    trie.editNode(token[1], tweet_score[tweet])
                    print("PALAVRA JA NA TRIE!!!")
                #alterar informações do token no dicionário caso já exista



    return tokens


def main():

    content_list = leCSVDict()

    content_list_copy = copy.deepcopy(content_list)

    tweet_content, tweet_score = tweetnScore(content_list)

    total_tweets = len(tweet_content)

    #formata os tweets (minúsculo, sem pontuação e somente palavras de tamanho > 2)
    formatted_tweets = formatTweet(tweet_content, total_tweets)

    print(formatted_tweets)

    trie = Trie()
    tokens = tokenizer(formatted_tweets, trie, tweet_score)

    # Quando precisar fazer a busca de chaves em tweet, será necessário remover os acentos dos tweets (para comparação)


if __name__ == "__main__":
    main()
