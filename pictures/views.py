from django.http import HttpResponse
from django.template import loader
from .models import Picture
from django.shortcuts import render, redirect
from .forms import PictureForm

def pictures(request):
    sort_by = request.GET.get('sort', 'name')

    valid_sort_fields = ['name', 'upload_date']

    if sort_by not in valid_sort_fields:
        sort_order = 'name'
    else:
        sort_order = sort_by

    pictures = Picture.objects.all().order_by(sort_order)

    context = {
        'pictures': pictures,
        'current_sort': sort_order,
    }

    template = loader.get_template('all_pictures.html')

    return HttpResponse(template.render(context, request))

def image(request, id):
    mypicture = Picture.objects.get(id=id)
    template = loader.get_template('image.html')
    context = {
      'mypicture': mypicture,
    }
    return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def upload_image(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PictureForm()
    return render(request, 'upload_image.html', {'form': form})

def delete_image(request):
    #TODO delete
    return redirect('/pictures')