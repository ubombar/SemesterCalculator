
class Course():
    POINTS = {  'A+':4.0, 'A':4.0, 'A-':3.7, 
                'B+':3.3, 'B':3.0, 'B-':2.7, 
                'C+':2.3, 'C':2.0, 'C-':1.7,
                'D+':1.3, 'D':1.0, 'F':0.0, # F FX all the same
                'UE':0.0, 'SE':0.0, 'W':0.0}

    def __init__(self, cred, code, grad, name):
        self.dept = code.split(" ")[0]
        self.code = code.split(" ")[1] 
        self.name = name 
        self.cred = cred
        self.__grade = grad.upper()
        self.failpass = grad in {'UE', 'SE'}
        self.withdraw = grad in {'W'}
    
    def __str__(self):
        tmp = f"{'%.1f' % (self.credpoint)}"
        space = " " * (max(4 - len(tmp), 0))
        space2 = " " * (max(8 - len(self.coursecode), 0))

        head = f"[{tmp}] {space} {self.cred} cred {self.grade}"

        if self.failpass or self.withdraw:
            head = f"[N\A] {space} {self.cred} cred {self.grade}"

        return f"{head} \t{self.coursecode} {space2} {self.name}"
    
    def notcalculate(self):
        return self.failpass or self.withdraw

    @property
    def grade(self):
        return self.__grade
    
    @property
    def point(self):
        return Course.POINTS[self.grade]

    @property
    def credpoint(self): # get point * credit
        return self.point * self.cred

    @property
    def coursecode(self):
        return f"{self.dept} {self.code}"

class Semester():
    def __init__(self, name, courses):
        self.courses = courses
        self.name = name

    def __str__(self):

        tmp = f"courses: {self.numcourse} \t credits: {self.allcredits}({self.gpacredits}) \t gpa: {'%.2f' % self.gpa} \tname: {self.name}\n"

        for course in self.courses:
            tmp += f"\t{course}\n"
        
        return tmp

    @property
    def shortstr(self):
        return f"courses: {self.numcourse} \t credits: {self.allcredits}({self.gpacredits}) \t gpa: {'%.2f' % self.gpa} \tname: {self.name}\n"
    
    @property
    def numcourse(self):
        return len(self.courses)

    @property
    def allcredits(self):
        return self.__credits(True)

    @property
    def gpacredits(self):
        return self.__credits(False)
    
    def __credits(self, incall=False):
        cred = 0
        for course in self.courses:
            if not incall:
                if course.grade not in {'UE', 'SE', 'W'}:
                    cred += course.cred
            else:
                cred += course.cred
        return cred

    def __points(self, incall=False): # include all courses (SE UE and W) when calc gpa they are not included
        point = 0
        for course in self.courses:
            if not incall:
                if course.grade not in {'UE', 'SE', 'W'}:
                    point += course.point
            else:
                point += course.point
                
        return point

    def __credpoints(self, incall=False): # include all courses (SE UE and W) when calc gpa they are not included
        point = 0
        for course in self.courses:
            if not incall:
                if course.grade not in {'UE', 'SE', 'W'}:
                    point += course.credpoint
            else:
                point += course.credpoint
                
        return point

    @property
    def allpoints(self):
        return self.__points(True)

    @property
    def gpapoints(self):
        return self.__points(False)
    
    @property
    def gpa(self):
        if self.gpacredits == 0:
            return 0.0
        return self.gpacredpoints / self.gpacredits

    @property
    def allcredpoints(self):
        return self.__credpoints(True)

    @property
    def gpacredpoints(self):
        return self.__credpoints(False)

class Program():
    def __init__(self):
        self.semesters = list()
    
    @property
    def agpa(self):
        totalpoints = 0.0
        totalcredits = 0.0

        for semester in self.semesters:
            totalpoints += semester.gpacredits * semester.gpa
            totalcredits += semester.gpacredits

        if totalcredits == 0:
            return 0.0
        return totalpoints / totalcredits
    
    @property
    def gpa(self):
        calculated = set() # holds the codes that are already calculated!

        totalpoints = 0.0
        totalcredits = 0.0

        for semester in reversed(self.semesters): # go from last to first
            for course in semester.courses:
                if course.coursecode in calculated: continue

                if course.notcalculate(): continue

                totalpoints += course.credpoint
                totalcredits += course.cred

                calculated.add(course.coursecode)

        if totalcredits == 0:
            return 0.0
        return totalpoints / totalcredits

    @property
    def cset(self):
        cset = set()
        for semester in self.semesters:
            for course in semester.courses:
                cset.add(course.coursecode)
        return cset
    
    def __str__(self):
        temp = f"semesters: {len(self.semesters)} \t courses taken: {len(self.cset)}\n"

        for semester in self.semesters:
            temp += f"\t{semester.shortstr}"

        if self.gpa < 2.0:
            rank = "UNSATISFACTORY"
        elif self.gpa < 3.0:
            rank = "SATISFACTORY"
        elif self.gpa < 3.5:
            rank = "HONOR"
        else:
            rank = "HIGH HONOR"

        line = f"agpa: {'%.2f' % self.agpa} \t gpa: {'%.2f' % self.gpa} \t rank: {rank}\n"


        return f"{temp}{line}"

