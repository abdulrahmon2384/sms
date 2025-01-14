import random, uuid
from random import choice, sample
from datetime import datetime, timedelta
from .models.admin_model import School_information, Admin, Announcements, Events
from .models.student_model import Students, Student_attendance, Student_fee, Results, Classes
from .models.teacher_model import Teachers, Teacher_attendance
from . import app, bcrypt, db
from faker import Faker


fake = Faker()
password = "password"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


class_ = {
	           'KG1':{}, "KG2": {}, 
	          'PRIMARY1': {}, 'PRIMARY2': {}, 
	          'PRIMARY3': {}, 'PRIMARY4': {},
	          'PRIMARY5': {}, 'PRIMARY6': {}
}


EXPENSES = {"first term":
 {
  "First Aid": 100000, 
  "School Maintanance": 35000, 
  "Cleaner": 50000, "others": 15000, 
  "Total Teachers Tips": 80000
 },
"second term":
  {
	"First Aid": 75000, 
	"School Maintanance": 800000, 
	"Cleaner": 500000, "others": 15000, 
	"Total Teachers Tips": 35000
   },
"third term":
   {
	 "First Aid": 105000, 
	 "School Maintanance": 200000, 
	 "Cleaner": 50000, "others": 15000, 
	 "Total Teachers Tips": 35000
	}
}


CURRENT_YEAR = ['2023/2024']
BUDGET = {
	"first term": 15000000,
	"second term":15000000,
	"third term": 15000000
	}

terms = ['first term', 'second term', 'third term']
result_types = ['exam', 'assignment', 'quiz', 'test']


def generate_fake_school_info(CURRENT_YEAR, terms, 
							  class_, results_type, EXPENSES, BUDGET):
	school_name = "School of Coding"
	school_address = "123 Fake Street"
	school_email = "plsgq@example.com"
	school_phone = "123-456-7890"
	current_year = CURRENT_YEAR
	grades = {'A+': 90, 'A': 80, 'B': 70, 'C': 60, 'D': 50, 'F': 40}

	school_classes = {}
	school_terms = {current_year: terms}
	school_result_type = {"result_types": results_type}

	school_total_revenues = {}
	school_total_expenses = {current_year: EXPENSES}
	school_total_budget = {current_year: BUDGET}
	school_grades = {current_year: grades}
	
	result = School_information(
		          school_classes = {"classes" : ["KG1", "PRIMARY5"]},
                  school_name=school_name,
		          school_address=school_address,
		          school_email=school_email,
		          school_phone=school_phone,
		          school_terms=school_terms,
				  school_founded_year  = "2008",
				  school_total_revenues =school_total_revenues,
				  school_total_expenses=school_total_expenses,
		          school_total_budget=school_total_budget,
				  school_grades=school_grades,
				  school_result_type =	school_result_type,
				  school_location = "123 Elm Street, Springfield",
				  nationality = "Nigeria",
				  zipcode = "110113"
	             )
	return result


def generate_date_of_birth():
	import datetime
	
	age = random.randint(5, 20)
	current_year = datetime.datetime.now().year
	birth_year = current_year - age
	
	birth_month = random.choice([4, 6, 9, 11, 2])
	if birth_month in [4, 6, 9, 11]:
		max_day = 30
	elif birth_month == 2:
		if birth_year % 4 == 0 and (birth_year % 100 != 0 or birth_year % 400 == 0):
			max_day = 29  
		else:
			max_day = 28  
	birth_day = random.randint(1, max_day)

	date_of_birth = datetime.datetime(birth_year, birth_month, birth_day)
	return date_of_birth


def generate_student_other_expenses(class_):
	expenses = {"lesson_fee": {}, "class_books": {}}
	class_books = class_.class_books
	class_lesson_fee = class_.class_lesson_fee
	
	books = class_books.get("books")[:3]
	amounts = class_books.get("amounts")[:3]
	
	for name, amount in zip(books, amounts):
		expenses["class_books"].setdefault(name, amount)
	
	terms = ["first term", "second term", "third term"]
	for term in terms:
		current_date = datetime.now()
		first_month = current_date - timedelta(days=30)
		second_month = current_date - timedelta(days=60)
		third_month = current_date - timedelta(days=90)
		expenses["lesson_fee"].setdefault(term, 
										  {
											  first_month.strftime('%B'): class_lesson_fee,
											  second_month.strftime('%B'): class_lesson_fee,
											  third_month.strftime('%B'): class_lesson_fee
										  })
	
	return expenses

			
