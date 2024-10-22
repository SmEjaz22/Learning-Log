from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import never_cache

@never_cache
def register(request):
    """Register a new user."""
    
    if request.user.is_authenticated:
        return render(request,'registration/already_registered.html')
    
    
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
        # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('Learning_logs:indexx')
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)



from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request,'registration/already_logged_in.html')
        return super().get(request)
# Use *args when you want to accept any number of positional arguments.
# Use **kwargs when you want to accept any number of keyword arguments.
