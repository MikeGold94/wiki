from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wikientry(request, title):
    markdowner = Markdown()
    wiki_entry = util.get_entry(title)
    if wiki_entry is None:
        return render(request, "encyclopedia/entrymissing.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/wikientry.html", {
            "entryAsHTML": markdowner.convert(wiki_entry),
            "title": title
        })
