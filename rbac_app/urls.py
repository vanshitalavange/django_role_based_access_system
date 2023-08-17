from django.urls import path
from . import views

urlpatterns = [

    # pages
    path('',views.render_home,name="home"),
    path('dashboard/',views.render_dashboard,name="render_dashboard"),
    path('forms/<str:form_type>/',views.render_forms,name="render_forms"),

    # apis
    path('login/',views.login,name="login"),
    path('user/add/',views.add_user,name="add_user"),
    path('user/delete/',views.delete_user,name="delete_user"),
    path('user/update/',views.update_user,name="update_user"),
    path('api/add/',views.add_API,name="add_API"),
    path('api/update/',views.update_API,name="update_API"),
    path('api/delete/',views.delete_API,name="delete_API"),
    path('api/all/',views.view_all_API,name="view_all_API"),
    path('user/api/',views.view_API_of_user,name="view_API_of_user"),
    path('map/api/',views.map_API_to_users,name="map_API_to_users"),
    path('get/map/api/',views.view_mapped_API,name="view_mapped_API"),
    path('unmap/user/',views.unmap_user,name="unmap_user")
]