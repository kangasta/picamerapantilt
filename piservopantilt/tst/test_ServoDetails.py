from unittest import TestCase

try:
	from unittest.mock import Mock, patch
except ImportError:
	from mock import Mock, patch

from piservopantilt import ServoDetails

class ServoDetailsTest(TestCase):
	def test_cannot_create_with_invalid_pw(self):
		with self.assertRaises(ValueError):
			ServoDetails(12,100,2500)
		with self.assertRaises(ValueError):
			ServoDetails(12,500,2600)
		ServoDetails(12,500,2500)

	def test_provides_servo_details(self):
		sd = ServoDetails(12,1000,2000)
		self.assertEqual(sd.pin, 12)
		self.assertEqual(sd.min, 1000)
		self.assertEqual(sd.max, 2000)

	def test_cannot_set_invalid_pos(self):
		sd = ServoDetails(12,1000,2000)
		with self.assertRaises(ValueError):
			sd.pos = 181
		with self.assertRaises(ValueError):
			sd.pos = -1

	def test_pos_setter_affects_pos_and_pw_output(self):
		sd = ServoDetails(12,1000,2000)
		sd.pos = 90
		self.assertEqual(sd.pos, 90)
		self.assertEqual(sd.pulsewidth, 1500)

