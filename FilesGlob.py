import os

# basic filter function use prefix, surfix, and contains
def prefix_filter(strs):
    if strs == '':
        return trueFunc

    def isprefix(x):
        if x[:len(strs)] == strs:
            return True
        else:
            return False
    return isprefix


def surfix_filter(strs):
    if strs == '':
        return trueFunc

    def issurfix(x):
        if x[-len(strs):] == strs:
            return True
        else:
            return False
    return issurfix


def contain_filter(strs):
    if strs == '':
        return trueFunc

    def iscontain(x):
        return strs in x
    return iscontain


def trueFunc(x):
    return True


# read the list of files
def globFiles(rfolder, prefix='', surfix='', contained='', fullPath=True):
    pfunc = prefix_filter(prefix)
    cfunc = contain_filter(contained)
    sfunc = surfix_filter(surfix)
    
    def filter_func(x):
        return pfunc(x) and cfunc(x) and sfunc(x)

    files = os.listdir(rfolder)
    if fullPath:
        fs = [rfolder+f for f in files if filter_func(f)]
    else:
        fs = [f for f in files if filter_func(f)]
    return fs



