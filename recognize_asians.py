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

# targets = {}
# with open("targets.json", "r") as f:
# 	targets = json.load(f)

# time until audio files can be played again in seconds
# audioDelay = 5

data = pickle.loads(open(encodings_path, "rb").read())

knownEncodings = data[0]
knownNames = data[1]
encodingCounts = data[2]

print("loaded encoding lists with {} entries".format(len(knownEncodings)))

# porportion of matches needed to recognize face
# matchThreshold = 0.0
# minimum difference between best and second best matches needed to establish certainty
# minDifference = 0.2

vs = VideoStream(src=0).start()
writer = None

print("starting webcam...")
# waits for the webcam to warm up
time.sleep(2.0)

# timeSinceAudioExec = 0
# lastAudioTime = time.time()
while True:
	frame = vs.read()
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(frame, width=750)
	r = frame.shape[1] / float(rgb.shape[1])

	boxes = face_recognition.face_locations(rgb, model=detect_method)
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# if len(encodings) == 0:
	# 	print("[INFO] No faces in frame")

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
			# competitor = max(counts, key=lambda n: counts.get(n) / encodingCounts[n], default=None)
			# compMatchProp = 0.0
			# if competitor != None:
			# 	compMatchProp = counts[competitor] / encodingCounts[competitor]

			# print("[INFO] {}% match. Threshold is {}. {} reference encodings.".format(nameMatchProp * 100, matchThreshold, encodingCounts[name]))

			# #setting unknown threshold here
			# if nameMatchProp < matchThreshold :
			# 	name = "unknown"
			# elif competitor != None and (nameMatchProp - minDifference) < compMatchProp :
			# 	print("------ too close with closest competing match {} at {}%. Reverting to unknown".format(competitor, compMatchProp * 100))
			# 	name = "unknown"
			# else:
			# 	target = next((item for item in targets if item["name"] == name), None)
			# 	if target != None and (time.time() - timeSinceAudioExec) > audioDelay :
			# 		timeSinceAudioExec = time.time()
			# 		wave_obj = sa.WaveObject.from_wave_file(target["file"])
			# 		play_obj = wave_obj.play()
		# else:
		# 	print("[INFO] Unrecognized face")

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
