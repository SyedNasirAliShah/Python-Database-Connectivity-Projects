import mysql.connector as myconn

class Student:
    def __init__(self):
        try:
            self.conn = myconn.connect(
                host = "localhost",
                user = "****",
                password = "*******",
                database = "college"
            )
            self.cursor = self.conn.cursor()
            self.stdDict = {}
            self.loadDataFromDB()
        except myconn.Error as err:
            print(f"Error: {err}")


    def loadDataFromDB(self):
        query = "SELECT * FROM student"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.stdDict = {record[0]: {"name": record[1], "dep": record[2], "semester": record[3], "cgpa": record[4]} for record in records}
        print(f"Loaded {len(self.stdDict)} from database...\n\n")


    def addStudent(self, rollno, name, dep, semester, cgpa):
        if None in [rollno, name, dep, semester, cgpa]:
            print("Missing data, cannot add student.")
            return
        if rollno in self.stdDict:
            print(f"rollno {rollno} already exists.. please enter another")
            return
        self.stdDict[rollno] = {"name":name, "dep":dep, "semester": semester, "cgpa": cgpa}
        query = """CREATE TABLE IF NOT EXISTS student
        (rollno INT PRIMARY KEY,
         name VARCHAR(20),
         dep VARCHAR(20),
         semester VARCHAR(20),
         cgpa FLOAT(3, 2))""" 
        self.cursor.execute(query)
        query = f"INSERT INTO student(rollno, name, dep, semester, cgpa) VALUES (%s, %s, %s, %s, %s)"
        values = (rollno, name, dep, semester, cgpa)
        self.cursor.execute(query, values)
        self.conn.commit()
        
    def removeStudent(self, rollno):
        if rollno in self.stdDict:
            query = "DELETE FROM student WHERE rollno = %s"
            value = (rollno,)
            self.cursor.execute(query, value)
            self.conn.commit()
            del self.stdDict[rollno]
            print(f"Removed Successfully...")
        else:
            print(f"RollNo {rollno} not in  records...")

    def searchStudent(self, rollno):
        if rollno in self.stdDict:
            for key, values in self.stdDict.items():
                if rollno == key:
                    print(f"Rollno: {rollno}, name: {values['name']}, department: {values['dep']}, semester: {values['semester']}, CGPA: {values['cgpa']} ")
                    return
        else:
            print(f"The student's rollno {rollno} is not exist.")
            


    def updateSingleFeild(self, rollno, feild):
        if rollno in self.stdDict:
            match(feild):
                case "rollno":
                    try:
                        newRollno = int(input("Enter new RollNo: "))
                        if newRollno in self.stdDict:
                            print(f"Rollno is already exists. Please enter another rollno")
                            return
                    except ValueError:
                        print("Please enter the integer value")
                    query = "UPDATE student SET rollno = %s Where rollno = %s"
                    values = (newRollno, rollno)
                    self.cursor.execute(query, values)
                    self.conn.commit()
                    self.stdDict[newRollno] = self.stdDict.pop(rollno)

                case "name":
                    newName = input("Enter new name: ")
                    query = "UPDATE student SET name = %s Where rollno = %s"
                    values = (newName, rollno)
                    self.cursor.execute(query, values)
                    self.conn.commit()
                    self.stdDict[rollno]["name"] = newName

                case "dep":
                    newDep = input("Enter new department: ")
                    query = "UPDATE student SET dep = %s Where rollno = %s"
                    values = (newDep, rollno)
                    self.cursor.execute(query, values)
                    self.conn.commit()
                    self.stdDict[rollno]["dep"] = newDep

                case "semester":
                    newSemester = input("Enter new semester: ")
                    query = "UPDATE student SET semester = %s Where rollno = %s"
                    values = (newSemester, rollno)
                    self.cursor.execute(query, values)
                    self.conn.commit()
                    self.stdDict[rollno]["semester"] = newSemester

                case "cgpa":
                    try:
                        newCgpa = float(input("Enter new cgpa: "))
                    except ValueError:
                        print("Please enter the float value for CGPA.")
                    query = "UPDATE student SET cgpa = %s Where rollno = %s"
                    values = (newCgpa, rollno)
                    self.cursor.execute(query, values)
                    self.conn.commit()
                    self.stdDict[rollno]["cgpa"] = newCgpa

                case _:
                    print("Feild does not exist.")
        else:
            print(f"The rollno {rollno} is not exists")
    

    def updateAllFeilds(self, rollno, newRollno, newName, newDep, newSemester, newCgpa):
        if rollno in self.stdDict:
            if  newRollno in self.stdDict:
                print("The rollno is already exists")
                return
            query = "UPDATE student SET rollno = %s, name = %s, dep = %s, semester = %s, cgpa = %s where rollno = %s"
            values = (newRollno, newName, newDep, newSemester, newCgpa, rollno)
            self.cursor.execute(query, values)
            self.conn.commit()
            self.stdDict[newRollno] = self.stdDict.pop(rollno)
            self.stdDict[newRollno].update({"name":newName, "dep": newDep, "semester": newSemester,"cgpa":newCgpa})
            print(f"Updated Successfully...")
        else:
            print(f"The rollno {rollno} is not found")       


    def displayRecords(self, choice):
        match(choice):
            case 1:
                if not self.stdDict:
                    print("No record(s) found")
                else:
                    for rollno, details in self.stdDict.items():
                        print(f"Rollno: {rollno}, name: {details['name']}, department: {details['dep']}, semester: {details['semester']}, CGPA: {details['cgpa']} ")
                        print("-"*70)
            case 2:
                query = "SELECT * FROM student"
                self.cursor.execute(query)
                records = self.cursor.fetchall()
                for record in records:
                    print(record)
            case _:
                print("INVALID INPUT.")
                return

    def isExist(self, rollno):
        if not rollno in self.stdDict:
            return False
        else:
            return True

    def closeConnection(self):
        self.cursor.close()
        self.conn.close()

