from django.shortcuts import render, redirect




def homepage(request):
    # visited = request.session.get("visited")
    # if not visited:
    #     request.session["visited"] = True
    # else:
    #     return redirect("pages:page")
    return render(request, 'homepage/welcome.html')