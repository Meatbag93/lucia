# Original code by Carter Tem
# Used in Lucia with permition

import os
import math
import sound_lib
from sound_lib import stream
import ctypes
import lucia


class Sound(lucia.audio.Sound):
	def __init__(self):
		self.handle = None
		self.freq = 44100

	def load(self, filename=""):
		if self.handle:
			self.close()
		if lucia.get_global_resource_file() is not None:
			try:
				filename = lucia.get_global_resource_file().get(filename)
			except KeyError:  # the file doesn't exist in the pack file.
				if os.path.isfile(filename) == False:
					return
		self.handle = stream.FileStream(file=filename)
		self.freq = self.handle.get_frequency()

	def stream(self, data):
		if self.handle:
			self.close()
		if not data:
			return
		data = ctypes.create_string_buffer(data)
		self.handle = stream.FileStream(mem=True, file=ctypes.addressof(data), length=len(data))

	def play(self):
		if self.handle is None:
			return
		self.handle.looping = False
		self.handle.play()

	def play_wait(self):
		if self.handle is None:
			return
		self.handle.looping = False
		self.handle.play_blocking()

	def play_looped(self):
		if self.handle is None:
			return
		self.handle.looping = True
		self.looping = True
		self.handle.play()

	def stop(self):
		if self.handle and self.handle.is_playing:
			self.handle.stop()
			self.handle.set_position(0)

	def get_source_object(self):
		return self.handle

	def pause(self):
		if self.handle is None:
			return
		self.handle.pause()

	def resume(self):
		if self.handle is None:
			return
		self.handle.resume()

	@property
	def volume(self):
		if not self.handle:
			return False
		return round(math.log10(self.handle.volume) * 20)

	@volume.setter
	def volume(self, value):
		"""Volume between 0 (full volume) to -100 silence"""
		if not self.handle:
			return False
		vol = 10 ** (float(value) / 20)
		if vol > 1.0:
			vol = 1.0
		self.handle.set_volume(vol)

	@property
	def pitch(self):
		if not self.handle:
			return False
		return (self.handle.get_frequency() / self.freq) * 100

	@pitch.setter
	def pitch(self, value):
		if not self.handle:
			return False
		self.handle.set_frequency((float(value) / 100) * self.freq)

	@property
	def pan(self):
		if not self.handle:
			return False
		return self.handle.get_pan() * 100

	@pan.setter
	def pan(self, value):
		if not self.handle:
			return False
		self.handle.set_pan(float(value) / 100)

	def close(self):
		if self.handle:
			self.handle.free()
			self.__init__()

