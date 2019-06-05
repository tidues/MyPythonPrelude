
# test if this is a integer or float number
def isNumber(text):
    tLst = text.split('.')

    if len(tLst) > 2 or len(tLst) < 1:
        return False

    for t in tLst:
        if t.isnumeric() is False:
            return False

    return True

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

        


