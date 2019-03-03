'''
Original Author: Shengyao Lu
Creation date: Mar 2, 2019
Contents of file: 
	Unit testing of FaceRecognition
'''

import unittest,requests
import face_recognition
import website
class BasicTests(unittest.TestCase): 
###############
#### tests ####
###############
    def test_face_recog(self):
        image_true = face_recognition.load_image_file('tests/obama.jpg')
        image_false = face_recognition.load_image_file('tests/back.jpg')
        self.assertEqual(website.FaceDetection(image_true), 'True')
        self.assertEqual(website.FaceDetection(image_false), 'False')

if __name__ == "__main__":
	unittest.main()

		