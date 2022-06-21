from django.shortcuts import redirect, render
from django import forms
from . import random2
from django.http import HttpResponseNotFound 

from . import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    if util.get_entry(name) is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": name,
            "entry": markdown2.markdown(util.get_entry(name))
        })
    else:
        return notfound(request)

def search(request):
    q = request.GET.get('q')
    if util.get_entry(q) is not None:
        return entry(request, q)
    else:
        return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/newpage.html", {"message": "Title already exists. Use another title or make necessary edits.", 
                "form":form,
                "form.title": title, "form.content": content})
            else:
                util.save_entry(title, content)
                return entry(request,title)
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewEntryForm()
        })

# This is to deliver an error message
# As stated by requirements
def notfound(request):
    return HttpResponseNotFound() 

def edit(request, name):
    content = util.get_entry(name)
    if content is not None:
        if request.method == "POST":
            content = request.POST.get("content")
            util.save_entry(name, content.replace("\n",""))
            return redirect("entry", name=name)
        else:
            return render(request, "encyclopedia/edit.html", {'content': content, 'title': name})
    else:
        return notfound(request)

def randompage(request):
    entries = util.list_entries()
    name = random2.choice(entries)
    return redirect("entry", name=name)

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(label="Content (in Markdown)",widget=forms.Textarea(attrs={'class':'form-control','rows':10}))

class ExistingEntryForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(label="Content (in Markdown)",widget=forms.Textarea(attrs={'class':'form-control','rows':10}))