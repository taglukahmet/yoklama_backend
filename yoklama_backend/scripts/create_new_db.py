import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoklama_backend.settings')
django.setup()

from lecturer_data.models import *
#uni - fac and departments
uni = University.objects.get(name="Ortadoğu Teknik Üniverstesi")
fac = Faculty.objects.get(name = "Mühendislik Fakültesi")
ceng = Department.objects.get(name = "Bilgisayar Mühendisliği")
eee = Department.objects.get(name = "Elektrik-Elektronik Mühendisliği")
me = Department.objects.get(name = "Makine Mühendisliği")
mete = Department.objects.get(name = "Malzeme ve Metalurji Mühendisliği")
enve = Department.objects.get(name = "Çevre Mühendisliği")
ie = Department.objects.get(name = "Endüstri Mühendisliği")
fde = Department.objects.get(name = "Gıda Mühendisliği")
aee = Department.objects.get(name = "Havacılık ve Uzay Mühendisliği")
geoe = Department.objects.get(name = "Jeoloji Mühendisliği")
cheme = Department.objects.get(name = "Kimya Mühendisliği")
mine = Department.objects.get(name = "Maden Mühendisliği")
pete = Department.objects.get(name = "Petrol ve Doğalgaz Mühendisliği")


#buildings
cenga = Building.objects.create(name="A Blok", department = ceng, faculty = fac, university= uni)
cengb = Building.objects.create(name="B Blok", department = ceng, faculty = fac, university= uni)

eeea = Building.objects.create(name="A Blok", department = eee, faculty = fac, university= uni)
eeed = Building.objects.create(name="D Blok", department = eee, faculty = fac, university= uni)

meb = Building.objects.create(name="B Blok", department = me, faculty = fac, university= uni)
med = Building.objects.create(name="D Blok", department = me, faculty = fac, university= uni)
meg = Building.objects.create(name="G Blok", department = me, faculty = fac, university= uni)

meteb = Building.objects.create(name="B Blok", department = mete, faculty = fac, university= uni)
metec = Building.objects.create(name="C Blok", department = mete, faculty = fac, university= uni)
metee = Building.objects.create(name="E Blok", department = mete, faculty = fac, university= uni)

enveb = Building.objects.create(name="Binası", department = enve, faculty = fac, university= uni)
ieb = Building.objects.create(name="Binası", department = ie, faculty = fac, university= uni)
fdeb = Building.objects.create(name="Binası", department = fde, faculty = fac, university= uni)
aeeb = Building.objects.create(name="Binası", department = aee, faculty = fac, university= uni)
geoeb = Building.objects.create(name="Binası", department = geoe, faculty = fac, university= uni)
chemeb = Building.objects.create(name="Binası", department = cheme, faculty = fac, university= uni)
mineb = Building.objects.create(name="Binası", department = mine, faculty = fac, university= uni)
peteb = Building.objects.create(name="Binası", department = pete, faculty = fac, university= uni)

yp = Building.objects.create(name="Yüksel Proje Amfisi", university= uni)
mm = Building.objects.create(name="Merkez Mühendislik Binası", university= uni)

#classrooms
cenga1 = Classroom.objects.create(name="BMB1", building = cenga)
cenga2 = Classroom.objects.create(name="BMB2", building = cenga)
cenga3 = Classroom.objects.create(name="BMB3", building = cenga)

cengb1 = Classroom.objects.create(name="BMB4", building = cengb)
cengb2 = Classroom.objects.create(name="BMB5", building = cengb)
cengb3 = Classroom.objects.create(name="BMB A101", building = cengb)

eeea1= Classroom.objects.create(name="EA202", building = eeea)
eeea2= Classroom.objects.create(name="EA206", building = eeea)
eeea3= Classroom.objects.create(name="EA207", building = eeea)
eeea4= Classroom.objects.create(name="EA208", building = eeea)
eeea5= Classroom.objects.create(name="EA209", building = eeea)
eeea6= Classroom.objects.create(name="EA211", building = eeea)
eeea7= Classroom.objects.create(name="EA306", building = eeea)
eeea8= Classroom.objects.create(name="EA307", building = eeea)
eeea9= Classroom.objects.create(name="EA310", building = eeea)
eeea10= Classroom.objects.create(name="EA312", building = eeea)

