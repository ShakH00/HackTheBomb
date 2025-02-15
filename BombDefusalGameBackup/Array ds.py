exp=[2200,2350,2600,2130,2190]
print("in feb company spend extra compare to janurary",exp[1]-exp[0])
print("first quater expense",exp[0]+exp[1]+exp[2])
print(' any expense is = 2000',2000 in exp)
exp.append(1980)
print("added june month",exp[5])
exp[3]=exp[3]-200
print("April month updated",exp[3])