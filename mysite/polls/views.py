from django.http import HttpResponseRedirect,  HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.db import connection

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def admin_view(request):

    # This would fix the vulnerability by checking if user has admin
    # status before rendering the page

    #user = User.objects.get(id=request.session["user_id"])
    #
    #if not user.admin_status:
    #    return HttpResponseForbidden("Only admin has access")

    all_users = User.objects.all()
    return render(request, "polls/admin-view.html", {"users": all_users})



from django.shortcuts import render, redirect
from .models import User

def login(request):

    if "wrong_tries" not in request.session:
        request.session["wrong_tries"] = 0

    if request.session["failed_attempts"] >= 5:
        return render(request,"polls/login.html", {"error": "Too many failed login attempts. Please try again later."})

    if request.method == "POST":

        with connection.cursor() as cursor:

            name = request.POST["username"]
            psw = request.POST["password"]
            cursor.execute(
                 """
                 SELECT id, username, password, admin_status
                 FROM polls_user
                 WHERE username = %s
                 AND password = %s
                 """,
                 [name, psw])

            #cursor.execute(f"""SELECT id, username, password, admin_status
            #                FROM polls_user
            #                WHERE username = '{name}'
            #                AND password = '{psw}'
            #               """)
            result = cursor.fetchone()


        if result:
            request.session["wrong_tries"] = 0
            request.session["user_id"] = result[0]
            request.session["username"] = result[1]
            request.session["is_admin"] = result[3]

            return redirect("/")
        
    request.session["wrong_tries"] += 1
    return render(request, "polls/login.html")

def register(request):

    if request.method == "POST":
        name= request.POST["username"]
        psw = request.POST["password"]

        #from django.contrib.auth.hashers import make_password
        #psw = make_password(psw)

        User.objects.create(username=name,password=psw,admin_status=False)
        return redirect("/login/")

    return render(request,"polls/register.html")

def logout(request):

    request.session.flush()

    return redirect("/login/")