from CuckooSearchRunner import CSRunner
from CuckooSearchCVRP import LevyCombinationTypes
from CuckooSearchCVRP import Neighborhoods as n

#region running on main pc
combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.TWOOPT, n.EXCHANGE]
fileName = 'crossTwoOpt_exchange_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.TWOOPT, n.SHIFT1, n.SWAP22]
fileName = 'crossTwoOpt_shift1_swap22_5050_levy4_levy5_500iter'

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP21, n.SHIFT1, n.SWAP22]
fileName = 'swap21_shift1_swap22_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP21, n.REINSERTION, n.SWAP22]
fileName = 'swap21_reinsertion_swap22_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP21, n.SHIFT1]
fileName = 'swap21_shift1_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP11, n.SHIFT1, n.SWAP22]
fileName = 'twoOpt_shift1_swap22_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP11, n.REINSERTION, n.SWAP22]
fileName = 'twoOpt_reinsertion_swap22_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP21, n.SHIFT1, n.DOUBLE_BRIDGE]
fileName = 'swap21_shift1_doubleBridge_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP21, n.REINSERTION]
fileName = 'swap21_reinsertion_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP11, n.SHIFT1, n.DOUBLE_BRIDGE]
fileName = 'twoOpt_shift1_doubleBridge_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP21, n.REINSERTION, n.DOUBLE_BRIDGE]
fileName = 'swap21_reinsertion_doubleBridge_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP21, n.EXCHANGE]
fileName = 'swap21_exchange_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP11, n.SHIFT1]
fileName = 'twoOpt_shift1_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1_LARGE_1
listNeighbor = [n.SWAP21, n.DOUBLE_BRIDGE]
fileName = 'swap21_doubleBridge_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)
#endregion

#region running on 2nd pc
combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP11, n.OR_OPT2]
fileName = 'twoOpt_orOpt2_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP21, n.OR_OPT2]
fileName = 'swap21_orOpt2_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP11, n.SHIFT2]
fileName = 'twoOpt_shift2_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP11, n.SWAP21]
fileName = 'twoOpt_swap21_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP11, n.SWAP21, n.DOUBLE_BRIDGE]
fileName = 'twoOpt_swap21_doubleBridge_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.TWOOPT, n.SWAP21, n.SWAP22]
fileName = 'crossTwoOpt_swap21_swap22_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.TWOOPT, n.OR_OPT3]
fileName = 'crossTwoOpt_orOpt3_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.TWOOPT, n.SWAP21]
fileName = 'crossTwoOpt_swap21_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP21, n.SHIFT2]
fileName = 'swap21_shift2_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.TWOOPT, n.SWAP21, n.DOUBLE_BRIDGE]
fileName = 'crossTwoOpt_swap21_doubleBridge_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1_LARGE_1
listNeighbor = [n.SWAP21, n.SWAP22]
fileName = 'swap21_swap22_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)
#endregion

#region run on camille pc
combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP21, n.OR_OPT3]
fileName = 'swap21_orOpt3_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.TWOOPT, n.SHIFT2]
fileName = 'crossTwoOpt_shift2_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1_LARGE_1
listNeighbor = [n.SWAP11, n.SWAP22]
fileName = 'twoOpt_swap22_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1_LARGE_1
listNeighbor = [n.TWOOPT, n.SWAP22]
fileName = 'crossTwoOpt_swap22_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1
listNeighbor = [n.SHIFT1]
fileName = 'shift1_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP11, n.REINSERTION]
fileName = 'twoOpt_reinsertion_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1
listNeighbor = [n.SWAP21]
fileName = 'swap21_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2_LARGE_1
listNeighbor = [n.SWAP11, n.REINSERTION, n.DOUBLE_BRIDGE]
fileName = 'twoOpt_reinsertion_doubleBridge_5050_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP11, n.EXCHANGE]
fileName = 'twoOpt_exchange_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.SWAP11, n.OR_OPT3]
fileName = 'twoOpt_orOpt3_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.TWOOPT, n.SHIFT1]
fileName = 'crossTwoOpt_shift1_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_2
listNeighbor = [n.TWOOPT, n.REINSERTION]
fileName = 'crossTwoOpt_reinsertion_5050_levy6_500iter'
CSRunner(combiType, listNeighbor, fileName)

combiType = LevyCombinationTypes.SMALL_1_LARGE_1
listNeighbor = [n.SWAP11, n.DOUBLE_BRIDGE]
fileName = 'twoOpt_doubleBridge_levy4_levy5_500iter'
CSRunner(combiType, listNeighbor, fileName)

#endregion