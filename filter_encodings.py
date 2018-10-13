import pickle
import copy

file1 = "encoding"
file2 = "encoding_nate"

output = "encoding_asian"

data = pickle.loads(open(file1, "rb").read())

nameMatches = ["Daniel", "jared", "thomas"]

newEncodingList = []
newNameList = []
newMatchCount = {}

filterName = "asian"

for (i, name) in enumerate(data[1]):
    if name in nameMatches:
        newEncodingList.append(data[0][i])
        newNameList.append(filterName)
        newMatchCount[filterName] = newMatchCount.get(filterName, 0) + 1

filtered = (newEncodingList, newNameList, newMatchCount)

with open(output, "wb") as f:
    f.write(pickle.dumps(filtered))
