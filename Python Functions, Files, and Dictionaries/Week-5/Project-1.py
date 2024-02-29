
'''
Week-5 Project-1
'''

punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
def strip_punctuation(ss):
    for c in ss:
        if(c in punctuation_chars):
            ss = ss.replace(c,"")
    return ss

# list of positive words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())
print(positive_words)

def get_pos(string):
    sents = string.split('\n')
    count = 0
    for sent in sents:
        s = strip_punctuation(sent)
        words = s.split()
        for word in words:
            if (word.lower() in positive_words):
                count += 1      
    return count


negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())
            
def get_neg(string):
    sents = string.split('\n')
    count = 0
    for sent in sents:
        s = strip_punctuation(sent)
        words = s.split()
        for word in words:
            if (word.lower() in negative_words):
                count += 1      
    return count

result = open("resulting_data.csv",'w')
header = "Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n"
result.write(header)

with open("project_twitter_data.csv",'r') as file:
    lines = file.readlines()
    for line in lines:
        if(line == lines[0]):
            continue
        lst = line.split(',')
        tweet_text = lst[0]
        retweet_count = lst[1]
        reply_count = lst[2]
        positive_count = get_pos(tweet_text)
        negative_count = get_neg(tweet_text)
        net_score = positive_count - negative_count
        string_data = "{},{},{},{},{}\n".format(retweet_count,reply_count.replace('\n',''),positive_count,negative_count,net_score)
        result.write(string_data)
result.flush()
result.close()

