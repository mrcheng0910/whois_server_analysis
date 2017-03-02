import tldextract

from collections import Counter


no_fetch_extract = tldextract.TLDExtract(suffix_list_urls=None)

fp = open('test.txt','r')
domains = []

for i in fp:
    domain = no_fetch_extract(i).domain
    domains.append(domain)

domains = list(set(domains))
c = Counter()
domain_struct = {}

for dm in domains:
    length = len(dm)
    for d in dm[:length-1]:
        domain_struct['length'] = length



