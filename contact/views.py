from django.shortcuts import render

def contact(request):
    return render(request, 'contact/contact.html',
    {'content':
    [['My email', 'pavlo.olshansky@gmail.com'],
    ['My adress', 'Novoyavorivsk']]})
