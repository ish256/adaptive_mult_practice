import numpy as np
from scipy.special import betaincinv


# create array holding all possible multiplication combinations
valVect = np.arange(2, 10)
valArray1, valArray2 = np.meshgrid(valVect, valVect)
valArray = np.array([valArray1.flatten(), valArray2.flatten()])

print(valArray.shape)

# initial drawing scheme
numChoices = np.size(valArray, 1)
probArray = np.ones((numChoices, 1)) * (1/numChoices)

# correct vs incorrect counts
correctAndIncorrectCounts = np.ones((numChoices, 2))

for k in np.arange(50):

    drawInd = np.random.choice(numChoices, 1, p=probArray.flatten())

    # update count array depending on response
    correctFlag = 1
    if correctFlag:
        correctAndIncorrectCounts[drawInd, 0] += 1
    else:
        correctAndIncorrectCounts[drawInd, 1] += 1

    # update probabilities based on counts
    probArray = 1-betaincinv(
        correctAndIncorrectCounts[:, 0], correctAndIncorrectCounts[:, 1], 1/(1+2))
    probArray = probArray/sum(probArray)

print(probArray)
