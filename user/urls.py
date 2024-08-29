from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
from .api_views import UserViewSet
from .views import *

# Create a router for the UserViewSet
userrouter = SimpleRouter()
userrouter.register(r'users', UserViewSet, basename='users_view')

# Include the router URLs in urlpatterns
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signup-submit/', register, name='signup_submit'),
    path('login/', login_view, name='login'),
    path('login-submit/', loginUser, name='login_submit'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('user-tasks/',user_tasks_view,name='user_tasks'), # all user's completed incompleted tasks
    path('install-complete/', app_page, name='install_complete'), # Clicking Incomplete tasks
    path('app/<int:app_id>/upload/', upload_screenshot, name='upload_screenshot'), # Proof for app installation
    path('admin/list-apps/', List_Apps, name='ListApps'),
    path('admin/add-app/', Add_app, name='add_app'),
    path('admin/add-app-submit/', Add_app_submit, name='add_app_submit'),
    path('admin/pending-tasks/', admin_pending_tasks, name='admin_pending_tasks'),
    path('admin/accept-task/<int:task_id>/', accept_task, name='accept_task'),
    path('', home, name='home'),
]

urlpatterns += userrouter.urls
if settings.DEBUG:
    print("((((((((((((((((((          added           ))))))))))))))))))")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)