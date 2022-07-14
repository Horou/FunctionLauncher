import numpy

from FunctionLauncher.FunctionLauncher import FunctionLauncher
from FunctionLauncher.JsonObjectEncoder import JsonObjectEncoder


####################################################################

class Address:
    def __init__(self):
        self.name = "name"
        self.surname = "surname"
        self.zip_code = 46130
        self.coordinate = 123.456789
        self.coordinate32 = numpy.float32(123.456789)
        self.nothing = None
        self.is_bool = True


class Personne:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.did_you_win = False
        self.address = Address()
        self.heavy_shit = {
            ("temp", numpy.float32(123.456789)): Address()
        }
        self.super_heavy_shit = [
            {
                ("temp", numpy.float32(123.456789)): Address()
            },
            {
                ("temp", 123.456789): Address()
            }
        ]
        self.capacity_tester1 = "#"*66000

    def testeur(self, something, cool, hell_yeah="brodha"):
        self.did_you_win = True
        return "You Win"


class PersonneMirror(Personne):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.did_you_win = False

    @FunctionLauncher("localhost", 8069)
    def testeur(self, something, cool, hell_yeah="brodha"):
        return "You Lose"


if __name__ == "__main__":
    instance = PersonneMirror("nicolas", "nemouthe")
    result = instance.testeur("something", "cool", hell_yeah="brodha2")
    print(">>>>>instance<<<<<: \n" + JsonObjectEncoder.dumps(instance, indent="    "))
    print(">>>>>Function return<<<<<: " + str(result))
    result = instance.testeur("something", "cool", hell_yeah="brodha2")
    print(">>>>>instance<<<<<: \n" + JsonObjectEncoder.dumps(instance, indent="    "))
    print(">>>>>Function return<<<<<: " + str(result))
