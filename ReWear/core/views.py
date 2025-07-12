from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, get_object_or_404

# Create your views here.


def details(request):
    return render(request, "details.html")

def details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, "details.html", {"product": item})

def dashboard(request):
    return render(request, "userdashboard.html")

def admindashboard(request):
    return render(request, "admindashboard.html")


def create_item(request):
    if request.method == 'POST':
        # === Process submitted form ===
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        type_ = request.POST.get('type')
        size = request.POST.get('size')
        condition = request.POST.get('condition')
        tags_raw = request.POST.get('tags', '')
        swap_points = int(request.POST.get('swap_points', 0))
        is_available = 'is_available' in request.POST

        # Create item object
        item = Item.objects.create(
            title=title,
            description=description,
            image=image,
            category=category,
            type=type_,
            size=size,
            condition=condition,
            swap_points=swap_points,
            is_available=is_available,
            owner=request.user
        )

        # Process tags
        tag_names = [tag.strip() for tag in tags_raw.split(',') if tag.strip()]
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            item.tags.add(tag)

        item.save()

        return redirect('details')

    else:
        # === Render blank form for GET ===
        return render(request, 'additem.html')
