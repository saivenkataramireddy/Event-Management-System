from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.db.models import Sum
from django.core.files.storage import default_storage
from . models import Add_event, EventMedia, Registration, Users
from .serializers import UserSerializer,Add_eventSerializer

def home(request):
    available_dates = Add_event.objects.filter(is_booked=False).values_list('date', flat=True)
    events = Add_event.objects.all()
    return render(request, 'index.html', {
        "events": events,
        'available_dates': available_dates
    })

def login_check(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")

        user = Users.objects.filter(name=name, password=password).first()

        if user is None:
            return HttpResponse("Invalid Username or Password")

        request.session['user_id'] = user.id 

        if user.role == "user":
            return redirect('user_dashboard', user_id=user.id)
        elif user.role == "admin":
            request.session['admin_name'] = user.name
            return redirect("admin_page")
        else:
            return HttpResponse("Invalid role assigned to user")

    return HttpResponse("Invalid request", status=405)



def register_check(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")

        if Users.objects.filter(name=username).exists():
            return render(
                request,
                "index.html",
                {
                    "error_message": "Username already exists!",
                    "show_register_form": True,  
                },
            )

        data = {
            "name": username,
            "password": password,
            "address": address,
            "phone_number": phone_number
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect("home")
        else:
            return HttpResponse(serializer.errors, status=400)

    return HttpResponse("Invalid request method", status=405)


def add_event(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "phonenumber": request.POST.get("phonenumber"),
            "budget": request.POST.get("event_budget"),
            "description": request.POST.get("description"),
            "date": request.POST.get("date"),
            "location": request.POST.get("location")
        }
        serializer = Add_eventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect("admin_page")
        else:
            return HttpResponse(serializer.errors, status=400)
    return HttpResponse("Invalid Data", status=405)


def admin_page(request):
    users = Users.objects.filter(role="user")
    events = Add_event.objects.all()
    all_media = EventMedia.objects.all().order_by('-uploaded_at')
    total_users = Users.objects.count()
    total_budget = Add_event.objects.aggregate(Sum('budget'))['budget__sum'] or 0
    total_events = Add_event.objects.count()

    admin_name = request.session.get('admin_name', 'Admin')

    return render(request, "admin.html", {
        "users": users,
        "events": events,
        "total_users": total_users,
        "total_budget": total_budget,
        "total_events": total_events,
        "user": {"name": admin_name},
        "all_media" : all_media
    })

def edit_event(request, id):
    event = get_object_or_404(Add_event, id=id)

    if request.method == "POST":
        event.name = request.POST.get("name")
        event.phonenumber = request.POST.get("phonenumber")
        event.budget = request.POST.get("event_budget")
        event.description = request.POST.get("description")
        event.date = request.POST.get("date")
        event.location = request.POST.get("location")
        event.save()
        return redirect("admin_page")

    return HttpResponse("Invalid request", status=405)

def delete_event(request,id):
    if request.method=="POST":
        event=get_object_or_404(Add_event,id=id)
        event.delete()
        return redirect("admin_page")
    return HttpResponse("Invalid request method",status=405)

def delete_user(request,id):
    if request.method=="POST":
        user=get_object_or_404(Users,id=id)
        user.delete()
        return redirect("admin_page")
    return HttpResponse("Invalid request method",status=405)

def edit_user(request, id):
    user = get_object_or_404(Users, id=id)
    if request.method == "POST":
        serializer = UserSerializer(user, data={
            "name": request.POST.get("username"),
            "password": request.POST.get("password"),
            "address": request.POST.get("address"),
            "phone_number": request.POST.get("phone_number")
        })
        if serializer.is_valid():
            serializer.save()
            return redirect("admin_page")  
        else:
            return HttpResponse(serializer.errors, status=400)
    return HttpResponse("Invalid request method", status=405)

def user_dashboard(request, user_id):
    session_user_id = request.session.get("user_id")
    if not session_user_id:
        return redirect("home")

    user = get_object_or_404(Users, id=session_user_id)
    user_events = Add_event.objects.filter(booked_by=user)
    all_media = EventMedia.objects.all().order_by('-uploaded_at')

    return render(request, "user.html", {
        "user": user,
        "events": user_events,
        "all_media": all_media
    })



def create_event(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    
    if request.method == "POST":
        event_date = request.POST.get("date")

        if Add_event.objects.filter(date=event_date).exists():
            messages.error(request, "Sorry, there’s already an event on that date. Please choose another date.")
            return redirect('user_dashboard', user_id=user.id)

        Add_event.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            budget=request.POST.get("budget"),
            date=event_date,
            location=request.POST.get("location"),
            booked_by=user,
            status="pending"
        )

        messages.success(request, "Your event has been added successfully and is under review!")
        return redirect('user_dashboard', user_id=user.id)

    return redirect('user_dashboard', user_id=user.id)


def accept_event(request, id):
    event = get_object_or_404(Add_event, id=id)
    event.status = "accepted"
    event.save()
    return redirect("admin_page")

def reject_event(request, id):
    event = get_object_or_404(Add_event, id=id)
    event.status = "rejected"
    event.save()
    return redirect("admin_page")

def upload_event_media(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        video = request.FILES.get("video")
        image = request.FILES.get("image")

        EventMedia.objects.create(
            name=name,
            description=description,
            video=video,
            image=image
        )
        messages.success(request, "Media uploaded successfully!")
        return redirect("admin_page")
    return redirect("admin_page")

def delete_media(request, media_id):
    if request.method == 'POST':
        media = get_object_or_404(EventMedia, id=media_id)

        image_path = media.image.path if media.image else None
        video_path = media.video.path if media.video else None

        media.delete()

        if image_path and default_storage.exists(image_path):
            default_storage.delete(image_path)

        if video_path and default_storage.exists(video_path):
            default_storage.delete(video_path)

        if 'from_user' in request.POST:
            return redirect('view_events')
        return redirect('admin_page')

    return HttpResponse("Invalid request method", status=405)


def view_events(request):
    events = EventMedia.objects.all()
    return render(request,"view_events.html", {
        "events":events
    })