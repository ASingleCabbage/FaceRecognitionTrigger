from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import cv2
import math, json
import simpleaudio as sa

encodings_path = "encoding_asian"
# had to use the faster yet less accurate "hog" instead of "cnn"
detect_method = "hog"

data = pickle.loads(open(encodings_path, "rb").read())

knownEncodings = data[0]
knownNames = data[1]
encodingCounts = data[2]

print("loaded encoding lists with {} entries".format(len(knownEncodings)))

vs = VideoStream(src=0).start()
writer = None

print("starting webcam...")
time.sleep(2.0)

while True:
	frame = vs.read()
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(frame, width=750)
	r = frame.shape[1] / float(rgb.shape[1])

	boxes = face_recognition.face_locations(rgb, model=detect_method)
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	for encoding in encodings:
		matches = face_recognition.compare_faces(knownEncodings, encoding)
		name = "asian"

		nameMatchProp = 0.0

		if True in matches:
			matchedIdxs = [ i for (i, b) in enumerate(matches) if b ]
			counts = {}

			for i in matchedIdxs:
					name = knownNames[i]
					counts[name] = counts.get(name, 0) + 1

			name = max(counts, key=lambda n: counts.get(n) / encodingCounts[n])
			nameMatchProp = counts.pop(name) / encodingCounts[name]

		names.append("{}% ".format(int(nameMatchProp * 100)) + name)
	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# rescale the face coordinates
		top = int(top * r)
		right = int(right * r)
		bottom = int(bottom * r)
		left = int(left * r)

		# draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		   break

cv2.destroyAllWindows()
vs.stop()
