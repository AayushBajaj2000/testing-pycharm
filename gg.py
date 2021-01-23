import pandas as pd

# Reading the file from the folder
xlsx = pd.ExcelFile('OEC2021_-_School_Record_Book_.xlsx')
# Reading Student Records
Student_Records = pd.read_excel(xlsx, 'Student Records')

# Reading Teacher Records
# Teacher_Records = pd.read_excel(xlsx,'Teacher Records')

# Reading TA Records
# TA_Records = pd.read_excel(xlsx,'Teaching Assistant Records')

# Reading Infected status
# Infected = pd.read_excel(xlsx,'ZBY1 Status')
# students = Student_Records.loc[Student_Records['Period 1 Class'] == #"Physics A"][['First Name','Last Name']]

# print(getStudentsfromPeriod("Period 1 Class","Physics B"))

# All classes in the period

def main():
    # Getting all the unique classes from all the Periods
    periodOneClasses = getClassesfromPeriod("Period 1 Class")
    periodTwoClasses = getClassesfromPeriod("Period 2 Class")
    periodThreeClasses = getClassesfromPeriod("Period 3 Class")
    periodFourClasses = getClassesfromPeriod("Period 4 Class")

    Period1Classes = addCourses(1,periodOneClasses)
    Period2Classes = addCourses(2,periodTwoClasses)
    Period3Classes = addCourses(3, periodThreeClasses)
    Period4Classes = addCourses(4, periodFourClasses)

    # making a new Day variable which has all the periods with all classes inside them
    newDay = Day(Period1Classes, Period2Classes, Period3Classes, Period4Classes)

    #Now adding students according to grades in each class
    addStudents(newDay.period1)

def addStudents(period):
    #Looping through all the classes and adding students from the excel dataframe
    for x in period:
        Student_Records[Student_Records['Period 1 Class'] == (x.name + ' ' + x.section)]

def addCourses(period,periodClasses):
    returnArray = []
    for x in periodClasses:
        # splitting the variable to get the name and section
        name = ""
        section = ""
        temp = x.split()
        if len(temp) == 2:
            name = temp[0]
            section = temp[1]
        elif len(temp) == 3:
            name = temp[0] + ' ' + temp[1]
            section = temp[2]
        # making a new class using the period,name and section
        returnArray.append(Course(period, name, section))
    return returnArray

def getStudentsfromPeriod(Period, class_var):
    # Getting the students from the dataframe that we have according
    # to the class and period
    students = Student_Records.loc[Student_Records[Period] == class_var]
    return students

def getClassesfromPeriod(Period):
    # Getting the students from the dataframe that we have according
    # to the class and period
    test = Student_Records[Period].values.tolist()
    Period = set([])
    # Getting all the unique classes for the period
    for x in test:
        if x != None:
            Period.add(x)
    return Period

class Course:
    def __init__(self, period, name, section):
        self.name = name
        self.period = period
        self.section = section
        self.spreadability = 0
        self.gr9 = []
        self.gr10 = []
        self.gr11 = []
        self.gr12 = []
        self.teacher = ""
        self.tas = []

        def setTeacher(self, teacher):
            self.teacher = teacher

        def addTA(self, ta):
            self.tas.append(ta)

        def calculateSpreadabilityAvg(self):
            sum = 0
            for s in self.gr9:
                sum += s.spreadability
            for s in self.gr10:
                sum += s.spreadability
            for s in self.gr11:
                sum += s.spreadability
            for s in self.gr12:
                sum += s.spreadability
            for t in self.tas:
                sum += t.spreadability

            sum += self.teacher.spreadability
            self.spreadability = sum / len(self.students)

        def spreadToClass(self):
            for s in self.gr9:
                s.setSpreadability(self.spreadability)
                s.setInfection()
            for s in self.gr10:
                s.setSpreadability(self.spreadability)
                s.setInfection()
            for s in self.gr11:
                s.setSpreadability(self.spreadability)
                s.setInfection()
            for s in self.gr12:
                s.setSpreadability(self.spreadability)
                s.setInfection()
            for s in self.tas:
                s.setSpreadability(self.spreadability)
                s.setInfection()

            self.teacher.setSpreadability(self.spreadability)
            self.teacher.setInfection()

        def __str__(self):
            return (str(self.name) + " - The current infection rate in this class is: " + str(self.spreadability))

class Day():
    def __init__(self, period1, period2, period3, period4):
        self.period1 = period1
        self.period2 = period2
        self.period3 = period3
        self.period4 = period4


# Teacher CLASS - Used to Objectize a student during any given moment
class Teacher():
    def __init__(self, id, lname, fname):
        self.id = id
        self.lname = lname
        self.fname = fname
        self.ageFactor = 1.5 * 1.5 * 1.5 * 1.5 * 1.5 * 1.5
        self.spreadability = 0
        self.infectious = 0

    def setSpreadability(self, spread):
        self.spreadability = spread * (self.infectious + 1)

    def setInfection(self):
        self.infectious = (1 + self.spreadability) * self.infectious
        self.infectious = (1 + self.ageFactor) * self.infectious

        if self.infectious >= 0.75:
            self.infectious = 1


# TA CLASS - Used to Objectize a student during any given moment
class Ta():
    def __init__(self, id, lname, fname):
        self.id = id
        self.lname = lname
        self.fname = fname
        self.ageFactor = 1.5 * 1.5 * 1.5 * 1.5
        self.spreadability = 0
        self.infectious = 0

    def setSpreadability(self, spread):  # spreadability is determined by how sick they are
        self.spreadability = spread * (self.infectious + 1)

    def setInfection(self):  # their chance of sickness is determined by if they have any infections and their age
        self.infectious = (1 + self.spreadability) * self.infectious
        self.infectious = (1 + self.ageFactor) * self.infectious

        if self.infectious >= 0.75:  # if they have 75% chance of being sick, they will be sick
            self.infectious = 1

# STUDENT CLASS - Used to make an Object for any student at any given time
class Student():
    def __init__(self, id, lname, fname, grade, conditions):
        self.id = id
        self.lname = lname
        self.fname = fname
        self.grade = grade
        self.spreadability = 0
        self.infectious = 0
        self.healthConditions = 0.7 if conditions else 0  # this should just be a True or False variable

    def setSpreadability(self, spread):
        self.spreadability = spread * (self.infectious + 1)

    def setInfection(self):
        gradeFactor = 0
        if self.grade == 9:
            gradeFactor = 1.5
        elif self.grade == 10:
            gradeFactor = 1.5 * 1.25
        elif self.grade == 11:
            gradeFactor = 1.5 * 1.5
        elif self.grade == 12:
            gradeFactor = 1.5 * 1.5 * 1.25

        self.infectious = (1 + self.spreadability) * self.infectious
        self.infectious = (1 + gradeFactor) * self.infectious

        if self.infectious >= 0.75:
            self.infectious = 1

main()