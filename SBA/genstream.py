chart="kronos"
f=open(chart+".txt", "w")
l=1500
r=1575
for i in range (0,101):
    l=1500+150*i
    r=1575+150*i    
    f.write(str(l)+",0\n")
    f.write(str(r)+",1\n")
f.close()