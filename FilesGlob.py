import os
from natsort import natsorted, ns

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
# fullPath: 0: file names; 1: full paths; 2: both
def globFiles(rfolder, prefix='', surfix='', contained='', fullPath=2):
    pfunc = prefix_filter(prefix)
    cfunc = contain_filter(contained)
    sfunc = surfix_filter(surfix)
    
    def filter_func(x):
        return pfunc(x) and cfunc(x) and sfunc(x)

    # grab all file names
    files = [f for f in os.listdir(rfolder) if filter_func(f)]

    # natural sort all file names
    files = natsorted(files, alg=ns.IGNORECASE)

    # output accrodingly
    if fullPath == 0:
        fs = files
    elif fullPath == 1:
        fs = [rfolder+f for f in files]
    elif fullPath == 2:
        fs = ([rfolder+f for f in files], files)
    else:
        try:
            raise ValueError
        except ValueError:
            print('ValueError Exception: fullPath is ', fullPath)

    return fs



