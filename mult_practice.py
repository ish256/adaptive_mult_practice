import numpy as np
import time
import pandas as pd
import argparse


def mult_practice(mode):

    # make df to hold data
    df = pd.DataFrame(
        columns=['timeStamp', 'mode', 'topVal', 'botVal', 'ansTime', 'correct'])

    while True:

        # set up problem according to mode
        if mode == 1:

            # set up easy problems
            val1 = np.random.randint(3, 9+1)
            val2 = np.random.randint(3, 9+1)

        if mode == 2:

            # set up medium problems
            val1 = np.random.randint(10, 99+1)
            val2 = np.random.randint(3, 9+1)

        if mode == 3:

             # set up hard problem
            val1 = np.random.randint(10, 99+1)
            val2 = np.random.randint(10, 99+1)

        strPt1 = '{val1}'.format(val1=val1)
        strPt1 = strPt1.rjust(4)
        print(strPt1+'\n x {val2} \n _____'.format(val2=val2))

        # get response and time it
        start = time.time()
        answer = input("Enter Answer:")
        end = time.time()

        # calc time it took
        timeToAns = end - start

        # check if answer is correct
        successCheck = 1 if val1*val2 == int(answer) else 0
        print('Correct' if successCheck == 1 else 'Incorrect')

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