def main():
    student = Student()
    while True:
        print("SELECT CHOICE FROM THE MENU")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Update Single Feild")
        print("4. Update All Feilds")
        print("5. Search Student")
        print("6. Display All Records")
        print("7. Exit")
        try:
            choice = int(input("Enter your choice: "))
            match(choice):
                case 1:
                    try:
                        rollno = int(input("Enter the rollno of student: "))
                    except ValueError:
                        print("Please enter integer value")
                        continue
                    name = input("Enter the name of student: ")
                    dep = input("Enter the department of student: ")
                    semester = input("Enter the semester of student: ")
                    try:
                        cgpa = float(input("Enter the CGPA of student: "))
                    except Exception as e:
                        print("Please enter the float value for CGPA")
                        continue
                    student.addStudent(rollno, name, dep, semester, cgpa)
                case 2:
                    try:
                        rollno = int(input("Enter the rollno of student you want to remove: "))
                    except ValueError:
                        print("Please enter integer value")
                        continue
                    student.removeStudent(rollno)
                case 3:
                    try:
                        rollno = int(input("Enter the rollno for feild: "))
                    except ValueError:
                        print("Please enter integer value")
                        continue
                    feild = input("Enter the feildname you want to update: ")
                    student.updateSingleFeild(rollno, feild)
                case 4:
                    try:
                        rollno = int(input("Enter rollno of student you want to update: "))
                    except ValueError:
                        print("Please enter integer value")
                        continue
                    if student.isExist(rollno):
                        try:
                            newRollno = int(input("Enter the new rollno of student: "))
                        except ValueError:
                            print("Please enter the integer value")
                            continue
                        newName = input("Enter the new name of student: ")
                        newDep = input("Enter the new department of student: ")
                        newSemester = input("Enter the new semester of student: ")
                        try:
                            newCgpa = float(input("Enter the nwe CGPA of student: "))
                        except ValueError:
                            print("Please enter float value for CGPA")
                            continue
                        student.updateAllFeilds(rollno, newRollno, newName, newDep, newSemester, newCgpa)
                    else:
                        print("Rollno is not exist in student records.")
                case 5:
                    try:
                        rollno = int(input("Enter the  rollno you want to search"))
                    except ValueError:
                        print("Please enter integer value")
                        continue
                    student.searchStudent(rollno)
                case 6:
                    ch = int(input("You want to see the data in 1. python dict 2. SQL records"))
                    student.displayRecords(ch)

                case 7:
                    student.closeConnection()
                    print("Exiting Program...")
                    break
                case _:
                    print("INVALID CHIOICE.")
        except Exception as e:
            print(e)
    

if __name__ == "__main__":
    main()