import unittest,requests
import face_recognition
from ..website import *
import sys
print(sys.path)
class BasicTests(unittest.TestCase): 
###############
#### tests ####
###############
    def test_face_recog(self):
        image_true = face_recognition.load_image_file("tests/obama.jpg")
        image_false = face_recognition.load_image_file("tests/back.jpg")
        self.assertEqual(FaceDetection(image_true), 'True')
        self.assertEqual(FaceDetection(image_false), 'False')

if __name__ == "__main__":
	unittest.main()

		