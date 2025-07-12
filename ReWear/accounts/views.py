from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Create your views here.
User = get_user_model()  # use custom user model



@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Field name is still 'username' in HTML
        password = request.POST.get('password')

        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/core/dashboard')  # replace with your post-login route
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile = request.FILES.get('profile')

        # ✅ Basic validation
        if not email or not password1 or not password2:
            messages.error(request, 'Email and passwords are required.')
            return render(request, 'register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'register.html')

        try:
            # ✅ Create user manually
            user = User.objects.create_user(
                username=email,  # still required by AbstractUser
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )

            # ✅ Attach optional profile image
            if profile:
                user.Profile = profile
                user.save()

            # ✅ Auto-login after registration
            login(request, user)
            return redirect('/core/dashboard')
        except ValidationError as ve:
            messages.error(request, f'Validation error: {ve.messages}')
        except Exception as e:
            messages.error(request, f'Unexpected error: {str(e)}')

    return render(request, 'register.html')