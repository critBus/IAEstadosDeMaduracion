import re
def hayMaths(p,texto):
    return len(re.findall(p,texto))>0