import pandas as pd
from Day import Day
from Person import Person
from Course import Course

# Reading the file from the folder
xlsx = pd.ExcelFile('OEC2021_-_School_Record_Book_.xlsx')
# Reading Student Records
Student_Records = pd.read_excel(xlsx, 'Student Records')
# Reading Infected status
Infected = pd.read_excel(xlsx,'ZBY1 Status')
InfectedRows = Infected['Student ID'].values.tolist()
# Reading Teacher Records
Teacher_Records = pd.read_excel(xlsx,'Teacher Records')
# Reading TA Records
TA_Records = pd.read_excel(xlsx,'Teaching Assistant Records')

# Our main function
def main():
    # Getting all the unique classes from all the Periods
    periodOneClasses = getClassesfromPeriod("Period 1 Class")
    periodTwoClasses = getClassesfromPeriod("Period 2 Class")
    periodThreeClasses = getClassesfromPeriod("Period 3 Class")
    periodFourClasses = getClassesfromPeriod("Period 4 Class")

    #Adding all the courses in the periods
    Period1Classes = addCourses(periodOneClasses)
    Period2Classes = addCourses(periodTwoClasses)
    Period3Classes = addCourses(periodThreeClasses)
    Period4Classes = addCourses(periodFourClasses)

    #Now adding students according to grades in each class
    addPeople(1, Period1Classes)
    addPeople(2, Period2Classes)
    addPeople(3, Period3Classes)
    addPeople(4, Period4Classes)

    #Making a new Day variable which has all the periods with all classes inside them
    newDay = Day(Period1Classes, Period2Classes,
                 Period3Classes, Period4Classes)

    #Making a new excel sheet using the data
    for period in newDay.periods:
        for row in period:
            for test in row.peopleInClass:
                print(test.id,test.sickness)

def addPeople(period,classes):
    # Looping through all the classes and adding students from the excel dataframe
    for course in classes:
        people = []
        # Getting all the students that are in the course
        if period == 1:
            # Getting all the students in the given course
            people = Student_Records[Student_Records['Period 1 Class'] == (
                course.name + " " + course.section)].values.tolist()
        elif period == 2:
            # Getting all the students in the given course
            people = Student_Records[Student_Records['Period 2 Class'] == (
                course.name + " " + course.section)].values.tolist()
        elif period == 3:
            # Getting all the students in the given course
            people = Student_Records[Student_Records['Period 3 Class'] == (
                course.name + " " + course.section)].values.tolist()
        elif period == 4:
            # Getting all the students in the given course
            people = Student_Records[Student_Records['Period 4 Class'] == (
                course.name + " " + course.section)].values.tolist()

        # Declaring empty arrays for students and Infectedstudents
        studentRows = []
        infectedStudents = []

        # Looping through all the people and adding them to the periods
        for row in people:
            ID = row[0] # Id
            fname = row[1] # first name
            lname = row[2] # last name
            grade = row[3] # grade
            healthConditions = row[8] # healthConditions
            extracCurricular = row[9] # extra curicular activities

            # The id is inside the infectedPeople ID's then we just add students to the infectedStudents
            if ID in InfectedRows:
                infectedStudents.append(
                    Person(ID, lname, fname, grade, extracCurricular, healthConditions,True))

            # Adding all the student objects to the array
            studentRows.append(
                Person(ID, lname, fname, grade, extracCurricular, healthConditions,False))

        # Setting the class variables for the people
        course.peopleInClass = studentRows
        course.infectedPeople = infectedStudents

def addCourses(periodClasses):
    # Empty array for returning the courses
    returnArray = []

    # Looping over the name of the courses
    for courseName in periodClasses:
        # splitting the variable to get the name and section
        name = ""
        section = ""
        temp = courseName.split()
        if len(temp) == 2:
            name = temp[0]
            section = temp[1]
        elif len(temp) == 3:
            name = temp[0] + ' ' + temp[1]
            section = temp[2]
        # making a new class using the period,name and section
        returnArray.append(Course(name, section))
    return returnArray

def getStudentsfromPeriod(Period, class_var):
    # Getting the students from the dataframe that we have according to the class and period
    students = Student_Records.loc[Student_Records[Period] == class_var]
    return students

def getClassesfromPeriod(Period):
    # Getting the students from the dataframe that we have according to the class and period
    temp = Student_Records[Period].values.tolist()
    Period = set([])
    # Getting all the unique classes for the period as we are using a set
    for course in temp:
        if course != None:
            Period.add(course)
    return Period

# Calling the main function
main()