eeed1= Classroom.objects.create(name="D131", building = eeed)
eeed2= Classroom.objects.create(name="D134", building = eeed)
eeed3= Classroom.objects.create(name="D135", building = eeed)

yp1= Classroom.objects.create(name="YP-A1", building=yp)
yp2= Classroom.objects.create(name="YP-A2", building=yp)
yp3= Classroom.objects.create(name="YP-A3", building=yp)
yp4= Classroom.objects.create(name="YP-A4", building=yp)
yp5= Classroom.objects.create(name="YP-B201", building=yp)
yp6= Classroom.objects.create(name="YP-B202", building=yp)
yp7= Classroom.objects.create(name="YP-D001", building=yp)
yp8= Classroom.objects.create(name="YP-D002", building=yp)
yp9= Classroom.objects.create(name="YP-D003", building=yp)
yp10= Classroom.objects.create(name="YP-D101", building=yp)
yp11= Classroom.objects.create(name="YP-D102", building=yp)
yp12= Classroom.objects.create(name="YP-D103", building=yp)
yp13= Classroom.objects.create(name="YP-D104", building=yp)
yp14= Classroom.objects.create(name="YP-D105", building=yp)
yp15= Classroom.objects.create(name="YP-D106", building=yp)
yp16= Classroom.objects.create(name="YP-D107", building=yp)
yp17= Classroom.objects.create(name="YP-D201", building=yp)
yp18= Classroom.objects.create(name="YP-D202", building=yp)
yp19= Classroom.objects.create(name="YP-D203", building=yp)
yp20= Classroom.objects.create(name="YP-D204", building=yp)
yp21= Classroom.objects.create(name="YP-D205", building=yp)

mm1= Classroom.objects.create(name="MM14", building=mm)
mm2= Classroom.objects.create(name="MM125", building=mm)
mm3= Classroom.objects.create(name="MM308", building=mm)
mm4= Classroom.objects.create(name="MM309", building=mm)
mm5= Classroom.objects.create(name="MM315", building=mm)
mm6= Classroom.objects.create(name="MM316", building=mm)
mm7= Classroom.objects.create(name="MM316A", building=mm)
mm8= Classroom.objects.create(name="MM321", building=mm)
mm9= Classroom.objects.create(name="MM412", building=mm)
mm10= Classroom.objects.create(name="MM451", building=mm)

#lectures
ceng100 = Lecture.objects.create(name="CENG", code="100", department=ceng, explicit_name="Computer Engineering Orientation")
ceng111 = Lecture.objects.create(name="CENG", code="111", department=ceng, explicit_name="Introduction to Computer Engineering Consepts")
ceng140 = Lecture.objects.create(name="CENG", code="140", department=ceng, explicit_name="C Programming")
ceng200 = Lecture.objects.create(name="CENG", code="200", department=ceng, explicit_name="Introduction to computers & Fortran Programming")
ceng210 = Lecture.objects.create(name="CENG", code="210", department=ceng, explicit_name="Introduction to computers & Advanced Fortran Programming")
ceng213 = Lecture.objects.create(name="CENG", code="213", department=ceng, explicit_name="Data Structures")
ceng222 = Lecture.objects.create(name="CENG", code="222", department=ceng, explicit_name="Statistical Methods for Computer Engineering")
ceng223 = Lecture.objects.create(name="CENG", code="223", department=ceng, explicit_name="Discrete Computational Structures")
ceng229 = Lecture.objects.create(name="CENG", code="229", department=ceng, explicit_name="C Programming")
ceng230 = Lecture.objects.create(name="CENG", code="230", department=ceng, explicit_name="Introduction to Cprogramming")
ceng232 = Lecture.objects.create(name="CENG", code="232", department=ceng, explicit_name="Logic Design")
ceng240 = Lecture.objects.create(name="CENG", code="240", department=ceng, explicit_name="Programming with Python for Engineers")
ceng242 = Lecture.objects.create(name="CENG", code="242", department=ceng, explicit_name="Programming Language Concepts")
ceng280 = Lecture.objects.create(name="CENG", code="280", department=ceng, explicit_name="Formal Languages and Abstract Machines")
ceng300 = Lecture.objects.create(name="CENG", code="300", department=ceng, explicit_name="Summer Practice I")
ceng301 = Lecture.objects.create(name="CENG", code="301", department=ceng, explicit_name="Algorithms and Data Structures")

