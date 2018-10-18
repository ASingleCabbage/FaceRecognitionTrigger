from imutils import paths, resize
import face_recognition
import pickle
import cv2
import os, argparse

# data_path is a folder containing folders, with each folder containing faces
# of a person to recognize. The subfolder name should be the name of the person
# the folder is for.
#
#   data_path ---> person1_name ---> images of person1
#                > person2_name ---> images of person2
#                  ...

parser = argparse.ArgumentParser(description='Encode faces.')
parser.add_argument("-i", "--dataset", required=True,
                    help="path to input directory of faces + images")
parser.add_argument("-e", "--encodings", required=True,
	                help="path to serialized db of facial encodings")
args = vars(parser.parse_args())


data_path = args["dataset"]
encoding_output = args["encodings"]

# "cnn" for more accurate but less speed, "hog" for the opposite
detect_method = "cnn"

imagePaths = list(paths.list_images(data_path))

print("Loaded {} images from path {}:".format(len(imagePaths), data_path))
for path in imagePaths:
    print(path)

knownEncodings = []
knownNames = []

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    return  cv2.resize(image, dim, interpolation = inter)

counttracker = {}
for (i, path) in enumerate(imagePaths):
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    name = path.split(os.path.sep)[-2]

    # resize neccessary or else we run out of GPU memory
    image = image_resize(cv2.imread(path), width=800)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print("encoding faces")
    boxes = face_recognition.face_locations(rgb, model=detect_method)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)
        count = counttracker.get(name, 0) + 1
        counttracker[name] = count


data = (knownEncodings, knownNames, counttracker)
with open(encoding_output, "wb") as f:
    f.write(pickle.dumps(data))
