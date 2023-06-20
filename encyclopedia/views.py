from django.shortcuts import render
import markdown2

from . import util

def index(request):
    return render(request, 'encyclopedia/index.html', {
        "entries": util.list_entries
    })

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def entry(request, title): #takes request and title as input, returns a rendered HTML file as the response
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, 'encyclopedia/error.html', {
            "message": "Invalid entry"
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            "title": title,
            "content": html_content
        })

def search(request): #request is of method "POST", returns a rendered form of a html file as the response
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, 'encyclopedia/entry.html', { 
                "title": entry_search,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            recommendation = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, 'encyclopedia/search.html', {
                "recommendation": recommendation
            })
        
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, 'encyclopedia/error.html', {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(content)
            return render(request, "encyclopedia/entry.html", {
                "title" : title,
                "content" : html_content
            })