#lecturers
mail1="ucoluk@ceng.metu.edu.tr"
pass1="ucoluk.1234"
user1 = User.objects.create_user(username=mail1, email=mail1, password=pass1)
lec1 = Lecturer.objects.create(user=user1, title="Prof. Dr.", first_name="Göktürk", last_name="Üçoluk", department=ceng)

mail2="altingovde@ceng.metu.edu.tr"
pass2="altingovde.1234"
user2 = User.objects.create_user(username=mail2, email=mail2, password=pass2)
lec2 = Lecturer.objects.create(user=user2, title="Prof. Dr.", first_name="İsmail Şengör", last_name="Altıngövde", department=ceng)

mail3="onur@ceng.metu.edu.tr"
pass3="onur.1234"
user3 = User.objects.create_user(username=mail3, email=mail3, password=pass3)
lec3 = Lecturer.objects.create(user=user3, title="Dr.", first_name="Onur Tolga", last_name="Şehitoğlu", department=ceng)

mail4="toroslu@ceng.metu.edu.tr"
pass4="toroslu.1234"
user4 = User.objects.create_user(username=mail4, email=mail4, password=pass4)
lec4 = Lecturer.objects.create(user=user4, title="Prof. Dr.", first_name="İsmail Hakkı", last_name="Toroslu", department=ceng)

mail5="mangu@ceng.metu.edu.tr"
pass5="mangu.1234"
user5 = User.objects.create_user(username=mail5, email=mail5, password=pass5)
lec5 = Lecturer.objects.create(user=user5, title="Prof. Dr.", first_name="Murathan", last_name="Manguoğlu", department=ceng)

mail6="ertekin@ceng.metu.edu.tr"
pass6="ertekin.1234"
user6 = User.objects.create_user(username=mail6, email=mail6, password=pass6)
lec6 = Lecturer.objects.create(user=user6, title="Assoc. Prof. Dr.", first_name="Şeyda", last_name="Ertekin", department=ceng)

mail7="karagoz@ceng.metu.edu.tr"
pass7="karagoz.1234"
user7 = User.objects.create_user(username=mail7, email=mail7, password=pass7)
lec7 = Lecturer.objects.create(user=user7, title="Prof. Dr.", first_name="Pınar", last_name="Karagöz", department=ceng)



#sections
ceng140_1 = Section.objects.create(section_number="1", lecture=ceng140, lecturer=lec2)
ceng140_2 = Section.objects.create(section_number="2", lecture=ceng140, lecturer=lec2)
ceng140_3 = Section.objects.create(section_number="3", lecture=ceng140, lecturer=lec1)

ceng242_1 = Section.objects.create(section_number="1", lecture=ceng242, lecturer=lec3)
ceng242_2 = Section.objects.create(section_number="2", lecture=ceng242, lecturer=lec4)

ceng232_1 = Section.objects.create(section_number="1", lecture=ceng232, lecturer=lec5)
ceng232_2 = Section.objects.create(section_number="2", lecture=ceng232, lecturer=lec5)

ceng222_1 = Section.objects.create(section_number="1", lecture=ceng222, lecturer=lec6)
ceng222_2 = Section.objects.create(section_number="2", lecture=ceng222, lecturer=lec7)

ceng213_1 = Section.objects.create(section_number="1", lecture=ceng213, lecturer=lec3)
ceng213_2 = Section.objects.create(section_number="2", lecture=ceng213, lecturer=lec6)
ceng213_3 = Section.objects.create(section_number="3", lecture=ceng213, lecturer=lec5)

#hours
ceng_140_3_1 = Hours.objects.create(day = "Monday", order="1", time_start="09:40", time_end="10:30", section= ceng140_3, classroom=cengb1)
ceng_140_3_2 = Hours.objects.create(day = "Wednesday", order="2", time_start="10:40", time_end="11:30", section= ceng140_3, classroom=cengb1)
ceng_140_3_3 = Hours.objects.create(day = "Wednesday", order="3", time_start="11:40", time_end="12:30", section= ceng140_3, classroom=cengb1)

