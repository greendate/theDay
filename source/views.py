from django.shortcuts import render, redirect
from .forms import UserEditForm, Create, ImageForm, StatusForm, CommentForm
from .models import UserInfo, Event, Coming, Image, Status, Like, Comment
from django.contrib.auth.models import User

def index(request):
    # create initial user info to avoid query errors
    if request.user.is_authenticated:
        if len(UserInfo.objects.filter(user=request.user)) == 0:
            user_inst = UserInfo()
            user_inst.user = request.user
            user_inst.save()
    return render(request, 'source/index.html')


def my(request):
    events = Event.objects.filter(organizer=request.user)
    user_inst = UserInfo.objects.get(user_id=request.user.id)
    return render(request, 'source/my.html', {'user': request.user, 'user_inst': user_inst, 'events': events})


def user(request, identity):
    user = User.objects.get(id=identity)
    user_inst = UserInfo.objects.get(user_id=identity)
    return render(request, 'source/user.html', {'user': user, 'user_inst': user_inst})


def new_event(request):
    if request.method == 'POST':
        event_inst = Event()
        form = Create(request.POST, request.FILES)

        event_inst.names = form.data["names"]
        print(request.POST.get('date'))
        event_inst.date = form.data["date"]
        event_inst.our_story = form.data["our_story"]
        event_inst.when = form.data["when"]
        event_inst.where = form.data["where"]
        event_inst.picture_url = request.FILES.get("picture_url")
        event_inst.organizer = request.user
        event_inst.save()
        return redirect("/my")
    form = Create()
    return render(request, 'source/new_event.html', {'form': form})


def edit(request):
    if request.method == 'POST':
        user_inst = UserInfo()
        form = UserEditForm(request.POST, request.FILES)

        user_inst.user = request.user
        user_inst.telegram_alias = form.data["telegram_alias"]
        user_inst.messenger_alias = form.data["messenger_alias"]
        user_inst.interests_description = form.data["interests_description"]
        if request.FILES.get("picture_url") != None:
             user_inst.picture_url = request.FILES.get("picture_url")
        else:
             picture_url =  UserInfo.objects.get(user=request.user).picture_url

        query = UserInfo.objects.filter(user=request.user)

        if not query:
            user_inst.save()
        else:
            user_inst.save(update_fields=["telegram_alias", "messenger_alias", "interests_description", "picture_url"])

        return redirect("/my")
    else:
        telegram = ""
        messenger = ""
        interests_description = ""
        picture_url = "source/static/img/default-profile-icon-16.png"
        # in order to have values from database in forms
        query = UserInfo.objects.filter(user=request.user)
        if not query:
            telegram = ".."
            messenger = ".."
        else:
             telegram = UserInfo.objects.get(user=request.user).telegram_alias
             messenger = UserInfo.objects.get(user=request.user).messenger_alias
             interests_description = UserInfo.objects.get(user=request.user).interests_description
             picture_url =  UserInfo.objects.get(user=request.user).picture_url
        form = UserEditForm(initial={'telegram_alias':telegram, 'messenger_alias': messenger, 'interests_description': interests_description, 'picture_url': picture_url})
    user_info = UserInfo.objects.get(user=request.user)
    return render(request, 'source/edit.html', {'form': form, 'user': request.user, 'user_info': user_info})


def posts(request, event_id):
    if request.method == 'POST':
        status_form = StatusForm(request.POST)
        status_model = Status()
        status_model.status_text = status_form.data["status_text"]
        status_model.event = Event.objects.get(id=event_id)
        status_model.save()
        return redirect('/posts/' + str(event_id))
    form = StatusForm()
    event =  Event.objects.get(id=event_id)
    status_list = Status.objects.filter(event=event.id)
    organizer = UserInfo.objects.get(user=event.organizer)
    for status in status_list:
        status.likes = len(Like.objects.filter(status=status))
        status.comments = len(Comment.objects.filter(status=status))
    return render(request, 'source/posts.html', {'form': form, 'event': event, 'posts': status_list, 'organizer': organizer})


def accept(request, event_id):
    acceptance = Coming()
    acceptance.user = request.user
    acceptance.event = Event.objects.get(id=event_id)
    acceptance.save()
    return redirect("/event/" + str(event_id))


def event(request, event_id):
    if not request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        return render(request, "source/nonregistered.html", {'event': event})
    in_list = Coming.objects.filter(event=Event.objects.get(id=event_id), user=request.user)
    image_list = Image.objects.filter(event=Event.objects.get(id=event_id))
    print(in_list)
    if(not in_list):
        event = Event.objects.get(id=event_id)
        ab_test = request.user.id % 2
        return render(request, "source/event.html", {'event': event, 'ab_test': ab_test})
    else:
        event = Event.objects.get(id=event_id)
        users = list(Coming.objects.filter(event=event))
        user_info_list = set()
        for user in users:
            print(user.user)
            user_info_list.add(UserInfo.objects.get(user=user.user))
        print(user_info_list)
        return render(request, "source/user_list.html", {'event': event, 'users': user_info_list, 'images': image_list})


def upload_to_gallery(request, event_id):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        image_model = Image()

        if form.is_valid():
            # form.save()
            image_model.event = Event.objects.get(id=event_id)
            image_model.picture = form.cleaned_data["picture"]
            image_model.description = form.cleaned_data["description"]
            image_model.save()
            return redirect('/event/' + str(event_id))
    else:
        form = ImageForm()
        form.data['event'] = Event.objects.get(id=event_id)
    return render(request, 'source/upload.html', {'form' : form})


def like(request, event_id, status_id):
    list = Like.objects.filter(status=status_id, user=request.user)
    if len(list) == 0:
        like_model = Like()
        like_model.status = Status.objects.get(id=status_id)
        like_model.user = request.user
        like_model.save()
    return redirect('/posts/' + str(event_id))


def comment(request, event_id, status_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment_model = Comment()
        comment_model.status = Status.objects.get(id=status_id)
        comment_model.user = UserInfo.objects.get(user=request.user)
        comment_model.comment = form.data["comment"]
        comment_model.save()
        return redirect('/comment/' + str(event_id) + "/" + str(status_id))
    form = CommentForm()
    event =  Event.objects.get(id=event_id)
    status = Status.objects.get(id=status_id)
    organizer = UserInfo.objects.get(user=event.organizer)
    comments = Comment.objects.filter(status=status)
    status.likes = len(Like.objects.filter(status=status))
    status.comments = len(Comment.objects.filter(status=status))
    return render(request, 'source/status.html', {'form' : form, 'post': status, 'organizer': organizer, 'comments': comments})
