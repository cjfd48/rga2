from _datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from presupuestacion.models import Proyecto,Poste,UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from presupuestacion.forms import ProyectoForm
from presupuestacion.forms import UserForm, UserProfileForm

def index(request):

    project_list = Proyecto.objects.all()
    context_dict = {'proyectos': project_list}
    if request.user.is_authenticated():
        userp=UserProfile.objects.get(user=request.user)
        context_dict['user_profile']=userp

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits += 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'presupuestacion/index.html', context_dict)

    return response


def about(request):
    #return HttpResponse('Rango says here is the about page.')
    context_dict = {'boldmessage': "Rango says here is the about page."}
    return render(request, 'presupuestacion/about.html', context_dict)

@login_required
def proyecto(request, proyecto_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        proyecto = Proyecto.objects.get(slug=proyecto_slug)
        context_dict['nombre_proyecto'] = proyecto.nombre

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        postes = Poste.objects.filter(proyecto=proyecto)

        # Adds our results list to the template context under name pages.
        context_dict['postes'] = postes
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['proyecto'] = proyecto
    except Proyecto.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'presupuestacion/proyecto.html', context_dict)
@login_required
def add_proyecto(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = ProyectoForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect(reverse('presupuestacion:index'))
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = ProyectoForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'presupuestacion/add_proyecto.html', {'form': form})


from presupuestacion.forms import PosteForm
@login_required
def add_poste(request, proyecto_slug):

    try:
        proy = Proyecto.objects.get(slug=proyecto_slug)
    except Proyecto.DoesNotExist:
                proy = None

    if request.method == 'POST':
        form = PosteForm(request.POST)
        if form.is_valid():
            if proy:
                poste = form.save(commit=False)
                poste.proyecto = proy
                # poste.views = 0
                poste.save()
                # probably better to use a redirect here.
                return HttpResponseRedirect(reverse('presupuestacion:proyecto',args=[proyecto_slug]))
        else:
            print(form.errors)
    else:
        form = PosteForm()

    context_dict = {'form':form, 'proyecto': proy}

    return render(request, 'presupuestacion/add_poste.html', context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            #user.set_password(user.password)
            #user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'presupuestacion/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    redirect_url=request.GET.get('next')
    if redirect_url is None:
        redirect_url="/"

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # print("segundo: "+request.GET['next'])
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                user_profile=UserProfile.objects.get(user=user)
                login(request,user)

                # return redirect()

                # print(redirect_url)
                return HttpResponseRedirect(redirect_url)
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...

        return render(request, 'presupuestacion/login.html',{'next':redirect_url})

from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Proyecto.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
        cat_list = []
        print(starts_with)
        if starts_with:
                cat_list = Proyecto.objects.filter(nombre__istartswith=starts_with)
                # print(cat_list)
        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


def suggest_category(request):

        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        cat_list = get_category_list(8, starts_with)
        print(cat_list)
        return render(request, 'presupuestacion/cats.html', {'cat_list': cat_list})