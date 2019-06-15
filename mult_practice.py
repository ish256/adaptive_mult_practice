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
        valVect1 = np.arange(3, 10)
        valVect2 = np.arange(3, 10)

    if mode == 2:
        # set up medium problems
        valVect1 = np.arange(2, 10)
        valVect2 = np.arange(10, 100)

    if mode == 3:
        # set up hard problem
        valVect1 = np.arange(10, 100)
        valVect2 = np.arange(10, 100)

    valArray1, valArray2 = np.meshgrid(valVect1, valVect2)
    valArray = np.array([valArray1.flatten(), valArray2.flatten()])

    # initialize prior probability as uniform distribution
    numChoices = np.size(valArray, 1)
    priorProbArray = np.ones(numChoices) * (1/numChoices)
    # print(priorProbArray)
    #  intialize correct vs incorrect counts (col1 for correct, col2 for incorrect )
    correctAndIncorrectCounts = np.ones((numChoices, 2))

    while True:

        # sample from distribution with problems
        drawInd = np.random.choice(numChoices, 1, p=priorProbArray.flatten())
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

        # penalize correct answers that take too long (i.e lose half correct points after 10 seconds)
        halfLife = 15
        correctAndIncorrectCounts[drawInd, 0] = correctAndIncorrectCounts[drawInd, 0] * (
            2**(-1*timeToAns/halfLife))

        # update probabilities based on counts
        incorrectAnswerPenaltyMultiple = 3
        conditionalProbArray = 1-betaincinv(
            correctAndIncorrectCounts[:, 0], correctAndIncorrectCounts[:, 1], 1/(1+incorrectAnswerPenaltyMultiple))

        # calculate posterior using bayesian update and assign as new prior
        priorProbArray = conditionalProbArray*priorProbArray / \
            sum(conditionalProbArray*priorProbArray)
        # print(priorProbArray)

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
