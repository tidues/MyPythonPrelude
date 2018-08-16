import lib.FPToolBox as fp

# function that read data into double list
def dataFormat(ffname, start_row=0, sep='\t'):
    rf = open(ffname, 'r')
    lst = []
    for line in rf:
        line = line.strip()
        lst.append(fp.lmap(strip, line.split(sep)))
    rf.close()
    return lst


# function for strip
def strip(strs):
    return strs.strip()
