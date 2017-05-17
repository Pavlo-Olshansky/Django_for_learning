from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView
from .models import Post_blog, Author
from .form import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import time

class Post_list(ListView):
    model = Post_blog
    template_name = 'blog/post_blog.html'


class Post_list_detail(DetailView):
    model = Post_blog
    template_name = 'blog/post.html'


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            posts = Post_blog.objects.filter(title__icontains=q)
            return render(request, 'blog/search_results.html',
                          {'posts': posts, 'query': q})
    return render(request, 'blog/search_form.html', {'errors': errors})


def contact(request):
    congrat_message = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'pavlopavlo2012@mail.ru'),
                ['pavlo.olshansky@gmail.com'],
            )
            congrat_message = 'Thanks for the message! Send another?'
            # return HttpResponseRedirect('/blog/contact_form.html', {'congrat_message': 'Thanks for the message! Send another?'})
    else:
        form = ContactForm(
            initial={'subject': 'I love your site!'}
        )

    return render(request, 'blog/contact_form.html', {'form': form,
                                                      'congrat_message': congrat_message})

class Authors(ListView):
    model = Author
    template_name = 'blog/authors.html'


from django.utils.translation import ugettext as _

# @csrf_protect
# @cache_page(60 * 15)  # but better to cache view in URLs
def my_view(request):
    context = {}

    context['posts'] = Post_blog.objects.filter()
    if request.user.is_authenticated():
        context['username'] = request.user.get_username()

        if 'count' in request.session:
            request.session['count'] += 1
        else:
            request.session['count'] = 1
        context['count'] = request.session['count']

        if "favotire" in request.GET:
            request.session['favotire'] = request.GET['favotire']
            context['favotire'] = request.session['favotire']

            # Translators: This message appears on the home page only
            context['message'] = _("not log Your current blog is %s " % request.session["favotire"])


        elif 'favotire' in request.session:
            context['favotire'] = request.session['favotire']

            # Translators: This message appears on the home page only
            context['message'] = _("log Your current blog is %s " % request.session["favotire"])
        else:
            context['favotire'] = None
            context['message'] = "log You don't have a favorite blog."

        # return HttpResponse('You are logged, count={}'.format(request.session['count']), request.session['count'])
        return render (request, 'blog/my_test_view.html', context)
    else:
        context['username'] = None
        print(context['username'])
        if 'not_count' in request.session:
            request.session['not_count'] += 1
        else:
            request.session['not_count'] = 1

        if "favotire" in request.GET:
            request.session['favotire'] = request.GET['favotire']
            context['favotire'] = request.session['favotire']
            context['message'] = "not log Your current blog is %s " % request.session["favotire"]

        elif 'favotire' in request.session:
            context['favotire'] = request.session['favotire']
            context['message'] = "not log Your current blog is %s " % request.session["favotire"]
        else:
            context['favotire'] = None
            context['message'] = "not log You don't have a favorite blog."

        context['not_count'] = request.session['not_count']
        return render (request, 'blog/my_test_view.html', context)

def my_view_choose(request):
    context = {}

    context['posts'] = Post_blog.objects.filter()
    context['username'] = request.user.get_username()

    # if 'favotire' in request.session:
    #     context['favotire'] = request.session['favotire']
    #     context['message'] = "Your current blog is %s " % request.session["favotire"]
    # else:
    #     context['favotire'] = None
    #     context['message'] = "You don't have a favotire blog."

    context['favotire'] = request.session['favotire']

    if "favotire" in request.GET:
        request.session['favotire'] = request.GET['favotire']
        context['favotire'] = request.session['favotire']
        context['message'] = "not log Your current blog is %s " % request.session["favotire"]

    elif request.session.has_key('favorite'):
        context['favotire'] = request.session['favotire']
        context['message'] = "not log Your current blog is %s " % request.session["favotire"]

    else:
        # context['favotire'] = request.session['favotire']
        # context['message'] = "none Your current blog is %s " % request.session["favotire"]
        context['message'] = 'Choose your favorite !'
    return render(request, 'blog/my_test_view_choose.html', context)

    # return HttpResponse('You are logged, count={}'.format(request.session['count']), request.session['count'])


# @csrf_protect
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/blog/register_success/')
    else:
        form = RegistrationForm()

    return render(
        request,
        'registration/register.html',
        { 'form': form }
    )


def register_success(request):
    return render(request,
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render(request,
        'home/home.html',
        {'user': request.user}
    )

import csv
from django.http import HttpResponse

def download_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"'])

    return response



from django.http import StreamingHttpResponse
class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response

from reportlab.pdfgen import canvas
from django.http import HttpResponse

from io import BytesIO

def pdf_downloader(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Downloaded.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def img_downloader(request):
    image_data = open("static/home/img/phones.png", "rb").read()

    response = HttpResponse(image_data, content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename="Downloaded.png"'

    return response


from django.utils.translation import ugettext as _
def internalization(request):
    from django.utils import translation
    user_language = 'fr'
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    context = {}
    year = [2007]
    context['year'] = year
    years = (2007, 2008, 2009)
    context['count_years'] = len(years)
    context['count_year'] = len(year)
    context['years'] = years
    price_per_year = 20
    context['price_per_year'] = price_per_year
    context['hello'] = _("привіт")

    return render(request, 'blog/internalization/internalization.html', context)

from django.utils.translation import ugettext as _
from django.http import HttpResponse

def test(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)


# -------------------------SECURITY--------------------------------------

# TEMPLATES
#  http://djangobook.com/security-in-django/
# < form action = "." method = "post" > { % csrf_token %}

from django.views.decorators.cache import cache_page
# from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.csrf import csrf_exempt
#
# @cache_page(60 * 15)
# @csrf_protect
def my_view_2(request):
    pass

# @requires_csrf_token
# @csrf_exempt # pass the csrf
def my_view_3(request):
    return HttpResponse('Hello world')

from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
# @xframe_options_deny
# @xframe_options_sameorigin  # browser will only load the resource in a frame if the request originated from the same site.
def ok_to_load_in_a_frame(request):
    return HttpResponse("This page is safe to load in a frame on any site.")



# def display_meta(request):
#     values = request.META.items()
#     # values.sort()
#     html = []
#     for k, v in values:
#         html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
#     return HttpResponse('<table>%s</table>' % '\n'.join(html))
