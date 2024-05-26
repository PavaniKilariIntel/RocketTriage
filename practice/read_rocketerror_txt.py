f = open("rocketerror.txt", "r")
result ={}
for line in f:
    line = line.strip()
    key = line.split(':')[0]
    # print(line)
    if key not in result:
        result[key]=line.split(':')[-1]

print(result, sep="\n")
print(str(result))

