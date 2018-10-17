from unittest import TestCase

try:
	from unittest.mock import MagicMock, patch, call
except ImportError:
	from mock import MagicMock, patch, call

import pigpio
import resettabletimer

from piservopantilt import ServoControl

class ServoControlTest(TestCase):
	#def __get_mock_pi(self):
	#	mock = MagicMock()
	@patch.object(pigpio, 'pi')
	def test_constructor_moves_servo_to_initial_position(self, mock):
		mock.return_value = MagicMock()

		for pos in [(0,0), (180,180)]:
			s = ServoControl(initial_position=pos, auto_off=False)
			self.assertEqual(s.position["pan"], pos[0])
			self.assertEqual(s.position["tilt"], pos[1])

	@patch.object(pigpio, 'pi')
	def test_can_turn_off_the_servos(self, mock):
		pi_mock = MagicMock()

		mock.return_value = pi_mock
		s = ServoControl(pan_pin=12, tilt_pin=18, pan_limits=(500,2500),tilt_limits=(500,2500), initial_position=(90,90), auto_off=False)
		pi_mock.set_servo_pulsewidth.assert_has_calls([
			call(12,1500),
			call(18,1500)
		])
		s.off()
		pi_mock.set_servo_pulsewidth.assert_has_calls([
			call(12,0),
			call(18,0)
		])

	@patch.object(pigpio, 'pi')
	def test_has_methods_to_move_tom_min_and_max_positions(self, mock):
		mock.return_value = MagicMock()

		s = ServoControl(auto_off=False)

		s.min()
		self.assertEqual(s.position["pan"], 0)
		self.assertEqual(s.position["tilt"], 0)

		s.max()
		self.assertEqual(s.position["pan"], 180)
		self.assertEqual(s.position["tilt"], 180)

	@patch('piservopantilt.servo_control.ResettableTimer')
	@patch.object(pigpio, 'pi')
	def test_has_auto_off_timer(self, pi_mock, timer_mock):
		timer = MagicMock()
		pi_mock.return_value = MagicMock()
		timer_mock.return_value = timer

		s = ServoControl()

		timer.start.assert_called_with()
		timer.reset.assert_called_with()