def generate_random_subjects(n):
	subjects = [
	    "Mathematics", "English Language", "Science", "Social Studies",
	    "History", "Geography", "Computer Science", "Physical Education",
	    "Art", "Music", "Biology", "Chemistry", "Physics", "Literature",
	    "Foreign Language"
	]
	return sample(subjects, n)


def generate_yearly_salary_json(year, salary):
	data = {
		'first term': {'January': 0, 'February':0, 'March':0},
		'second term': {'April':0, 'May':0, 'June': 0},
		'third term': {'July': 0, 'August': 0, 'September': 0}
	}
	for term in data.keys():
		for month in data[term].keys():
			data[term][month] = salary
			
	return {year: data}


def generate_student_textbooks(n):
	textbooks = [
	    "Mathematics for Beginners", "Science Explorers", "History Chronicles",
	    "English Grammar Guide", "Art Appreciation 101",
	    "Geography Adventures", "Computer Science Basics",
	    "Literature Masterpieces", "Music Theory Fundamentals",
	    "Economics Essentials", "Physics Fundamentals", "Chemistry Essentials",
	    "Biology Basics", "Psychology Insights", "Sociology Essentials"
	]
	return sample(textbooks, n)


def generate_class_timetable():
	days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
	timetable = {}
	for day in days_of_week:
		timetable[day] = generate_random_subjects(7)
	return timetable


def generate_class_time_slots():
	time_slots = []
	current_time = "08:00"
	for _ in range(7):
		time_slots.append(current_time)
		current_time = (datetime.strptime(current_time, '%H:%M') +
		                timedelta(hours=1)).strftime('%H:%M')
	return time_slots


annoucement = [{
    "title": "School Holiday",
    "content":
    "Please be reminded that there will be no classes on Friday, March 15th, due to a scheduled school holiday. Enjoy your long weekend!",
    "date": "2024-03-15"
}, {
    "title": "Volunteer Opportunity",
    "content":
    "We're looking for parent volunteers to help with the upcoming school fair on April 5th. If you're interested, please contact the school office by March 20th.",
    "date": "2024-03-07"
}, {
    "title": "Uniform Reminder",
    "content":
    "A friendly reminder to all students: please ensure you are wearing the correct school uniform as outlined in the student handbook. Thank you for your cooperation.",
    "date": "2024-03-03"
}, {
    "title": "Library Book Return",
    "content":
    "All library books borrowed during the previous semester must be returned by Friday, March 8th. Overdue books will incur fines.",
    "date": "2024-03-05"
}]


def write_announcements_to_db(json_data):
	announcements = []
	for announcement in json_data:
		title = announcement['title']
		content = announcement['content']
		date = datetime.strptime(announcement['date'], '%Y-%m-%d').date()
		new_announcement = Announcements(title=title,
		                                content=content,
		                                created_at=date)
		announcements.append(new_announcement)
	return announcements


events = [{
    "name": "Parent-Teacher Meeting",
    "description":
    "A meeting between parents and teachers to discuss students' progress and address any concerns.",
    "date": "2024-04-15 18:00:00"
	}, {
    "name": "School Open House",
    "description":
    "An event where prospective students and their families can visit the school, meet teachers, and learn about programs and facilities.",
    "date": "2024-05-03 10:00:00"
	}, {
    "name": "Science Fair",
    "description":
    "A showcase of student projects and experiments related to various scientific topics.",
    "date": "2024-06-08 09:00:00"
	}, {
    "name": "Field Day",
    "description":
    "A day of outdoor activities and sports competitions for students, often held at the end of the school year.",
    "date": "2024-07-20 08:30:00"
	}, {
    "name": "Graduation Ceremony",
    "description":
    "A formal event to celebrate and recognize students who are completing their studies and moving on to the next phase of their lives.",
    "date": "2024-08-15 15:00:00"
	}]


