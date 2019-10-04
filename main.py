from CuckooSearchRunner import CSRunner
from CuckooSearchCVRP import LevyCombinationTypes
from CuckooSearchCVRP import Neighborhoods as n

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.TWOOPT, n.EXCHANGE]
fileName = 'twoOpt_exchange_5050_levy6test'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.TWOOPT, n.SHIFT1, n.SWAP22]
fileName = 'twoOpt_shift1_swap22_5050_levy4_levy5_test'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1_LARGE_1
listNeighbor = [n.TWOOPT, n.SWAP22]
fileName = 'twoOpt_swap22_levy4_levy5_test'
CSRunner(combiType, listNeighbor, fileName)