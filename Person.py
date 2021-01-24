# PERSON CLASS - Used to make an Object for any student, ta, teacher at any given time
class Person():
    def __init__(self, id, lname, fname, grade, extracCurricular, conditions, infected):
        self.id = id
        self.lname = lname
        self.fname = fname
        self.grade = grade
        self.extracCurricular = extracCurricular
        self.conditions = conditions
        self.sickness = 0
        self.infected = False
        self.gradeFactor = (1.25 ** (grade - 9))
        self.healthFactor = 1.7 if conditions else 0
        self.threshold = 10

    def updateInfection(self, totalPoints):
        self.sickness += (totalPoints * self.gradeFactor) * self.healthFactor
        if self.sickness >= self.threshold:
            self.infected = True
