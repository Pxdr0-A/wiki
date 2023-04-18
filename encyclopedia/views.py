from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from markdown2 import Markdown

import random as rnd

from . import util

class SearchEntryFrom(forms.Form):
    posted_entry = forms.CharField(label = "Search Entry")

class CreateEntry(forms.Form):
    posted_title = forms.CharField(label = "Give a Title")
    posted_content = forms.CharField(
        label = "Write here the markdown content",
        widget = forms.Textarea(attrs={'size':'80'}))

def dynamic_class(populate):
    class EditEntry(forms.Form):
        posted_content = forms.CharField(
            label = "Write here the markdown content",
            widget = forms.Textarea(attrs={'size':'80'}),
            initial = populate)
    
    return EditEntry
    
markdowner = Markdown()

def index(request):
    # to build the form and pass on to the html
    if request.method == "POST":
        search_form = SearchEntryFrom(request.POST)
        if search_form.is_valid():
            entry = search_form.cleaned_data["posted_entry"]
            if entry in util.list_entries():
                entry_request = util.get_entry(entry)
                entry_md = markdowner.convert(str(entry_request))
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry_md,
                    "title": entry
                })
            else:
                is_this = []
                for e in util.list_entries():
                    if entry in e:
                        is_this.append(e)
                return render(request, "encyclopedia/did_you_mean.html", {
                    "is_this": is_this
                })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "entry_search_form": SearchEntryFrom()
    })

def entry_page(request, title):
    entry_request = util.get_entry(title)
    entry_md = markdowner.convert(str(entry_request))
    if entry_request != None:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry_md,
            "title": title
        })
    else:
        return render(request, "404.html")

def create_entry(request):
    if request.method == "POST":
        create_form = CreateEntry(request.POST)
        if create_form.is_valid():
            posted_title = create_form.cleaned_data["posted_title"]
            posted_content = create_form.cleaned_data["posted_content"]
            if posted_title in util.list_entries():
                messages.error(request, "Entry already exists")
                return render(request, "encyclopedia/create.html",{
                    "create_entry_form": create_form
                })
            else:
                f = open(f"./entries/{posted_title}.md", "w")
                f.write(posted_content)
                f.close()
                entry_request = util.get_entry(posted_title)
                entry_md = markdowner.convert(str(entry_request))
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry_md,
                    "title": posted_title
                })

    return render(request, "encyclopedia/create.html",{
        "create_entry_form":CreateEntry()
    })

def edit_entry(request, title):
    if request.method == "POST":
        EditEntryClass = dynamic_class('')
        edit_form = EditEntryClass(request.POST)
        if edit_form.is_valid():
            posted_content = edit_form.cleaned_data["posted_content"]
            f = open(f"./entries/{title}.md", "w")
            f.write(posted_content)
            f.close()
            entry_md = markdowner.convert(str(posted_content))
            return HttpResponseRedirect(reverse("wiki:entry_page", args=[title]))
    else:
        f = open(f"./entries/{title}.md", "r")
        populate = f.read()
        f.close()
        EditEntryClass = dynamic_class(populate)
        return render(request, "encyclopedia/edit.html",{
            "edit_entry_form":EditEntryClass(),
            "title": title})

def random_page(request):
    list_of_entries = util.list_entries()
    rnd_selected = list_of_entries[rnd.randint(0,len(list_of_entries)-1)]
    return HttpResponseRedirect(reverse("wiki:entry_page", args=[rnd_selected]))