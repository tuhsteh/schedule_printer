

class Person:
    name = ''
    restrictions = []
    
    def __init__(self, name, restr = []):
        self.name = name
        self.restrictions = list(restr)
    
    def __str__(self):
        return self.name
    
    def isAvailable(self, date):
        return not (date in self.restrictions)
