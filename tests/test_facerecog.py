import unittest,requests
import face_recognition
<<<<<<< HEAD
import website
=======
from ..website import *

>>>>>>> 9b27781a3b34e542e18411b71c3fa97b5e230553
class BasicTests(unittest.TestCase): 
###############
#### tests ####
###############
    def test_face_recog(self):
<<<<<<< HEAD
        image_true = face_recognition.load_image_file('tests/obama.jpg')
        image_false = face_recognition.load_image_file('tests/back.jpg')
        self.assertEqual(website.FaceDetection(image_true), 'True')
        self.assertEqual(website.FaceDetection(image_false), 'False')
=======
        image_true = face_recognition.load_image_file("/tests/obama.jpg")
        image_false = face_recognition.load_image_file("/tests/back.jpg")
        self.assertEqual(FaceDetection(image_true), 'True')
        self.assertEqual(FaceDetection(image_false), 'False')
>>>>>>> 9b27781a3b34e542e18411b71c3fa97b5e230553

if __name__ == "__main__":
	unittest.main()

		