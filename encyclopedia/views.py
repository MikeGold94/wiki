from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from random import randint
from os import path

'''
from django.urls import reverse
'''
from django.http import HttpResponseRedirect

from . import util


class NewSearchForm(forms.Form):
    searchQuery = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia',
                                                                          'class': 'search'}))


class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Enter title of new wiki entry here...', 'class': 'search'}))
    entryForm = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter a new wiki entry here...', 'class': 'search'}), label="")


def index(request):
    if request.method == "POST":

        form = NewSearchForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the searchquery from the 'cleaned' version of form data
            searchquery = form.cleaned_data["searchQuery"]

            # Define variables bool_entryfound and array_string_searchresults from search method
            bool_entryfound, array_string_searchresults = util.search(searchquery)
            # Redirect user to list of tasks
            if bool_entryfound:
                print(f"Found one entry for searchquery {searchquery}")
                return wikientry(request, array_string_searchresults[0])
            elif not bool_entryfound and len(array_string_searchresults) == 0:
                print(f"Found no entries for searchquery {searchquery}")
                return wikientry(request, searchquery)
            else:
                print(f"Found {len(array_string_searchresults)} entries for searchquery {searchquery}")
                return render(request, "encyclopedia/index.html", {
                    "entries": array_string_searchresults,
                    "form": NewSearchForm()
                })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })


def wikientry(request, title):
    print(f"Searching for title: {title}")
    markdowner = Markdown()
    wiki_entry = util.get_entry(title)
    if wiki_entry is None:
        return render(request, "encyclopedia/entrymissing.html", {
            "title": title,
            "form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/wikientry.html", {
            "entryAsHTML": markdowner.convert(wiki_entry),
            "title": title,
            "form": NewSearchForm()
        })


def random(request):
    """
    Returns a random wiki entry
    :return: render
    """
    print("Searching for random wiki entry")
    list_string_allentries = util.list_entries()
    int_random = randint(0, len(list_string_allentries) - 1)
    print(f"Entry {list_string_allentries[int_random]} was chosen. Navigating to wiki entry page.")
    # return wikientry(request, path.splitext(list_string_allentries[int_random])[0])
    return HttpResponseRedirect(path.splitext(list_string_allentries[int_random])[0])


def newentry(request):
    if request.method == "POST":

        newentryform = NewEntryForm(request.POST)

        str_new_entry_title: str
        str_new_entry_data: str

        # Check if form data is valid (server-side)
        if newentryform.is_valid():
            str_new_entry_title, str_new_entry_data = newentryform.cleaned_data["title"], newentryform.cleaned_data["entryForm"]

            if util.search(str_new_entry_title)[0]:
                return render(request, "encyclopedia/newentry.html", {
                    "form": NewSearchForm,
                    "entry": newentryform,
                    "warning": True
                })
            else:
                f = open(f"entries/{str_new_entry_title}.md", "w+")
                f.write(str_new_entry_data)
                f.close()
                return HttpResponseRedirect(str_new_entry_title)
    else:
        return render(request, "encyclopedia/newentry.html", {
            "form": NewSearchForm(),
            "entry": NewEntryForm()
        })
