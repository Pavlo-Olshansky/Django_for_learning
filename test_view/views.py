from django.shortcuts import render

# Create your views here.
def greetings(request):
    context = {}
    if request.user.is_authenticated():
        # if request.user.is_active():
        context['user'] = request.user
    else:
        context['user'] = 'ANON'

    return render(request, "test_view/test_greetings.html", context)
