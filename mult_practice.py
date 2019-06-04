import numpy as np
import time
import pandas as pd
import argparse
from scipy.special import betaincinv


def mult_practice(mode=1):

    valVect = np.arange(2, 10)
    valArray = np.meshgrid(valVect, valVect)

    # make df to hold data
    df = pd.DataFrame(
        columns=['timeStamp', 'mode', 'topVal', 'botVal', 'ansTime', 'correct'])

    # set up problem according to mode
    if mode == 1:
        # set up easy problems
        # val1 = np.random.randint(3, 9+1)
        # val2 = np.random.randint(3, 9+1)
        valVect1 = np.arange(3, 10)
        valVect2 = np.arange(3, 10)
        #valVect1 = np.arange(4, 6)
        #valVect2 = np.arange(4, 6)

    if mode == 2:
        # set up medium problems
        # val1 = np.random.randint(10, 99+1)
        # val2 = np.random.randint(3, 9+1)
        valVect1 = np.arange(2, 10)
        valVect2 = np.arange(10, 100)

    if mode == 3:
        # set up hard problem
        # val1 = np.random.randint(10, 99+1)
        # val2 = np.random.randint(10, 99+1)
        valVect1 = np.arange(10, 100)
        valVect2 = np.arange(10, 100)

    valArray1, valArray2 = np.meshgrid(valVect1, valVect2)
    valArray = np.array([valArray1.flatten(), valArray2.flatten()])

    # initialize probability array
    numChoices = np.size(valArray, 1)
    probArray = np.ones((numChoices, 1)) * (1/numChoices)
    print(probArray)
    #  intialize correct vs incorrect counts (col1 for correct, col2 for incorrect )
    correctAndIncorrectCounts = np.ones((numChoices, 2))

    while True:

        # sample from distribution with problems
        drawInd = np.random.choice(numChoices, 1, p=probArray.flatten())
        print(drawInd)
        val1 = valArray[0, drawInd]
        val2 = valArray[1, drawInd]

        strPt1 = '{val1}'.format(val1=int(val1))
        strPt1 = strPt1.rjust(4)
        print(strPt1+'\n x {val2} \n _____'.format(val2=int(val2)))

        # get response and time it
        start = time.time()
        answer = input("Enter Answer:")
        end = time.time()

        # calc time it took
        timeToAns = end - start

        # check if answer is correct
        successCheck = 1 if val1*val2 == int(answer) else 0
        print('Correct' if successCheck == 1 else 'Incorrect')

        if successCheck:
            correctAndIncorrectCounts[drawInd, 0] += 1
        else:
            correctAndIncorrectCounts[drawInd, 1] += 1

        # update probabilities based on counts
        probArray = 1-betaincinv(
            correctAndIncorrectCounts[:, 0], correctAndIncorrectCounts[:, 1], 1/(1+2))
        probArray = probArray/sum(probArray)
        print(probArray)
        # add response to db
        numAnsInDB = df.shape[0]  # total number of responses
        curTime = pd.Timestamp.now().strftime('%B %d, %Y, %r')
        df.loc[numAnsInDB] = [curTime, mode,
                              val1, val2, timeToAns, successCheck]

        # save out response
        df.to_csv('mult_practice_history.csv')


if __name__ == "__main__":

    # parse mode input
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="modes:1,2,3", type=int)
    args = parser.parse_args()

    # call main function
    mult_practice(args.mode)
