import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoklama_backend.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from lecturer_data.models import University, Faculty, Department

url = "https://yokatlas.yok.gov.tr/lisans-univ.php?u=1084"

headers = {
    "User-Agent": "Chrome/138.0.7204.159"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

panels = soup.select('#bs-collapse .panel.panel-primary')
panels2 = soup.select('#bs-collapse2 .panel.panel-primary')
unipanel = soup.select_one('div.page-header h3')
if unipanel:
    uni = unipanel.find(string = True, recursive=False).strip().title()
uni = University.objects.create(name = f"{uni}")
print(f"{uni} created")
depts = []
facs = []

for panel in panels:
    faculty_el = panel.select_one("div.panel-heading h4.panel-title a small font")
    if faculty_el:
        faculty_name = faculty_el.text.strip("()")
        if faculty_name.find("KKTC") >=0:
            continue
    dept_el = panel.select_one("div.panel-heading h4.panel-title a div")
    if dept_el: 
        dept_name = dept_el.text 
        if dept_name.find("KKTC Uyruklu") >=0:
            continue
    if faculty_name and dept_name:
        depts.append({f"{faculty_name}":f"{dept_name}"})
for panel in panels2:
    faculty_el = panel.select_one("div.panel-heading h4.panel-title a small font")
    if faculty_el:
        faculty_name = faculty_el.text.strip("()")
        if faculty_name.find("KKTC") >=0:
            continue
    dept_el = panel.select_one("div.panel-heading h4.panel-title a div")
    if dept_el: 
        dept_name = dept_el.text
        if dept_name.find("KKTC Uyruklu") >=0:
            continue
    if faculty_name and dept_name:
        depts.append({f"{faculty_name}":f"{dept_name}"})

for dept in depts:
    for key in dept.keys():
        for value in dept.values():
            if "(İngilizce)" in value:
                val = value
                val = val.replace("(İngilizce)", "").strip()
                cnt = 0
                for dep in depts:
                    for valu in dep.values():
                        if val in valu and len(val) == len(valu) and "(İngilizce)" not in valu:
                            cnt = 1
                            break
                if cnt==0:
                    dept.update({key:val})



for dept in depts:
    for key in dept.keys():
        if key not in facs:
            facs.append(key)
            facult = Faculty.objects.create(name = f"{key}", university = uni)
            print(f"{facult} created on {uni}")
            

for dept in depts:
    for key in dept.keys():
        for value in dept.values():
            facultt = Faculty.objects.get(name = f"{key}", university = uni)
            depart = Department.objects.create(name = f"{value}", faculty = facultt)
            print(f"added {depart} | {facultt} to the {uni}")
