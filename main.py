import csv
import re
from tokenize import generate_tokens
import io
import copy


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
        #print("TWEET INTEIRO: {}".format(tweets[tweet]))

        tweets[tweet] = tweets[tweet].translate({ord(i): ' ' for i in '?!@#$.,;:-\'\"(){}[]~'}).lower()

        tweets[tweet] = re.sub(r'\b\w{1,2}\b', '', tweets[tweet])

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


def main():

    content_list = leCSVDict()

    content_list_copy = copy.deepcopy(content_list)

    tweet_content, tweet_score = tweetnScore(content_list)

    total_tweets = len(tweet_content)

    #formata os tweets (minúsculo, sem pontuação e somente palavras de tamanho > 2)
    formatted_tweets = formatTweet(tweet_content, total_tweets)

    print(formatted_tweets)

    word_dict = addDict(formatted_tweets, tweet_score, total_tweets)


if __name__ == "__main__":
    main()
