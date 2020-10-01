import cv2
import numpy as np
import random
from flask import Flask, make_response, render_template, request
app = Flask(__name__)

def captcha():
	r1 = random.randint(4, 10)
	s = ""
	while r1>0:
		r2 = random.randint(1, 10)
		if r2<=5:
			r3 = str(random.randint(0, 9))
		else:
			r3 = random.randint(0, 25)
			r4 = random.randint(1, 100)
			if r4<=50:
				r3 = chr(65+r3)
			else:
				r3 = chr(97+r3)
		s+=r3
		r1-=1
	return s

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def genImage():
  i1 = 255 * np.ones(shape=[256, 256, 3], dtype=np.uint8)
  text = captcha()
  r = random.randint(100, 200)
  r2 = random.randint(0, 90)
  i1 = cv2.putText(i1, text, (20, r), cv2.FONT_HERSHEY_SIMPLEX,  
                    1, (10, 10, 10))
  i1 = rotate_image(i1, r2)
  for i in range(i1.shape[0]):
    for j in range(i1.shape[1]):
      if i1[i][j].any() == 0:
        i1[i][j] = np.array((255, 255, 255))
  i2 = 255 * np.ones(shape=[256, 256, 3], dtype=np.uint8)
  i2 = cv2.rectangle(i2, (0, 0), (40, 256), (128, 128, 128), -1)
  for i in range(i2.shape[0]):
    np.random.shuffle(i2[i])
  return i1+i2, text

text = None

@app.route('/')
def hello_world():
  return render_template('hello.html')

@app.route('/endpoint')
def endpoint():
  global text
  captcha_image, text = genImage()
  retval, buffer = cv2.imencode('.png', captcha_image)
  response = make_response(buffer.tobytes())
  response.headers['Content-Type'] = 'image/png'
  return response

@app.route('/check', methods=["GET", "POST"])
def check():
  print(text)
  if request.json.get("value") == text:
    return "Thats right"
  else:
    return "There's some problem"