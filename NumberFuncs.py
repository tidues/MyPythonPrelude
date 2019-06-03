
# modular a range of numbers into list
def numberMod(rng, modulus):
    res = {}
    fst = None
    tmpLst = []
    for i in rng:
        val = i % modulus
        if val == 0:
            if fst is not None:
                # add the previous list
                res[(fst,i-1)] = tmpLst.copy()

            # initialize new list
            fst = i
            tmpLst = []

        if fst is None:
            fst = i

        tmpLst.append(i)

    if len(tmpLst) > 0:
        res[(fst, i)] = tmpLst.copy()

    return res

        


