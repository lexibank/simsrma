from lingpy import *
from collections import defaultdict
from clldutils.text import strip_chars

data = csv2list('data.tsv', strip_lines=False)

header = data[0]
concepts = defaultdict(list)
for line in data[1:]:
    for i, entry in enumerate(line):
        if header[i].endswith('_gloss'):
            gloss = strip_chars(
                    '⁰¹²³⁴⁵⁶⁷⁸⁹ᴴᴿ', entry)
            if gloss.strip() not in ['', 'NA']:
                concepts[gloss] += [(header[i][:-6], entry)]
with open('../etc/concepts.tsv', 'w') as f:
    f.write('NUMBER\tENGLISH\tVARIANTS\tLANGUAGES\n')

    for i, (k, v) in enumerate(
            sorted(concepts.items(), key=lambda x: x[0])):
        f.write(
            '\t'.join([
                str(i+1),
                k,
                '//'.join(list(set([line[1] for line in v]))),
                ';'.join([line[0] for line in v])])+'\n')
