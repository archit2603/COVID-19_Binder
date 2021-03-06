import cPickle
import numpy as np
import sys

infiles = sys.argv[1:-1]
outfile = sys.argv[-1]


#---- load PKL file ----#
predictions = []
for _ in infiles:
    f = open(_, 'rb')
    load = cPickle.load(f)
    predictions.extend(load)

##calculate the average of the predicted matrices
#finalPrediction = np.average(predictions, axis=0, weights=np.outer(modelWeights, tpWeights).flatten() )
finalPrediction = np.average(predictions, axis=0 )

##set the element (i, j) to 0.000001 when |i-j|<=5, we use 0.0001 instead of 0 here to distinguish our prediction file from that generated by others
for offset in np.arange(-5, 6):
    start = max(0, -offset)
    end = min(finalPrediction.shape[0], finalPrediction.shape[0] - offset)
    i = np.arange(start, end)
    j = i + offset
    finalPrediction[i, j] = 0.000001

assert (finalPrediction <=1).all()
assert (finalPrediction >=0).all()

##write the final prediction result
np.savetxt(outfile, finalPrediction, fmt='%10.6f', delimiter=' ')

