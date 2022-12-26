"""
Parallel processing in OpenCV:https://stackoverflow.com/questions/50910945/python3-parallel-process-opencv-video-frames

Concurrency: 
https://stackoverflow.com/questions/36847817/can-two-infinite-loops-be-ran-at-once
https://stackoverflow.com/questions/3474382/how-do-i-run-two-python-loops-concurrently
"""
import numpy as np
import os
import cv2 as cv
import sys
from multiprocessing.pool import ThreadPool
import threading
from collections import deque
# from api import latexSolver
import subprocess
from helper import *
import time

start = time.process_time()


img_path = "/Users/stevengong/Projects/HackMIT/image.jpg"

finished_loading = True

ans = ""
final_ans = ""

x, y, w, h = 460, 440, 1000, 200 # bounding box

class DummyTask:
	def __init__(self, data):
		self.data = data
	def ready(self):
		return True
	def get(self):
		return self.data

def save_frame(frame):
	# some intensive computation...
	median_grayscale = np.median(frame)
	gray = get_grayscale(frame)
	ret, img_thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
	# if (time.process_time() - start > 2):
	cv.imwrite(img_path, frame[y:y+h, x:x+w])
	# 	start = time.process_time()
	return frame

def main():
	try:
		fn = sys.argv[1]
	except:
		fn = 0
	cap = cv.VideoCapture(fn)


	threadn = cv.getNumberOfCPUs()
	pool = ThreadPool(processes = threadn)
	pending = deque()

	threaded_mode = True

	count = 0 
	
	# font
	font = cv.FONT_HERSHEY_SIMPLEX
	org = (50, 50)
	org2 = (50, 50)
	fontScale = 1
	color = (0, 0, 0)
	thickness = 2

	while True:
		while len(pending) > 0 and pending[0].ready():
			res = pending.popleft().get()
			res = cv.putText(res, ans, (x, y-50), font, 
                   fontScale, color, thickness, cv.LINE_AA)
			res = cv.putText(res, final_ans, (x - (len(final_ans) * 4), y + h + 50), font, 
                   1, color, thickness, cv.LINE_AA)
			
			res = cv.rectangle(res, (x, y), (x + w, y + h), color, 2)
			cv.imshow('Camera', res)
		if len(pending) < threadn:
			_ret, frame = cap.read()
			if threaded_mode:
				count += 1
				count %= 2
				task = pool.apply_async(save_frame, (frame.copy(),))
			else:
				task = DummyTask(save_frame(frame))
			pending.append(task)

		ch = cv.waitKey(1)
		if ch == ord(' '):
			threaded_mode = not threaded_mode # Switch between single threaded and multi-threaded
		if ch == 27:
			break

def getLatex():
	global finished_loading, ans, final_ans
	finished_loading = False
	result = subprocess.run(['pix2tex', img_path], stdout=subprocess.PIPE)
	try:
		ans = result.stdout.decode('utf-8').split(' ', 1)[1]
		if (len(ans) > 3):
			print("fetching answer for ", ans)
			# final_ans = latexSolver(ans)
	except:
		print("No LaTeX detected")
	
	finished_loading = True

def getLatexInfinite():
	while True:
		# try:
		num = int(input())
		global ans, final_ans
		if num == 0:
			for i in range(10):
				getLatex()
		elif num == 1: 
			ans = r"\int\frac{1 + \cos x}{x + \sin x}dx"
			# final_ans = latexSolver(ans)
			
		# except:
		# 	print("it's fine")

if __name__ == '__main__':
	thread2 = threading.Thread(target=getLatexInfinite)
	thread2.start()
	main()
	cv.destroyAllWindows()