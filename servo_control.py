import pigpio

from resettabletimer import ResettableTimer

class ServoDetails(object):
	def __init__(self, _pin, _min=500, _max=2500):
		self.__pin = _pin
		if not self.__check_pw(_min) or not self.__check_pw(_max):
			raise ValueError("Given min or max pulsewidth is invalid")
		self.__min = _min
		self.__max = _max
		self.__pos = None

	def __check_pw(self, pw):
		if pw >= 500 or pw <= 2500:
			return True
		return False

	@property
	def pin(self):
		return self.__pin

	@property
	def min(self):
		return self.__min

	@property
	def max(self):
		return self.__max

	@property
	def pos(self):
		return self.__pos

	@pos.setter
	def pos(self, pos):
		if pos > 180 or pos < 0:
			raise ValueError("Invalid servo position: " + str(pos))
		self.__pos = pos

	@property
	def pulsewidth(self):
		return int(self.__pos / 180 * (self.max - self.min) + self.min)

class ServoControl(object):
	def __init__(self, pan_pin=12, tilt_pin=18, pan_limits=(500,2500),tilt_limits=(500,2500), initial_position=(90,90), auto_off=1.5):
		self.__pi = pigpio.pi()
		self.__pan = ServoDetails(pan_pin, *pan_limits)
		self.__tilt = ServoDetails(tilt_pin, *tilt_limits)

		if auto_off:
			self.__auto_off_timer = ResettableTimer(auto_off, self.off)
			self.__auto_off_timer.start()
		else:
			self.__auto_off_timer = None

		# Move to initial position to have servos in known position
		self.move_to(*initial_position)

	def __set_pw(self, servo, pw=None):
		# TODO: check input pw validity
		if pw is None:
			pw = servo.pulsewidth
		return self.__pi.set_servo_pulsewidth(servo.pin, pw)

	def move_to(self, pan=None,tilt=None):
		if pan is not None:
			self.__pan.pos = pan
			self.__set_pw(self.__pan)
		if tilt is not None:
			self.__tilt.pos = tilt
			self.__set_pw(self.__tilt)
		if self.__auto_off_timer is not None:
			self.__auto_off_timer.reset()

	def off(self):
		for servo in [self.__pan, self.__tilt]:
			self.__set_pw(servo, 0)

	def min(self):
		self.move_to(0,0)

	def max(self):
		self.move_to(180,180)
