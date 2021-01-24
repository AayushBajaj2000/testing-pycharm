class Day():
    def __init__(self, period1, period2, period3, period4):
        self.periods = [period1, period2, period3, period4]
        self.courseNames = {}
        self.determineSpread()

    def determineSpread(self):
        for period in self.periods:
            for course in period:
                courseName = course.name + " " + course.section
                peopleInClass = course.peopleInClass
                infectedPeople = course.infectedPeople
                oldInfectedPeople = 0
                oldPeople = 0

                if courseName not in self.courseNames:
                    self.courseNames[courseName] = [
                        oldInfectedPeople, len(peopleInClass)]
                else:
                    oldPeople = self.courseNames[courseName][1]
                    oldInfectedPeople = self.courseNames[courseName][0]
                    del self.courseNames[courseName]

                pointsByContact = ((len(infectedPeople) *
                                    3) / len(peopleInClass)) * 100
                if oldInfectedPeople == 0:
                    pointsByGerms = 0
                else:
                    pointsByGerms = (oldInfectedPeople /
                                     (oldPeople + oldInfectedPeople)) * 100

                totalSickPoints = pointsByContact + pointsByGerms

                for person in peopleInClass:
                    person.updateInfection(totalSickPoints)

                course.updatedInfected()