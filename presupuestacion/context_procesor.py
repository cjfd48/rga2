from presupuestacion.models import UserProfile


def current_user_profile(request):
 if request.user.is_authenticated:
     user_profile=UserProfile.objects.get(user=request.user)
     return {'user_profile':user_profile}
