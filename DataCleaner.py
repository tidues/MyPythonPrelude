from . import StringTools as st
from . import FPToolBox as fp
import os

### this data cleaner is mainly for data cleaning before reading the raw dataset, so do not use it for other data manipulations, which should be excuted in the latter phase of the project

### speed bottle (guess): __readLine and __rowVerify

# all row and column indexes start with 0
class Cleaner:
    # header: the index of the header row, -1 if no header
    # newCols: a list of column labels or indexes that keeps in the cleaned data, None if keep all columns. Will not affect the order of the cleaned data.
    # startRow: the first row to start verifying, None if it is header+1
    # checkRow: a function that reads a row index, and output if verify this row or not. This will not reduce the number of rows in the cleaned data.
    # log: the place to log all the unpassed data
    # seps: the separators for columns, can put multiple separators in a string
    # osep: the output file separator
    # strip: if strip each cell, will be slower if True
    def __init__(self, header=0, newCols=None, startRow=None, checkRow=None, log='./logs/dcleaner.log', seps='\t', osep='\t', strip=False):
        self.header = header
        self.newCols = newCols
        if startRow is None:
            self.startRow += header
        else:
            self.startRow = startRow
        if checkRow is None:
            self.checkRow = lambda x: True
        else:
            self.checkRow = checkRow
        self.log = log
        self.colRules = {}
        self.extRules = []
        self.seps = seps
        self.label2idx = {}
        self.idx2label = {}
        self.osep = osep
        self.strip=strip


    # add verification rule for a column (by label or index)
    def setColRule(self, column, f):
        self.colRules[column] = f


    # set a dict of column rules
    def setColRules(self, colRules):
        for key in colRules:
            self.colRules[key] = colRules[key]


    # add extra rule
    def setExtRules(self, fs):
        self.extRules += fs


    # clean the given file
    # fpath: file for cleanning; cleanfpath: the cleaned file fullname
    def clean(self, fpath, cleanfpath, log=None, encoding='utf-8', newline=None, errors='replace'):
        # set log address
        if log is None:
            log = self.log

        # create paths if doesn't exit
        self.__makepath(cleanfpath)
        self.__makepath(log)

        # clean data
        with open(fpath, 'r', encoding=encoding, newline=newline, errors=errors) as rf, open(cleanfpath, 'w+') as wf, open(log, 'a+') as lf:
            lines = rf.readlines()
            for idx, line in enumerate(lines):
                if idx == self.header:
                    # initialize headers
                    wf.write(self.__readHeaders(line))
                elif idx < self.startRow:
                    # if before start row, just copy
                    wf.write(line)
                elif not self.checkRow(idx):
                    # if check row is false
                    wf.write(self.__readLine(line))
                else:
                    # if not header, not before start row, and checkrow is true
                    res = self.__rowVerify(line)
                    if res[0]:
                        wf.write(self.__readLine(line))
                    else:
                        errStr = fpath + '\t' + str(idx + 1) + '\t' + res[2] + '\t' + res[1] + '\n'
                        lf.write(errStr)


    # create path
    def __makepath(self, path):
        # create folder if not exist
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise


    # read headers
    def __readHeaders(self, headers):
        headerLst = st.splitOneOf(headers, self.seps, delEmpty=True)
        headerLst = fp.lmap(lambda x: x.strip(), headerLst)
        for idx, header in enumerate(headerLst):
            self.idx2label[idx] = header
            self.label2idx[header] = idx

        return self.__cleanCols(headerLst)


    # check if column index is in the newCols list
    def __keepIdx(self, idx):
        if idx in self.newCols:
            return True
        
        if idx not in self.idx2label:
            return False
        elif self.idx2label[idx] in self.newCols:
            return True

        return False


    # clean line
    def __readLine(self, line):
        valLst = st.splitOneOf(line, self.seps, delEmpty=False)
        if self.strip:
            valLst = fp.lmap(lambda x: x.strip(), valLst)
        return self.__cleanCols(valLst)


    # keep only cols that are needed
    def __cleanCols(self, valLst):
        resLst = []
        for idx, val in enumerate(valLst):
            if self.__keepIdx(idx):
                resLst.append(val)

        res = fp.foldr(fp.concat(self.osep), resLst, '')

        return res[:-1] + '\n'


    # verify a single row:
    def __rowVerify(self, row):
        rules = self.colRules
        erules = self.extRules

        # split into columns
        valLst = st.splitOneOf(row, self.seps, delEmpty=False)

        # strip whitespaces
        if self.strip:
            valLst = fp.lmap(lambda x: x.strip(), valLst)

        # verify column rules
        if len(rules) > 0:
            for key in rules:
                if not isinstance(key, int):
                    # if is not an index
                    if key not in self.label2idx:
                        print('Warning: column lable ', key, ' is not in the headers')
                        continue
                    else:
                        idx = self.label2idx[key]
                else:
                    idx = key

                if not rules[key](valLst[idx]):
                    if idx in self.label2idx:
                        col = self.label2idx[idx]
                    else:
                        col = str(idx)
                    return (False, rules[key].__name__, col)

        # verify extra rules
        if len(erules) > 0:
            for rule in erules:
                if len(self.idx2label) > 0:
                    # set input as a dict
                    vals = {}
                    for idx in self.idx2label:
                        vals[self.idx2label[idx]] = valLst[idx]
                else:
                    # set input as a valList
                    vals = valLst

                if not rule(vals):
                    return (False, rule.__name__, 'extra')

        # passed all verifiers
        return (True, '', '')