def add_events_to_database(events_lst):
	events = []
	for event_data in events_lst:
		name = event_data['name']
		description = event_data['description']
		date = datetime.strptime(event_data['date'], '%Y-%m-%d %H:%M:%S')

		# Create a new Event object
		new_event = Events(name=name, description=description, date=date)

		# Add the event to the database session
		events.append(new_event)
	return events


def generate_class_time_table():
	timetable = generate_class_timetable()
	time_slots = generate_class_time_slots()
	class_time_table = {"Times": time_slots}
	class_time_table.update(timetable)
	return class_time_table


# Generate fake admin data
def generate_fake_admins(n):
	school_info = School_information.query.first()
	adm = []
	for _ in range(n):
		admin = Admin(username=fake.user_name(),
		              firstname=fake.first_name(),
		              lastname=fake.last_name(),
		              email=fake.email(),
		              phonenumber=fake.phone_number(),
		              access=fake.boolean(),
		              key=hashed_password)
		adm.append(admin)
		
		
		school_info.school_total_admin += 1
		with app.app_context():
			db.session.commit()
	return adm


# Generate fake teacher data
def generate_fake_teachers(n, role="teacher"):
    school_info = School_information.query.first()
    teachers = []
    for _ in range(n):
        current_salary = random.randint(20000, 40000)
        teacher = Teachers(
		    username=fake.user_name(),
		    firstname=fake.first_name(),
		    lastname=fake.last_name(),
		    dob=fake.date_of_birth(),
		    address=fake.address(),
		    email=fake.email(),
		    phonenumber=fake.phone_number(),
		    gender=fake.random_element(elements=('male', 'female')),
		    qualification=fake.random_element(elements=('Bachelor\'s Degree',
		                                                'Master\'s Degree',
		                                                'PhD')),
		    years_of_experience=fake.random_number(digits=2),
		    certifications=fake.sentence(),
		    teaching_specializations=fake.word(),
		    languages_spoken=fake.word(),
		    emergency_contact=fake.phone_number(),
		    notes=fake.text(),
		    hire_date=fake.date_this_decade(),
		    current_salary=current_salary,
		    role=role,
		    key=hashed_password,
		    access=fake.boolean(),
		    salarys=generate_yearly_salary_json(2023, current_salary),
		    subject_taught=generate_random_subjects(3),
		    bio=fake.text(),
		    marital_status=fake.random_element(elements=('single', 'married')))
        teachers.append(teacher)
		
        
        school_info.school_total_teachers += 1
        with app.app_context():
            db.session.commit()
    return teachers


def generate_fake_classes(teachers, class_names):
    classes = []
    for class_ in class_names:
        class_name = class_
        class_fee = random.randint(30000, 50000)
        class_subjects = {'subjects': generate_random_subjects(10)}
        class_books = {
		    'books': generate_student_textbooks(5),
		    'authors': [fake.name() for i in range(2)],
		    'amounts': [random.randint(2000, 4000) for i in range(5)]
		}
        class_description = fake.text()
        class_time_table = generate_class_time_table()
        class_materials = fake.url()
        teacher_username = choice(teachers).username

        class_instance = Classes(class_name=class_name,
		                       class_fee=class_fee,
		                       class_subjects=class_subjects,
							   class_lesson_fee = random.randint(1000, 3000),
		                       class_books=class_books,
		                       class_description=class_description,
		                       class_time_table=class_time_table,
		                       materials=class_materials,
		                       teacher_username=teacher_username)
        classes.append(class_instance)
    return classes


