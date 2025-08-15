import requests
from bs4 import BeautifulSoup
from lecturer_data.models import University, Faculty, Department
def uniaddpres(code):
    url = f"https://yokatlas.yok.gov.tr/onlisans-univ.php?u={code}"

    headers = {
        "User-Agent": "Chrome/138.0.7204.159"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    panels = soup.select('#bs-collapse .panel.panel-danger')
    panels2 = soup.select('#bs-collapse2 .panel.panel-danger')
    unipanel = soup.select_one('div.page-header h3')
    if unipanel:
        uni = unipanel.find(string = True, recursive=False).strip().title()

    if University.objects.filter(name= uni).exists():
        uni = University.objects.get(name= uni)
        print(f"{uni} found")
        depts = []
        facs = []

        for panel in panels:
            faculty_el = panel.select_one("div.panel-heading h4.panel-title a small font")
            if faculty_el:
                faculty_name = faculty_el.text[1:-1]
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
                faculty_name = faculty_el.text[1:-1]
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
    
    else: print("please add the university from license")
