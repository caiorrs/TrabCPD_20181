import csv
import re
# from src.importer import Importer

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
        tweet_content[item] = re.sub(r'\b\w{1,2}\b', '', tweet_content[item])
        tweet_score[item] = ' '.join(tweet_score[item].split())

    #for tweet in range(len(tweet_content)):
    #    print("{},{}".format(tweet_content[tweet], tweet_score[tweet]))


    total_tweets = len(tweet_content)

    for tweet in range()


if __name__ == "__main__":
    main()
