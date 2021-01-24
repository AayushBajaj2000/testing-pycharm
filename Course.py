class Course:
    def __init__(self, name, section):
        self.name = name
        self.section = section
        self.peopleInClass = []
        self.infectedPeople = []

    def addPerson(self, Person):
        self.peopleInClass.append(Person)

        if Person.infected:
            self.infectedPeople.append(Person)

    def updatedInfected(self):
        for person in self.peopleInClass:
            if (person.infected == True):
                if person not in self.infectedPeople:
                    self.infectedPeople.append(person)



