# -*- coding: utf-8 -*-
from API import getSentiment
from Identifier import isRenZha

def main():
    FILENAME = "input.txt"
    DICT = {}
    TARGET_SENTI = {"NEGATIVE":0,
                    "POSITIVE":0,
                    "NEUTRAL":0,
                    "MIXED":0}

    with open(FILENAME) as f:
        content = f.readlines()
        
    content = [x.strip() for x in content] 

    # TARGET_SENTI = {'NEGATIVE': 4, 'POSITIVE': 1, 'NEUTRAL': 2, 'MIXED': 0}
    for sentence in content:
        senti = getSentiment(sentence)["Sentiment"]
        DICT[sentence] = senti
        TARGET_SENTI[senti] += 1

    print(DICT)
    print(TARGET_SENTI)
    score, report = isRenZha(TARGET_SENTI)
    print("他/她的人渣指数(1~10):", "{:.2f}".format(score))
    print("分析:", report)
main()