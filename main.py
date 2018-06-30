import csv
import re
import tokenize
import io
import copy
import unidecode


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
        tweets[tweet] = tweets[tweet].translate({ord(i): ' ' for i in "?!@#$.,;:-\'\"`(){}[]~*^%&1234567890=|/+\\"}).lower()
        # Remove palavras de tamanho <= 2
        tweets[tweet] = re.sub(r'\b\w{1,2}\b', '', tweets[tweet])
        #remove acentos das palavras
        tweets[tweet] = unidecode.unidecode(tweets[tweet])

        # tweets estão sem palavras de tamanho <= 2, sem caracteres especiais soltos e foram transformados para minúsculo


    return tweets

def addDict(tweets, scores, total_tweets):
    #tweets já formatados

    words_n_scores = {}

    for tweet in range(total_tweets):
        words = tweets[tweet].split()
        for word in words:
            #palavra não existe no dicionário
            if word not in words_n_scores.keys():
                words_n_scores[word] = [float(scores[tweet]), 1*float(scores[tweet]), 1]
            #palavra já está no dicionário
            #else:
                #print("!!!JA ESTÁ NO DICIONARIO!!!")
    print("DICIONARIO")
    print(words_n_scores)


    return words_n_scores

def tokenizer(tweets):

    tokens = []

    for tweet in range(len(tweets)):
        readline = io.StringIO(tweets[tweet]).readline
        for token in tokenize.generate_tokens(readline):
            if len(token[1]) > 2 and len(token[1].split()) > 0:
                print(token[1])
                tokens.append(token[1])

    return tokens


def main():

    content_list = leCSVDict()

    content_list_copy = copy.deepcopy(content_list)

    tweet_content, tweet_score = tweetnScore(content_list)

    total_tweets = len(tweet_content)

    #formata os tweets (minúsculo, sem pontuação e somente palavras de tamanho > 2)
    formatted_tweets = formatTweet(tweet_content, total_tweets)

    print(formatted_tweets)

    tokens = tokenizer(formatted_tweets)

    #word_dict = addDict(formatted_tweets, tweet_score, total_tweets)

    # Quando precisar fazer a busca de chaves em tweet, será necessário remover os acentos dos tweets (para comparação)


if __name__ == "__main__":
    main()
