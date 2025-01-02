from dateutil import parser
import datetime as dt
import random

import comms_pb2

valid_types = ['bool', 'int', 'float', 'str', 'time']
words = ['In', 'the', 'kitchen', 'the', 'breakfast', 'stove', 'gave', 'a', 'hissing', 'sigh', 'and', 'ejected', 'from', 'its', 'warm', 'interior', 'eight', 'pieces', 'of', 'perfectly', 'browned', 'toast,', 'eight', 'eggs', 'sunny', 'side', 'up,', 'sixteen', 'slices', 'of', 'bacon,', 'two', 'coffees,', 'and', 'two', 'cool', 'glasses', 'of', 'milk.']

class Point(object):
    """ The DummyPoint class can hold one of several value types: bool, int, 
    float, string.
    """
    def __init__(self, _type:str):
        self.value = None
        self.SetDefault(_type)
        self.access_counter = 0

    def set_value(self, value) -> bool:
        try:
            if type(self.value) is bool:
                if value.lower() in ['true', '1']:
                    self.value = True
                elif value.lower() in ['false', '0']:
                    self.value = False            

            elif type(self.value) is int:
                self.value = int(value)
            elif type(self.value) is float:
                self.value = float(value)
            elif type(self.value) is str:
                self.value = value
            elif type(self.value) is dt.datetime:
                self.value = parser.parse(value)
        except ValueError as e:
            print(e)

    def MutateValue(self):
        self.access_counter += 1
        if type(self.value) is bool:
            self.value = not self.value
        elif type(self.value) is int:
            if random.random() > 0.5:
                self.value += 1
            else:
                self.value -= 1
        elif type(self.value) is float:
            if random.random() > 0.5:
                self.value += 0.5
            else:
                self.value -= 0.25
        elif type(self.value) is str:
            self.value = words[self.access_counter % len(words)]
        elif type(self.value) is dt.datetime:
            self.value = dt.datetime.now()


    def SetDefault(self, type_str:str):
        # print('recevied type_str: "{}"'.format(type_str))
        if type_str == 'bool':
            self.value = False
        elif type_str == 'int':
            self.value = 100
        elif type_str == 'float':
            self.value = 1.5
        elif type_str == 'str':
            self.value = words[0]
        elif type_str == 'time':
            self.value = dt.datetime.now()
        else:
            self.value = 'error: unrecognized type_str "{}"'.format(type_str)


class Device(object):
    """ The Device class holds a collection of DummyPoints that can be 
    """
    def __init__(self):
        self.name = ""
        self.points = {}

    def add_point(self, _type:str, _id:str):
        self.points[_id] = Point(_type)

    def get_point(self, _id:str):
        if _id in self.points:
            return self.points[_id].value
        else:
            return Device
    
    def set_point(self, _id:str, value) -> bool:
        if _id in self.points:
            # and self.points[_id].isWritable()
            self.points[_id].set_value(value)
            return True
        else:
            return False
    
    def mutate_point(self, _id:str):
        if _id in self.points:
            self.points[_id].MutateValue()


def GetDtype(value):
    t = type(value)
    if t == bool:
        return comms_pb2.BOOL
    if t == int:
        return comms_pb2.INT64
    if t == float:
        return comms_pb2.FLOAT
    if t == str:
        return comms_pb2.STRING
    else:
        return comms_pb2.UNSPECIFIED