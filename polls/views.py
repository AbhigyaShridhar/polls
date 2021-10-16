from django.utils import timezone
from datetime import timedelta
from .models import User, Poll, Choice

from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PollForm, ChoiceForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    polls = Poll.objects.filter(active=True, public=True)
    if request.user.is_authenticated:
        polls = Poll.objects.filter(active=True)
        for poll in polls:
            if poll.expiry:
                if poll.expiry <= timezone.now():
                    poll.active=False
                    poll.save()
        return render(request, "polls/index.html", {
            'polls': Poll.objects.filter(active=True),
            'h': "Active Polls",
        })
    for poll in polls:
        if poll.expiry <= timezone.now():
            poll.active=False
            poll.save()
    return render(request, "polls/index.html", {
        'polls': Poll.objects.filter(active=True, public=True),
        'h': "Active Polls",
    })

def past(request):
    polls = Poll.objects.all()
    if request.user.is_authenticated:
        polls = Poll.objects.filter(active=False)
    else:
        polls = Poll.objects.filter(active=False, public=True)
    return render(request, "polls/index.html", {
        'polls': polls,
        'h': "Past Polls",
    })

class Register(View):
    template = 'polls/register.html'
    success_url = 'polls:index'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        p1 = request.POST["password"]
        p2 = request.POST["password_repeat"]
        if not p1 == p2:
            return render(request, self.template, {
                'error':'Passwords do not match'
            })
        try:
            user = User.objects.create_user(username, email, p1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, self.template, {
                "message": "Email address or username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse(self.success_url))

class Login(View):
    template = 'polls/login.html'
    success_url = 'polls:index'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            return render(request, self.template, {
                "error": "Invalid username and/or password."
            })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:index'))

def detail(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    done = False
    if request.user in poll.voted.all():
        done = True
    return render(request, "polls/detail.html", {
        'poll': poll,
        'choices': Choice.objects.filter(poll=poll),
        'done': done,
        'time_left': poll.expiry - timezone.now(),
    })

class Create(LoginRequiredMixin, View):
    template = "polls/create.html"
    success_url = 'polls:detail'

    def get(self, request):
        form = PollForm()
        return render(request, self.template, {
            'form': form,
            'render_time': timezone.now()
        })

    def post(self, request):
        form = PollForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.owner = request.user
            if not instance.expiry:
                instance.expiry = instance.pub_date + timedelta(minutes = 5)
            instance.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'poll_id':instance.id, }))

        return render(request, self.template, {
            'form': PollForm(),
            'render_time': timezone.now(),
            'error': 'Something went Wrong!'
        })

def results(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    choices = Choice.objects.filter(poll=poll).order_by('-votes')

    return render(request, "polls/results.html", {
        'choices': choices,
    })

class AddChoice(LoginRequiredMixin, View):
    template = "polls/choice.html"
    success_url = "polls:detail"

    def get(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        form = ChoiceForm()
        return render(request, self.template, {
            'form': form,
            'poll': poll,
        })

    def post(self, request, poll_id):
        form = ChoiceForm(request.POST)
        poll = Poll.objects.get(id=poll_id)
        if form.is_valid():
            instance = form.save()
            instance.poll = poll
            instance.save()
            poll.expiry = poll.expiry + timedelta(minutes = 5)
            poll.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'poll_id':poll_id, }))

        return render(request, self.template, {
            'form': form,
            'error': 'Something went wrong, plese try again',
        })

def vote(request, poll_id, choice_id):
    poll = Poll.objects.get(id=poll_id)
    choice = Choice.objects.get(id=choice_id)

    if poll.expiry > timezone.now():
        poll.voted.add(request.user)
        poll.save()

        choice.votes = choice.votes + 1
        choice.save()


        return HttpResponseRedirect(reverse('polls:results', kwargs={'poll_id':poll_id, }))

    return HttpResponseRedirect(reverse('polls:detail', kwargs={'poll_id':poll_id, }))

@login_required
def profile(request):
    polls = Poll.objects.filter(owner=request.user)
    return render(request, "polls/profile.html", {
        'polls': polls
    })

@login_required
def remove(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    poll.delete()
    return HttpResponseRedirect(reverse('polls:index'))

def end(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if poll.owner == request.user:
        poll.active = False
        poll.save()
        return HttpResponseRedirect(reverse('polls:index'))
    return HttpResponse("Invalid Request!!")

def search(request):
    query = request.POST['search_input']
    output = []
    polls = Poll.objects.all()
    for poll in polls:
        if query in poll.content:
            output.append(poll)

    return render(request, "polls/index.html", {
        'h': "Search Results",
        'polls': output,
    })
