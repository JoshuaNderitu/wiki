from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import random
import markdown2

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })

def search(request):
    query = request.GET.get('q')
    if not query:
        return redirect('index')
    
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]

    if len(results) == 1 and results[0].lower() == query.lower():
        return redirect('entry', title=results[0])
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
        else:
            util.save_entry(title, content)
            return redirect('entry', title=title)

    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect('entry', title=title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect('entry', title=title)
