# -*- coding: utf-8 -*-
import random
import math

class QueueError(Exception): pass

class DeviceQueue(object):
    def __init__(self, capacity):
        if not isinstance(capacity, int) or capacity <= 0:
            raise QueueError()
        self._capacity = capacity
        self._count = 0

    def is_full(self):
        return self._capacity == self._count

    def is_empty(self):
        return self._count == 0

    def enqueue(self):
        if self.is_full():
            raise QueueError
        self._count = self._count + 1

    def dequeue(self):
        if self.is_empty():
            raise QueueError
        self._count = self._count - 1

class ModelEvent(object):
    def __init__(self, time):
        self._time = time

class GenerationEvent(ModelEvent):
    def __init__(self, time):
        super(GenerationEvent, self).__init__(time)

class ProcessingEvent(ModelEvent):
    def __init__(self, time):
        super(GenerationEvent, self).__init__(time)

class Generator(object):
    def __init__(self, excepted_value):
        self._expected_value = excepted_value

    def generate_time(self):
        return (0 - self._expected_value) * math.log(1 - random.random())

    def generate_event(self):
        return GenerationEvent(self.generate_time())

class Processor(object):
    def __init__(self, expected_value, halfrange):
        self._expected_value = expected_value
        self._halfrange = halfrange

    def generate_time(self):
        return random.uniform(self._expected_value - self._halfrange, self._expected_value + self._halfrange)

    def generate_event(self):
        return ProcessingEvent(self.generate_time())

