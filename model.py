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

    def clear(self):
        self._count = 0

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

    def get_planned_time(self):
        return self._time

class GenerationEvent(ModelEvent):
    def __init__(self, time):
        super(GenerationEvent, self).__init__(time)

    def __repr__(self):
        return "Generate at %f" % self.get_planned_time()

class ProcessingEvent(ModelEvent):
    def __init__(self, time):
        super(ProcessingEvent, self).__init__(time)
        print("PROCESSING EVENT CREATED and planed to %f", time)

    def __repr__(self):
        return "Process at %f" % self.get_planned_time()

class Generator(object):
    def __init__(self, excepted_value):
        self._expected_value = excepted_value

    def generate_time(self):
        return (0 - self._expected_value) * math.log(1 - random.random())

    def generate_event(self, model_time):
        return GenerationEvent(self.generate_time() + model_time)

class Processor(object):
    def __init__(self, expected_value, halfrange):
        self._expected_value = expected_value
        self._halfrange = halfrange

    def generate_time(self):
        return random.uniform(self._expected_value - self._halfrange, self._expected_value + self._halfrange)

    def generate_event(self, model_time):
        return ProcessingEvent(self.generate_time() + model_time)

class Model(object):
    eps = 0.001

    def __init__(self, gen_expected_value, process_expected_value, process_halfrange, queue_capacity, with_return=False):
        self._generator = Generator(gen_expected_value)
        self._processor = Processor(process_expected_value, process_halfrange)
        self._queue = DeviceQueue(queue_capacity)
        self._events_list = []
        self._model_time = 0
        self._with_return = with_return

    def reinit(self):
        self._queue.clear()
        self._events_list = []
        self._model_time = 0

    def handle_generation(self):
        self._events_list.insert(0, self._generator.generate_event(self._model_time))
        if self._queue.is_full():
            #print("AT %f rejected, queue size = %d" % (self._model_time, self._queue._count))
            self._events_list.sort(key=lambda x: x.get_planned_time(), reverse=True)
            return False
        else:
            self._queue.enqueue()
            #print("AT %f generated" % self._model_time)
        self._events_list.insert(0, self._processor.generate_event(self._model_time))
        self._events_list.sort(key=lambda x: x.get_planned_time(), reverse=True)
        #print(self._events_list)
        return True

    def handle_processing(self):
        #print("AT %f processed" % self._model_time)
        if self._with_return:
            self._events_list.insert(0, self._processor.generate_event(self._model_time))
            self._events_list.sort(key=lambda x: x.get_planned_time(), reverse=True)
        else:
            self._queue.dequeue()
            return True


    def handle_event(self, ev, processed, rejected):
        print(repr(ev))
        if isinstance(ev, GenerationEvent):
            if self.handle_generation():
                return (processed, rejected)
            else:
                return (processed + 1, rejected + 1)
        elif isinstance(ev, ProcessingEvent):
            self.handle_processing()
            return (processed + 1, rejected)
        else:
            assert 0

    def run_dt(self, dt, to_process):
        self.reinit()
        processed = 0
        rejected = 0

        while processed < to_process:
            while True:
                try:
                    ev = self._events_list.pop()
                except IndexError:
                    self._events_list.insert(0, self._generator.generate_event(self._model_time))
                    self._events_list.sort(key=lambda x: x.get_planned_time(), reverse=True)
                    break

                if math.fabs(ev.get_planned_time() - self._model_time) < Model.eps: # process event
                    (processed, rejected) = self.handle_event(ev, processed, rejected)
                    if processed < to_process:
                        continue
                    else:
                        break
                elif ev.get_planned_time() < self._model_time: # timeout of event
                    print("timeout")
                    continue
                elif ev.get_planned_time() > self._model_time: # return to queue
                    self._events_list.insert(0, ev)
                    self._events_list.sort(key=lambda x: x.get_planned_time(), reverse=True)
                    break

            self._model_time = self._model_time + dt
        return self._model_time, rejected

model = Model(27, 27, 27, 1, True)
print(model.run_dt(0.001, 100))

