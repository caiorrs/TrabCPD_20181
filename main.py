import csv
import re


def main():
    input_file = input("Digite o nome do arquivo de entrada: ")

    with open(input_file) as csvfile:
        tweet_reader = csv.reader(csvfile)
        content_list = list(tweet_reader)

    tweet_content = []  # contem os tweets, sem o sentimento
    tweet_score = []  # contem apenas os sentimentos

    for item in content_list:
        tweet_content.append(item[0])
        tweet_score.append(item[1])

    # remove palavras de tamanho <= 2
    for item in range(len(tweet_content)):
        print("TWEET INTEIRO: {}".format(tweet_content[item]))
        tweet_content[item] = re.sub(r'\b\w{1,2}\b', '', tweet_content[item])

        tweet_content[item] = tweet_content[item].translate({ord(i): ' ' for i in '!@#$.,;:-\'\"'}).lower()
        print("TWEET REDUZIDO: {}\n\n\n".format(tweet_content[item]))
        tweet_score[item] = ' '.join(tweet_score[item].split())

    # for tweet in range(len(tweet_content)):
    #    print("{},{}".format(tweet_content[tweet], tweet_score[tweet]))

    total_tweets = len(tweet_content)

    for tweet in range(total_tweets):
        tweet_words = tweet_content[tweet].split()
        num_words = len(tweet_words)
        for word in range(num_words):
            # print("PALAVRA: {}---SCORE: {}".format(tweet_words[word], tweet_score[tweet]))
            exit()


if __name__ == "__main__":
    main()
