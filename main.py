import random
from copy import deepcopy


def getWords():
    with open("word_list.txt", "r", encoding="utf-8") as f:
        words = f.read().split()
    return words


def getAnswers():
    with open("answer_list.txt", "r", encoding="utf-8") as f:
        answers = f.read().split()
    return answers


def getWordsAndAnswers():
    return getWords(), getAnswers()


def chooseWord(words):
    return random.choice(words)


def getGreenPos(selectedWord, correctWord):
    pos = []
    for i, (s, c) in enumerate(zip(selectedWord, correctWord)):
        if s == c:
            pos.append(i)
    return pos


def greedFilter(selectedWord, correctWord, words):
    pos = getGreenPos(selectedWord, correctWord)
    if len(pos) == len(selectedWord):
        return words

    wordList = []
    for word in words:
        matchCount = 0
        if word == selectedWord:
            continue

        for p in pos:
            if selectedWord[p] == word[p]:
                matchCount += 1

        if matchCount == len(pos):
            wordList.append(word)

    return wordList


def getYelloPos(selectedWord, correctWord):
    pos = []
    for i in range(len(selectedWord)):
        if selectedWord[i] in correctWord:
            pos.append(i)
    return pos


def yellowFilter(selectedWord, correctWord, words):
    pos = getYelloPos(selectedWord, correctWord)

    wordList = []
    for word in words:
        matchCount = 0
        for p in pos:
            if selectedWord[p] in word:
                matchCount += 1

        if matchCount >= len(pos):
            wordList.append(word)

    return wordList


def getGrayPos(selectedWord, correctWord):
    pos = []
    for i in range(len(selectedWord)):
        if selectedWord[i] not in correctWord:
            pos.append(i)

    return pos


def grayFilter(selectedWord, correctWord, words):
    pos = getGrayPos(selectedWord, correctWord)

    wordList = deepcopy(words)
    for word in words:
        matchCount = 0
        for p in pos:
            if selectedWord[p] in word:
                matchCount += 1

        # グレーに少しでもヒットした単語は候補から消す必要がある
        if matchCount > 0:
            wordList.remove(word)

    return wordList


def wordFiltering(selectedWord, correctWord, words):
    wordList = greedFilter(selectedWord, correctWord, words)
    wordList = yellowFilter(selectedWord, correctWord, wordList)
    wordList = grayFilter(selectedWord, correctWord, wordList)

    return wordList


def getSolveTime(correctWord, words, maxTry=100):
    wordList = deepcopy(words)

    for i in range(1, maxTry + 1):
        selectedWord = chooseWord(wordList)
        wordList = wordFiltering(selectedWord, correctWord, wordList)
        if len(wordList) == 1:
            return i

    return -1


def totallingSolveTime(times):
    tmp = [0] * (max(times) + 1)
    for t in times:
        if t == -1:
            tmp[0] += 1
        else:
            tmp[t] += 1
    return tmp


words, answers = getWordsAndAnswers()

times = []
for correctWord in answers:
    time = getSolveTime(correctWord, words, maxTry=10)
    times.append(time)

# 解くのにかかった手数を集計して表示
total = totallingSolveTime(times)
print("解けなかった:", total[0])
for i in range(1, len(total)):
    print(f"{i}回:", total[i])
