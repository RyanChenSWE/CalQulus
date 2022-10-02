"""
Tesseract is an OCR, but it doesn't work on LaTeX.
"""
import cv2
from latexConverter import LatexConverter
import pytesseract
from pytesseract import Output

video_capture = cv2.VideoCapture(0)

# get grayscale image
def get_grayscale(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

solver = LatexConverter()
while True:
	ret, img = video_capture.read()
	custom_config = '--oem 3 --psm 7' # https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
	d = pytesseract.image_to_data(img, config=custom_config, output_type=Output.DICT)
	# img = get_grayscale(img)
	print(d)
	n_boxes = len(d['level'])
	for i in range(n_boxes):
		# if (d['conf'][i] < 90): continue
		(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imshow('img', img)

	if cv2.waitKey(10) == 27: #Press the "Escape key" to terminate the program
		video_capture.release()
		cv2.destroyAllWindows()
		print("Program terminated, I hope you found your match :)")
		break
	