def generate_fake_students(n, classes):
    school_info = School_information.query.first()
    students = []
    for _ in range(n):
        class_ = choice(classes)
        gender = choice(["male", "female"])
        student = Students(
			username=fake.user_name(),
			firstname=fake.first_name(),
			lastname=fake.last_name(),
			dob=generate_date_of_birth(),
			address=fake.address(),
			email=fake.email(),
			homephone=fake.phone_number(),
			enroll_date=fake.date_this_decade(),
			gender=gender,
			placeofbirth=fake.city(),
			nationality=fake.country(),
			previous_school=fake.company(),
			medical_information=fake.sentence(),
			parental_consent=fake.boolean(),
			languages_spoken=fake.word(),
			image_link=fake.image_url(),
			
			mother_firstname=fake.first_name(),
			mother_lastname=fake.last_name(),
			mother_address=fake.address(),
			mother_placeofemployment=fake.company(),
			mother_occupation=fake.job(),
			mother_town=fake.city(),
			mother_state=fake.state(),
			mother_cellphonenumber=fake.phone_number(),
			mother_homephonenumber=fake.phone_number(),
			
			father_firstname=fake.first_name(),
			father_lastname=fake.last_name(),
			father_address=fake.address(),
			father_placeofemployment=fake.company(),
			father_occupation=fake.job(),
			father_town=fake.city(),
			father_state=fake.state(),
			father_cellphonenumber=fake.phone_number(),
			father_homephonenumber=fake.phone_number(),
			
			left_date=None,
			key=hashed_password,
			class_id=class_.id,
			others_expenses=generate_student_other_expenses(class_),
			access=True,
			years = {"years": [2022, 2023, 2024]}
		)

        students.append(student)
        temp = class_.class_number_of_students
		
        if temp is None:
            temp = {"total": 0}
			
        if temp.get(gender):
            temp[gender] +=1
            temp["total"] +=1
        else:
            temp[gender] =1
            temp["total"] +=1
			

        class_.class_numberOfStudent = temp
        school_info.school_total_students += 1
        print(class_.class_numberOfStudent, gender, class_.id)
		
        with app.app_context():
            db.session.commit()

    return students


def generate_fake_results(students, terms, result_types, year):
	results = []
	for student in students:
		for term in terms:
			for result_type in result_types:
				subjects = student.class_.class_subjects['subjects']
				for subject in subjects:
					date = fake.date_between(start_date='-1y', end_date='now')
					result = Results(result_type=result_type,
					                 year=year,
					                 term=term,
					                 subject=subject,
					                 marks_obtain=100,
					                 total_mark=random.randint(45, 100),
					                 submission_date=date,
					                 comment=fake.text(),
					                 student_username=student.username,
					                 class_id=student.class_id)
					results.append(result)
	return results


def divide_number_into_four_parts(number, deducted_value=0):
	number -= deducted_value
	quotient = number // 4
	result = [quotient, quotient, quotient, quotient]
	return result


def generate_fake_student_fees(students, years, terms):
    student_fees = []
    temp = {}
    school_info = School_information.query.first()
    for student in students:
        for year in years:
            for term in terms:
                n = random.choice([0, 1200, 500, 300, 200])
                amount = divide_number_into_four_parts(student.class_.class_fee, n)
				
                for fee_amount in amount:
                    payment_date = fake.date_time_between_dates(
					    datetime.strptime(f"{year.split('/')[0]}-01-01", "%Y-%m-%d"),
					    datetime.strptime(f"{year.split('/')[0]}-12-31", "%Y-%m-%d"))
                    payment_method = fake.random_element(
					    elements=('cash', 'credit card', 'bank transfer'))
                    payment_status = fake.random_element(
					    elements=('pendint', 'successfull'))
                    payment_note = fake.text()

                    student_fee = Student_fee(transaction_id=str(uuid.uuid4()),
					                         year=year,
					                         term=term,
					                         fee_amount=fee_amount,
					                         payment_date=payment_date,
					                         payment_method=payment_method,
					                         payment_status=payment_status,
					                         payment_note=payment_note,
					                         student_username=student.username,
					                         class_id=student.class_id)
                    student_fees.append(student_fee)

                    if term not in temp:
                        temp[term] = fee_amount
                    else:
                        temp[term] += fee_amount
					
    return student_fees, temp


