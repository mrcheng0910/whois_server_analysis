

fp_total = open('dist_of_domain.txt','r')

srv_total = []

for i in fp_total:
    srv_total.append(i.split('\t')[0].lower())


srv_total = set(srv_total)

print len(srv_total)

fp_d = open('detected_srv.txt','r')

srv_d = []
for i in fp_d:
    srv_d.append(i.strip().lower())

srv_d = set(srv_d)
print len(srv_d)


cha = srv_total-srv_d

print len(cha)

for i in cha:
    print i
