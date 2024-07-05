from django.urls import path
from .views import (index_view, login_view, logout_view, register_view, upload_view, like_view,
                    follow_view, profile_settings_view, profile_view, search_view,)

urlpatterns = [
    path('', index_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('upload/', upload_view),
    path('like/', like_view),
    path('follow/', follow_view),
    path('setting/', profile_settings_view),
    path('profile/', profile_view),
    path('search/', search_view),
    # path('delete/', post_delete_view),
]

# post_delete_view
