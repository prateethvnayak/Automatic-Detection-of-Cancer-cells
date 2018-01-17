import image_predict as pre


def predict(path):
    number, score = pre.predict(path)
    countab = 0
    countn = 0
    for i in range(0, number.__len__()):
        print 'Image number ', i + 1
        if number[i] == 1:
            print 'ABNORMAL:', score[i] * 100, '%'
            countab += 1
        else:
            print 'NORMAL:', score[i] * 100, '%'
            countn += 1

    return countab, countn

