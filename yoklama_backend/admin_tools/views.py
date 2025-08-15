from django import forms
from .uni_list import University_list, Pres_list
from lecturer_data.models import University
from .scrape_static_unis import uniadd
from .scrape_static_pres import uniaddpres
from django.shortcuts import render

class UniversitySelectForm(forms.Form):
    university = forms.ChoiceField(
        choices=[('all', 'All')] + [(key, key) for key in University_list.keys()]
    )

class PresSelectForm(forms.Form):
    pre = forms.ChoiceField(
        choices=[('all', 'All')] + [(key, key) for key in Pres_list.keys()]
    )

def run_script(request):
    if request.method == "POST":
        form = UniversitySelectForm(request.POST)
        if form.is_valid():
            university_name = form.cleaned_data['university']

        added_data=[]
        if university_name == 'all':
            selected_universities = University_list.keys()
        else: 
            selected_universities = [university_name]

        for uni_data in selected_universities:
            if not University.objects.filter(name = uni_data).exists():
                uniadd(University_list[university_name])
                added_data.append(f"Added {university_name} to the database.")
            else:
                added_data.append(f"{university_name} already exists in the database.")

        return render(request, 'admin/custom_script_page.html', {
                'form': form,
                'added_data': added_data
            })

    else:
        form = UniversitySelectForm()

    return render(request, 'admin/custom_script_page.html', {
        'form': form,
        'added_data': None
    })

def run_script_for_pres(request):
    if request.method == "POST":
        form = PresSelectForm(request.POST)
        if form.is_valid():
            pres_name = form.cleaned_data['pre']

        added_data=[]
        if pres_name == 'all':
            selected_pres = Pres_list.keys()
        else: 
            selected_pres = [pres_name]

        for pres_data in selected_pres:
            if University.objects.filter(name = pres_data).exists():
                uniaddpres(Pres_list[pres_name])
                added_data.append(f"Added {pres_name} pre-licence to the database.")
            else:
                added_data.append(f"please first add {pres_name} from university adder")

        return render(request, 'admin/custom_script_page.html', {
                'form': form,
                'added_data': added_data
            })

    else:
        form = PresSelectForm()

    return render(request, 'admin/custom_script_page.html', {
        'form': form,
        'added_data': None
    })