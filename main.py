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
from api import latexSolver
import subprocess
import time
from bbox import create_bboxes

img_path = "/Users/stevengong/Projects/HackMIT/image.jpg"

ans = "2+2=4" # To do: Store this in LaTeX
class DummyTask:
	def __init__(self, data):
		self.data = data
	def ready(self):
		return True
	def get(self):
		return self.data

def save_frame(frame):
	# some intensive computation...
	cv.imwrite(img_path, frame)
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
	fontScale = 1
	color = (255, 0, 0)
	thickness = 2

	while True:
		while len(pending) > 0 and pending[0].ready():
			res = pending.popleft().get()
			res = cv.putText(res, ans, org, font, 
                   fontScale, color, thickness, cv.LINE_AA)
			cv.imshow('threaded video', res)
		if len(pending) < threadn:
			_ret, frame = cap.read()
			if threaded_mode:
				count += 1
				count %= 2
				if (count == 0): 
					task = pool.apply_async(save_frame, (frame.copy(),))
				else: # In case you want to alternate between tasks
					task = pool.apply_async(create_bboxes, (frame.copy(),))
			else:
				task = DummyTask(save_frame(frame))
			pending.append(task)

		ch = cv.waitKey(1)
		if ch == ord(' '):
			threaded_mode = not threaded_mode # Switch between single threaded and multi-threaded
		if ch == 27:
			break

def getLatex():
	while True:
		# result = os.system("pix2tex /Users/stevengong/Projects/HackMIT/junk/test.png")
		# latex_output = os.system("pix2tex " + img_path)
		# print("output", latex_output)
		result = subprocess.run(['pix2tex', '/Users/stevengong/Projects/HackMIT/samples/test3.png'], stdout=subprocess.PIPE)
		try:
			ans = result.stdout.decode('utf-8').split(' ', 1)[1]
			print(ans)
			if (len(ans) > 3):
				# ans = latexSolver(ans)
				print(ans)
				time.sleep(100)
		except:
			print("No LaTeX detected")
	
	return frame


if __name__ == '__main__':
	thread2 = threading.Thread(target=getLatex)
	thread2.start()
	main()
	cv.destroyAllWindows()