ceng_140_1_1 = Hours.objects.create(day = "Monday", order="1", time_start="12:40", time_end="13:30", section= ceng140_1, classroom=cenga3)
ceng_140_1_2 = Hours.objects.create(day = "Tuesday", order="2", time_start="13:40", time_end="14:30", section= ceng140_1, classroom=cenga3)
ceng_140_1_3 = Hours.objects.create(day = "Tuesday", order="3", time_start="14:40", time_end="15:30", section= ceng140_1, classroom=cenga3)

ceng_140_2_1 = Hours.objects.create(day = "Monday", order="1", time_start="13:40", time_end="14:30", section= ceng140_2, classroom=cenga3)
ceng_140_2_2 = Hours.objects.create(day = "Friday", order="2", time_start="13:40", time_end="14:30", section= ceng140_2, classroom=cenga3)
ceng_140_2_3 = Hours.objects.create(day = "Friday", order="3", time_start="14:40", time_end="15:30", section= ceng140_2, classroom=cenga3)

ceng_242_1_1 = Hours.objects.create(day = "Tuesday", order="1", time_start="09:40", time_end="10:30", section= ceng242_1, classroom=cenga1)
ceng_242_1_2 = Hours.objects.create(day = "Wednesday", order="2", time_start="10:40", time_end="11:30", section= ceng242_1, classroom=cenga1)
ceng_242_1_3 = Hours.objects.create(day = "Wednesday", order="3", time_start="11:40", time_end="12:30", section= ceng242_1, classroom=cenga1)

ceng_242_2_1 = Hours.objects.create(day = "Monday", order="1", time_start="08:40", time_end="09:30", section= ceng242_2, classroom=cenga3)
ceng_242_2_2 = Hours.objects.create(day = "Monday", order="2", time_start="09:40", time_end="10:30", section= ceng242_2, classroom=cenga3)
ceng_242_2_3 = Hours.objects.create(day = "Thursday", order="3", time_start="09:40", time_end="10:30", section= ceng242_2, classroom=cenga3)

ceng_232_1_1 = Hours.objects.create(day = "Monday", order="1", time_start="10:40", time_end="11:30", section= ceng232_1, classroom=cenga1)
ceng_232_1_2 = Hours.objects.create(day = "Monday", order="2", time_start="11:40", time_end="12:30", section= ceng232_1, classroom=cenga1)
ceng_232_1_3 = Hours.objects.create(day = "Wednesday", order="3", time_start="12:40", time_end="13:30", section= ceng232_1, classroom=cenga1)

ceng_232_2_1 = Hours.objects.create(day = "Monday", order="1", time_start="13:40", time_end="14:30", section= ceng232_2, classroom=cenga2)
ceng_232_2_2 = Hours.objects.create(day = "Monday", order="2", time_start="14:40", time_end="15:30", section= ceng232_2, classroom=cenga2)
ceng_232_2_3 = Hours.objects.create(day = "Wednesday", order="3", time_start="16:40", time_end="17:30", section= ceng232_2, classroom=cenga2)

ceng_222_1_1 = Hours.objects.create(day = "Monday", order="1", time_start="15:40", time_end="16:30", section= ceng222_1, classroom=cenga1)
ceng_222_1_2 = Hours.objects.create(day = "Monday", order="2", time_start="16:40", time_end="17:30", section= ceng222_1, classroom=cenga1)
ceng_222_1_3 = Hours.objects.create(day = "Wednesday", order="3", time_start="16:40", time_end="17:30", section= ceng222_1, classroom=cenga1)

ceng_222_2_1 = Hours.objects.create(day = "Tuesday", order="1", time_start="10:40", time_end="11:30", section= ceng222_2, classroom=cenga2)
ceng_222_2_2 = Hours.objects.create(day = "Tuesday", order="2", time_start="11:40", time_end="12:30", section= ceng222_2, classroom=cenga2)
ceng_222_2_3 = Hours.objects.create(day = "Friday", order="3", time_start="09:40", time_end="10:30", section= ceng222_2, classroom=cenga2)

