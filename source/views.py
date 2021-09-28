from django.shortcuts import render, redirect
from .forms import UserEditForm, Create
from .models import UserInfo, Event, Coming
from django.contrib.auth.models import User

def index(request):
    return render(request, 'source/index.html')


def my(request):
    return render(request, 'source/user.html', {'user': request.user})


def user(request, identity):
    user = User.objects.get(id=identity)
    user_inst = UserInfo.objects.get(user_id=identity)
    return render(request, 'source/user.html', {'user': user, 'user_inst': user_inst})


def new_event(request):
    if request.method == 'POST':
        event_inst = Event()
        form = Create(request.POST)

        event_inst.names = form.data["names"]
        print(request.POST.get('date'))
        event_inst.date = form.data["date"]
        event_inst.our_story = form.data["our_story"]
        event_inst.when = form.data["when"]
        event_inst.where = form.data["where"]
        event_inst.picture_url = form.data["picture_url"]
        event_inst.organizer = request.user

        event_inst.save()
        return redirect("/")
    form = Create()
    return render(request, 'source/new_event.html', {'form': form})


def edit(request):
    if request.method == 'POST':
        user_inst = UserInfo()
        form = UserEditForm(request.POST)

        user_inst.user = request.user
        user_inst.telegram_alias = form.data["telegram_alias"]
        user_inst.messenger_alias = form.data["messenger_alias"]
        user_inst.interests_description = form.data["interests_description"]
        user_inst.picture_url = form.data["picture_url"]

        query = UserInfo.objects.filter(user=request.user)

        if not query:
            user_inst.save()
        else:
            user_inst.save(update_fields=["telegram_alias", "messenger_alias", "interests_description", "picture_url"])

        return redirect("/")
    else:
        telegram = ""
        messenger = ""
        interests_description = ""
        picture_url = "https://sample-cover.jpg"
        # in order to have values from database in forms
        query = UserInfo.objects.filter(user=request.user)
        if not query:
            telegram = "@.."
            messenger = "@.."
        else:
             telegram = UserInfo.objects.get(user=request.user).telegram_alias
             messenger = UserInfo.objects.get(user=request.user).messenger_alias
             interests_description = UserInfo.objects.get(user=request.user).interests_description
             picture_url =  UserInfo.objects.get(user=request.user).picture_url
        form = UserEditForm(initial={'telegram_alias':telegram, 'messenger_alias': messenger, 'interests_description': interests_description, 'picture_url': picture_url})
    return render(request, 'source/edit.html', {'form': form})


def accept(request, event_id):
    acceptance = Coming()
    acceptance.user = request.user
    acceptance.event = Event.objects.get(id=event_id)
    acceptance.save()
    return redirect("/")


def event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, "source/event.html", {'event': event})

def list(request, event_id):
    return redirect("/")
