'''
	Todo:
	 - Write more LED manipulation methods
	 - Document/annotate file
	 - Change 'delay' parameter to 'speed' and make conversions to a delay in ms as required  
	 - Figure out why uwsgi doesn't like updating the lights
	 - Add sigterm handler to allow systemd to quickly end the thread
'''

from rpi_ws281x import PixelStrip, Color
import time
import threading

args = None
methodName = None
alive = True
change = False

class LEDStrip:
	def __init__(self, LED_COUNT = 30, LED_PIN = 10, LED_FREQ_HZ = 800000, LED_DMA = 10, LED_BRIGHTNESS = 255, LED_INVERT = False, LED_CHANNEL = 0):
		self.LEDMethods = {
			"animated-rainbow" : self._solidRainbow,
			"rainbow-circle" : self._rainbowCircle,
			"pixel-pileup" : self._pixelPileup,
			"rainbow-pixel-pileup" : self._rainbowPixelPileup,
			"pixel-run" : self._pixelRun,
			"rainbow-pixel-run" : self._rainbowPixelRun,
			"solid-color" : self._solidColor,
		}

		self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
		self.strip.begin()

		self.thread = threading.Thread(target=self._LEDThread, args=())
		self.thread.start()

	def _LEDThread(self):
		global methodName, alive, args

		while methodName == None and alive == True:
			pass

		while alive == True:
			self.LEDMethods[methodName]()
			time.sleep(0.02)

		args['color'] = Color(0, 0, 0)
		self.LEDMethods['solidColor']()

	def update(self, method, arguments):
		global args, alive, change, methodName

		if method == 'exit':
			alive = False
			change = True
			self.thread.join()
			return
		elif method not in self.LEDMethods.keys():
			return

		args = arguments
		methodName = method
		change = True

		return

	def _pixelRun(self):
		global change, args

		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, args['color'])
			self.strip.show()

			self.strip.setPixelColor(i, Color(0, 0, 0))
			time.sleep(args['delay'] / 1000)

			if change == True:
				change = False
				return

	def _rainbowPixelRun(self):
		global change, args

		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, self._color_wheel(int(255 * i / self.strip.numPixels()), args['offset']))
			self.strip.show()

			self.strip.setPixelColor(i, Color(0, 0, 0))
			time.sleep(args['delay'] / 1000)

			if change == True:
				change = False
				return

	def _solidColor(self):
		global change, args

		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, args['color'])
		self.strip.show()

		if change == True:
			change = False
			return

	def _color_wheel(self, pos, offset = 0):
		if offset != 0:
			pos = (pos + offset) & 255

		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def _solidRainbow(self):
		global change, args

		for j in range(256):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self._color_wheel(j & 255, args['offset']))
			self.strip.show()
			time.sleep(args['delay'] / 1000.0)

			if change == True:
				change = False
				return

	def _pixelPileup(self):
		global change, args

		for i in range(self.strip.numPixels()):
			for j in range(self.strip.numPixels() - i):
				self.strip.setPixelColor(j, args['color'])
				self.strip.show()

				if j + 1 != self.strip.numPixels() - i:
					self.strip.setPixelColor(j, Color(0, 0, 0))
				time.sleep(args['delay'] / 1000)

				if change == True:
					change = False
					return

	def _rainbowPixelPileup(self):
		global change, args

		for i in range(self.strip.numPixels()):
			for j in range(self.strip.numPixels() - i):
				self.strip.setPixelColor(j, self._color_wheel(int(255 * j / self.strip.numPixels()), args['offset']))
				self.strip.show()

				if j + 1 != self.strip.numPixels() - i:
					self.strip.setPixelColor(j, Color(0, 0, 0))
				time.sleep(args['delay'] / 1000)

				if change == True:
					change = False
					return

	def _rainbowCircle(self):
		global change, args

		for i in range(self.strip.numPixels()):
			for j in range(self.strip.numPixels()):
				self.strip.setPixelColor((i + j) % self.strip.numPixels(), self._color_wheel(int(255 * j / self.strip.numPixels()), args['offset']))
				self.strip.show()

				time.sleep(args['delay'] / 10000)

				if change == True:
					change = False
					return