def generate_fake_attendance(model, persons, terms, role='student'):
	temp = {}
	attendance_list = []
	for person in persons:
		for term, date in terms.items():
			# Define start and end dates
			start_date = date[0]
			end_date = date[1]

			# Generate date range
			date_range = [
			    start_date + timedelta(days=x)
			    for x in range((end_date - start_date).days + 1)
			]

			for date in date_range:

				morning_attendance = date
				evening_attendance = morning_attendance + timedelta(hours=7)

				comment = fake.text()
				status = fake.random_element(elements=('present', 'absent',
				                                       'present', 'present',
				                                       'late'))
				late_arrival = fake.boolean(
				    chance_of_getting_true=30) if status == 'Late' else None

				if morning_attendance:
					if role == 'teacher' or role == "head teacher":
						attendance_entry = model(
						    term=term,
						    morning_attendance=morning_attendance,
						    evening_attendance=evening_attendance,
						    comment=comment,
						    status=status,
						    late_arrival=late_arrival,
						    teacher_username=person.username)

						if term not in temp:
							temp[term] = 1
						else:
							temp[term] +=1
						
					else:
						attendance_entry = model(
						    term=term,
						    morning_attendance=morning_attendance,
						    evening_attendance=evening_attendance,
						    comment=comment,
						    status=status,
						    late_arrival=late_arrival,
						    student_username=person.username,
						    class_id=person.class_id)
						
						class_name = person.class_.class_name
						if "class" not in temp:
							temp = {"class": {class_name: {"attendance_count": 1}}}
						elif class_name not in temp["class"]:
							temp["class"][class_name] = {"attendance_count": 1}
						else :
							temp["class"][class_name]["attendance_count"] +=1
							

					attendance_list.append(attendance_entry)
	return attendance_list, temp


with app.app_context():
	school_info = generate_fake_school_info(CURRENT_YEAR[0], 
											terms, class_, 
											result_types, 
											EXPENSES, BUDGET)


	db.session.add(school_info)
	db.session.commit()

	
	admins = generate_fake_admins(2)
	db.session.add_all(admins)
	db.session.commit()
	
	
	teachers = generate_fake_teachers(10)
	db.session.add_all(teachers)
	db.session.commit()
	
	
	teachers = generate_fake_teachers(2, "head teacher")
	db.session.add_all(teachers)
	db.session.commit()
	
	
	teachers = Teachers.query.all()
	class_names = [
	'KG1', "KG2", 'PRIMARY1', 'PRIMARY2', 'PRIMARY3', 'PRIMARY4',
	'PRIMARY5', 'PRIMARY6'
	]
	classes = generate_fake_classes(teachers, class_names)
	db.session.add_all(classes)
	db.session.commit()
	
	
	classes = Classes.query.all()

	for _ in range(10):
		students = generate_fake_students(10, classes)
		db.session.add_all(students)
		db.session.commit()
	
	
	students = Students.query.all()
	
	years = ["2023/2024"]
	results = generate_fake_results(students, terms, result_types, CURRENT_YEAR[0])
	db.session.add_all(results)
	db.session.commit()
	
	
	students_fee, amount = generate_fake_student_fees(students, CURRENT_YEAR, terms)
	school_info.school_total_revenues = {CURRENT_YEAR[0]: amount}
	db.session.add_all(students_fee)
	db.session.commit()
	
	
	term = {
	'first term': [datetime(2023, 1, 1),
			   datetime(2023, 3, 31)],
	'second term': [datetime(2023, 4, 1),
				datetime(2023, 7, 31)],
	'third term': [datetime(2023, 8, 1),
			   datetime(2023, 11, 30)],
	}
	students_attendance, attendance = generate_fake_attendance(Student_attendance, students,
										   term)
	school_info.school_classes["classes_attendance"] = attendance.get("class")
	db.session.add_all(students_attendance)
	db.session.commit()
	
	
	teachrs_attendance, attendance = generate_fake_attendance(Teacher_attendance, teachers,
										  term, 'teacher')
	school_info.school_teachers = attendance
	db.session.add_all(teachrs_attendance)
	db.session.commit()
	
	
	evens_data = add_events_to_database(events)
	db.session.add_all(evens_data)
	db.session.commit()
	
	
	annoucements = write_announcements_to_db(annoucement)
	db.session.add_all(annoucements)
	db.session.commit()

	
	students = Students.query.all()
	term = {
	'first term': [datetime(2024, 1, 1),
			   datetime(2024, 3, 31)],
	'second term': [datetime(2024, 4, 1),
				datetime(2024, 7, 31)],
	'third term': [datetime(2024, 8, 1),
			   datetime(2024, 11, 30)],
	}
	
	print("Current school temp Databse created Successfully .......")

	











