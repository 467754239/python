
unit = {'t':2**40,'g':2**30,'m':2**20,'k':2**10,'b':1}

def convertUnit(s):
    s = s.lower()
    lastchar = s[-1]
    num = int(s[:-1])
    if lastchar in unit:
        return num*unit[lastchar]
    else:
        return int(s)

def scaleUnit(d):
    for k,v in unit.items():
        num = d / v
        if (0 < num < 2**10):
            return num,k

