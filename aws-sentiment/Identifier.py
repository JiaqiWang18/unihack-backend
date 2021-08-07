import math
def isRenZha(dict):
    GAO_JI_ZHA = "请注意了，他/她对你忽冷忽热，可能是高级渣，请理智对待"
    DI_JI_ZHA = "他/她对你态度一直不好，如果不是死党的话，请保持距离"
    HAO_REN = "他/她对你一直很好，在保持理智的情况下，可以相信"
    HAI_XING = "他/她大部分时间对你是好的，但是就是那一小部分不好的需要注意一下"
    PING_DAN = "平平淡淡，普通朋友"

    neg = dict['NEGATIVE']
    pos = dict['POSITIVE']
    neu = dict['NEUTRAL']
    mix = dict['MIXED']
    total = neg + pos + mix
    
    score = pos/total
    neu_score = neu/(total+neu)

    if(neu_score > 0.8):
        return 0, PING_DAN
    if(score < 0.3):
        return abs(1-score)*10,DI_JI_ZHA
    if(0.3 <= score and score <= 0.6):
        return abs(1-score)*10,GAO_JI_ZHA
    if(0.6 < score and score < 0.85):
        return abs(1-score)*10,HAI_XING
    if(score >= 0.85):
        return abs(1-score)*10,HAO_REN