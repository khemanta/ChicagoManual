import re
from pybtex.database.input import bibtex
from mytools.tools import drop_to_ipython as dti
import pprint

bib_file = 'zotero-iocbio.bib'
out_file = 'converted_bibliography.bib'

f = open(bib_file, 'r')
fs = f.read()
f.close()

oxygen = re.compile('18O')
smallP = re.compile('31P')
largeP = re.compile('32P')
rcarbon = re.compile('13C')
uhydrogen = re.compile(' 1H ')
ucotwo = re.compile(' CO2')
desros = re.compile('Des{Rosiers}')

fs = oxygen.sub('$^{18}\hspace{-0.04cm}${O}', fs)
fs = smallP.sub('$^{31}\hspace{-0.04cm}${P}', fs)
fs = largeP.sub('$^{32}\hspace{-0.04cm}${P}', fs)
fs = rcarbon.sub('$^{13}\hspace{-0.04cm}${C}', fs)
fs = uhydrogen.sub(' $^{1}\hspace{-0.04cm}${H} ', fs)
fs = ucotwo.sub(' {CO}$_2$', fs)
fs = desros.sub('DesRosiers', fs)

f = open(bib_file, 'w')
f.write(fs)
f.close()

parser = bibtex.Parser()
data = parser.parse_file(bib_file)

all_keys = set()
output_keys = []
for bibkey in data.entries:
    entry = data.entries[bibkey]

    try:
        authors = entry.persons[u'author']
    except Exception:
        print '  Ignoring :', bibkey
        continue

    if authors[0].prelast():
        A = authors[0].prelast()[0]
        B = authors[0].last()[0]
        A = A.lower().replace(r'{\"u}', 'u').replace(r'{\"o}', 'o')
        B = B.lower().replace(r'{\"u}', 'u').replace(r'{\"o}', 'o')
        first_author = ''.join((A, B))[:5]
    else:
        fa = authors[0].last()[0]
        fa = fa.lower().replace(r'{\"u}', 'u').replace(r'{\"o}', 'o').replace(r'des{ rosiers}', 'desrossiers')
        if fa.startswith('{'):
            first_author = fa[1:6]
        else:
            first_author = fa[:5]        
        
    mid_key = u''
    for index, person in enumerate(authors[1:]):
        last_name = person.last()[0].lower()
        if last_name.startswith('{'):
            first_letter = last_name[1]
        else:
            first_letter = last_name[0]
        mid_key += first_letter
        if index == 3:
            break

    year = entry.fields[u'year'][-2:]

    if mid_key.strip() == str():
        key = '_'.join([first_author, year])
    else:
        key = '_'.join([first_author, mid_key, year])

    new_key = key
    if key in all_keys:
        new_key = key + '_A'
        if new_key in all_keys:
            new_key = key + '_B'
            if new_key in all_keys:
                new_key = key + '_C'
                if new_key in all_keys:
                    msg = "Too many keys are the same."
                    raise UserWarning(msg, (new_key, all_keys))


    if new_key == 'des_c_05':
        print entry

    
    all_keys.add(new_key)

    output_keys.append((new_key, entry.fields[u'title'][:80]))
    insensitive_key = re.compile(bibkey, re.IGNORECASE)
    fs = insensitive_key.sub(new_key, fs)


for nk, tit in sorted(output_keys):
    print "{0:<20} {1}".format(nk, tit)

f = open(out_file, 'w')
f.write(fs)
f.close()


