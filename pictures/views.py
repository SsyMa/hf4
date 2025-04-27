from django.http import HttpResponse
from django.template import loader
from .models import Picture
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PictureForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pictures')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pictures')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('main')

@login_required
def pictures(request):
    sort_by = request.GET.get('sort', 'name')

    valid_sort_fields = ['name', 'upload_date']

    if sort_by not in valid_sort_fields:
        sort_order = 'name'
    else:
        sort_order = sort_by

    pictures = Picture.objects.filter(owner=request.user).order_by(sort_order)

    context = {
        'pictures': pictures,
        'current_sort': sort_order,
    }

    template = loader.get_template('all_pictures.html')

    return HttpResponse(template.render(context, request))

def image(request, id):
    picture = Picture.objects.get(id=id)
    template = loader.get_template('image.html')
    context = {
      'picture': picture,
    }
    return HttpResponse(template.render(context, request))

def main(request):
  return redirect('/pictures')

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.owner = request.user
            picture.save()
            return redirect('pictures')
    else:
        form = PictureForm()
    return render(request, 'upload_image.html', {'form': form})

@login_required
def delete_image(request, id):
    picture = get_object_or_404(Picture, id=id, owner=request.user)
    if request.method == 'POST':
        picture.delete()
    return redirect('pictures')