# Modify those below
# Note there should be a space between department and code like 'CS 101'

year1fall = Semester('2017-2018 Fall', 
        [
        Course(4, "CS 101",     "A",  "Algorithms and Programming I"),
        Course(3, "ENG 101",    "C-", "English and Composition I"),
        Course(1, "GE 100",     "A",  "Orientation I"),
        Course(4, "MATH 101",   "B",  "Calculus I"),
        Course(3, "MBG 110",    "A-", "Modern Biology"),
        Course(2, "TURK 101",   "W",  "Turkish I"),
        Course(1, "PE 110",     "B-", "Tennis"),
        Course(0, "GE 250",     "SE", "College Activities Program I"),
        ])
year1spring = Semester('2017-2018 Spring', 
        [
        Course(4, "CS 102",     "A-", "Algorithms and Programming I"),
        Course(3, "ENG 101",    "F",  "English and Composition I"),
        Course(4, "MATH 102",   "C+", "Calculus II"),
        Course(3, "MATH 132",   "C+", "Modern Biology"),
        Course(2, "TURK 101",   "C+", "Turkish I"),
        Course(2, "TURK 102",   "C",  "Turkish II"),
        Course(1, "GE 251",     "A",  "College Activities Program II"),
        ])

# SECOND YEAR
year2fall = Semester('2018-2019 Fall', 
        [
        Course(3, "CS 201",     "C+", "Fundemental Structures of Computer Science I"),
        Course(3, "ENG 101",    "B+",  "English and Composition I"),
        Course(4, "CS 223",     "C-", "Digital Deisgn"),
        Course(4, "MATH 225",   "D",  "Linear Algebra and Differantial Equations"),
        Course(4, "PHYS 101",   "C+", "General Physics I"),
        ])
year2spring = Semester('2018-2019 Spring', 
        [
        Course(3, "CS 202",     "C+", "Fundemental Structures of Computer Science II"),
        Course(3, "ENG 102",    "B",  "English and Composition II"),
        Course(4, "CS 224",     "C-", "Copmuter Organization"),
        Course(4, "CS 319",     "B",  "Object Oriented Software Engineering"),
        Course(4, "PHYS 102",   "B", "General Physics II"),
        Course(4, "HIST 200",   "B",  "History of Turkey"),
        ])
# THIRD YEAR
year3fall = Semester('2019-2020 Fall', 
        [
        Course(0, "CS 299",     "SE", "Summer Training I"),
        Course(3, "CS 201",     "B",  "Fundemental Structures of Computer Science I"),
        Course(3, "CS 315",     "C",  "Programming Languages"),
        Course(3, "EEE 391",    "C-", "Signals and Systems"),
        Course(3, "HART 239",   "A-", "Latin I"),
        Course(3, "MATH 230",   "B-", "Probability and Statistics"),
        ])
year3spring = Semester('2019-2020 Spring', 
        [
        Course(4, "CS 342",     "UE",   "Operating Systems"),
        Course(3, "CS 353",     "SE",   "Database Systems"),
        Course(3, "CS 421",     "SE",   "Computer Networks"),
        Course(3, "CS 464",     "UE",   "Machine Learning"),
        Course(2, "ENG 401",    "B",    "Technical Report Writing"),
        Course(3, "HART 240",   "B",    "Latin II"),
        ])

# FOURTH YEAR
year4fall = Semester('2020-2021 Fall', 
        [
        Course(3, "HUM 111",     "C+",   "Cultures Civilizations and Ideas I"),
        Course(3, "PSYC 100",    "A-",   "Introduction to Psychology"),
        Course(3, "EEE 391",     "B",    "Signals and Systems"),
        Course(3, "CS 484",      "A+",   "Computer Vision"),
        Course(3, "CS 491",      "A-",   "Senor Design Project I"),
        Course(0, "CS 399",      "SE",   "Summer Training II"),
        ])
year4spring = Semester('2020-2021 Spring', 
        [
        Course(4, "CS 342",      "B",   "Operating Systems"),
        Course(3, "CS 464",      "B+",  "Machine Learning"),
        Course(3, "IE 400",      "W",   "Principles of Engineering Management"),
        Course(3, "HUM 112",     "B+",  "Cultures Civilizations and Ideas II"),
        Course(3, "CS 492",      "A",   "Senor Design Project II"),  
        ])
year4summer = Semester('2020-2021 Summer', 
        [
        Course(2, "GE 301",      "A-",   "Science Technology and Society"),
        Course(3, "CS 426",      "A",   "Parallel Computing"),
        ])


year5fall = Semester('Additional Fall', 
        [
        Course(3, "CS 473",      "B+",   "Algorithms I"),
        Course(3, "CS 476",      "A-",   "Automata Theory and Formal Languages"),
        Course(3, "IE 400",      "A",   "Principles of Engineering Management"),
        Course(3, "CS 483",      "A-",   "Elective"),
        ])

program = Program()

program.semesters += [  year1fall, year1spring, 
                        year2fall, year2spring, 
                        year3fall, year3spring,
                        year4fall, year4spring, year4summer,
                        year5fall]

print(program) # print last 3 semesters
# print(year4spring)
# print(year5fall)

# print(program) # print statistics


