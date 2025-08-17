import BackendCore
import dearpygui.dearpygui as gui

class Speed:
    def __init__(self):
        self._speed = False

    @property
    def speed(self):

        return self._speed
    @speed.setter
    def setSpeed(self,value):
        self._speed = value

