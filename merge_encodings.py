import pickle, argparse


parser = argparse.ArgumentParser(description='Merge two existing encoding files.')
parser.add_argument("file1", help="1st encoding")
parser.add_argument("file2", help="2nd encoding")
parser.add_argument("output", help="name of output file")
args = vars(parser.parse_args())

file1 = args["file1"]
file2 = args["file2"]
output = args["output"]

print("Merging {} and {} to {}".format(file1, file2, output))

data1 = pickle.loads(open(file1, "rb").read())
data2 = pickle.loads(open(file2, "rb").read())

def merge(d1, d2):
    result = {}
    for name in d1:
        print(len(result))
        count2 = d2.get(name, None)
        result[name] = d1[name]
        if count2 != None:
            result[name] += count2
            d2.pop(name)
    return result.update(d2)

combined = (data1[0] + data2[0], data1[1] + data2[1], {**data1[2], **data2[2]})

print(len(combined[0]))
print(combined[2])

with open(output, "wb") as f:
    f.write(pickle.dumps(combined))
