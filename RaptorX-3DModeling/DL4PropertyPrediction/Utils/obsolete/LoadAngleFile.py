import numpy as np
import sys
import os

##this script reads local structure properties of a protein, the input is generated by Yujuan's code

def LoadAngleFile(file):

	fh = open(file, 'r')
	content = [ line.strip() for line in list(fh) ]
	fh.close()

	## the columns of an angle file shall have the following format
	"""
		Missing   Site   Res     SSE     CLE     Phi     	Psi     	Ome     	Theta   	Tau
		0       1       S       L       R       -567.228217     163.860412      -178.991919     -567.228217     -567.228217
		0       2       W       L       R       -120.908957     146.914399      178.129174      45.619312       -567.228217
		0       3       K       L       E       -153.259497     152.810022      -179.586798     44.832083       163.033597
		0       4       R       T       C       -55.053264      152.766129      178.343226      63.158484       -81.372650
		0       5       N       T       N       53.307653       32.783893       179.838307      89.056784       16.608994
		0       6       K       S       M       -113.751081     -31.616543      178.716756      81.103680       99.983842
		0       7       F       E       L       -125.149226     152.108011      178.433828      46.036281       35.768649
		0       8       R       E       E       -148.722436     154.831088      179.533233      42.680604       178.563212
		0       9       L       E       D       -102.209239     137.204447      -179.096700     60.847391       -123.268429
		0       10      T       E       E       -130.066019     129.438719      179.500802      51.261015       -167.185346
		0       11      Y       E       C       -66.686403      141.406750      178.828897      64.551367       -122.378681
		0       12      V       L       E       -144.994098     147.789405      -178.032688     47.818339       178.040420
		0       13      A       S       B       -84.656898      -25.420546      -179.376253     77.731713       -142.030883
	"""

	MissingList = []
	IndexList = []
	sequence = ''
	SS = ''
	CLE = ''
	phiList = []
	psiList = []
	thetaList = []
	tauList = []
	omgList = []

	pi = np.pi

	for line in content[1:]:
		fields = line.split()
		if len(fields) not in [3, 10]:
			print 'incorrect format in line: ', line
			exit(-1)

		Missing = np.int32(fields[0])
		Index = np.int32(fields[1])
		Residue = fields[2]
		
		if len(fields) == 10:
			ss = fields[3]
			cle = fields[4]
			phi = np.float32(fields[5])/180.0 * np.float32(np.pi)
			psi = np.float32(fields[6])/180.0 * np.float32(np.pi)
			omg = np.float32(fields[7])/180.0 * np.float32(np.pi)
			theta = np.float32(fields[8])/180.0 * np.float32(np.pi)
			tau = np.float32(fields[9])/180.0 * np.float32(np.pi)
		else:
			ss='L'
			cle='R'
			phi = 0
			psi = 0
			theta =0
			tau = 0
			omg = 0

		MissingList.append(Missing)
		IndexList.append(Index)
		sequence += Residue
		SS += ( 'L' if ss == 'C' else ss )
		CLE += cle
		phiList.append(phi)
		psiList.append(psi)
		thetaList.append(theta)
		tauList.append(tau)
		omgList.append(omg)

	AngleInfo = dict()
	AngleInfo['sequence'] = sequence
	AngleInfo['Missing'] = np.array(MissingList).astype(np.int32)
	AngleInfo['DISO'] = AngleInfo['Missing']
	AngleInfo['ResidueNumber'] = np.array(IndexList).astype(np.int32)
	AngleInfo['SS'] = SS
	AngleInfo['CLE'] = CLE
	AngleInfo['Phi'] = np.clip( np.array(phiList).astype(np.float32), -pi, pi)
	AngleInfo['Psi'] = np.clip( np.array(psiList).astype(np.float32), -pi, pi)
	AngleInfo['Theta'] = np.clip(np.array(thetaList).astype(np.float32), -pi, pi)
	AngleInfo['Tau'] = np.clip(np.array(tauList).astype(np.float32), -pi, pi)
	AngleInfo['Omg'] = np.clip(np.array(omgList).astype(np.float32), -pi, pi)

	return AngleInfo
