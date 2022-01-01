from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'mainapp'

urlpatterns = [
    path('', views.signin, name='signin'),
    path('admin/', admin.site.urls),
    path('ct', views.hello_ct, name='index_ct'),
    path('td', views.hello_td, name='index_td'),
    path('signin/', views.signin, name='signin'),
    path('signin/ct', views.signin_ct, name='signin_ct'),
    path('signin/td', views.signin_td, name='signin_td'),
    path('signin_submit/ct', views.signin_submit_ct, name='signin_submit_ct'),
    path('signin_submit/td', views.signin_submit_td, name='signin_submit_td'),
    path('signup/', views.signup, name='signup'),
    path('signup/ct', views.signup_ct, name='signup_ct'),
    path('signup/td', views.signup_td, name='signup_td'),
    path('signout/', views.signout, name='signout'),
    path('account/ct', views.account_ct, name='account_ct'),
    path('account/td', views.account_td, name='account_td'),
    path('remove_picture/', views.remove_picture, name='remove_picture'),
    path('addressbook_ct/', views.addressbook_ct, name='addressbook_ct'),
    path('addressbook_td/', views.addressbook_td, name='addressbook_td'),
    path('reportpb_ct/', views.reportpb_ct, name='reportpb_ct'),
    path('reportpb_td/', views.reportpb_td, name='reportpb_td'),
    path('pbsuccess_ct/', views.pbsuccess_ct, name='pbsuccess_ct'),
    path('pbsuccess_td/', views.pbsuccess_td, name='pbsuccess_td'),

    path('booking/', views.booking, name='booking'),
    path('mybookings/', views.mybookings, name='mybookings'),
    path('see_all_itineraries/', views.see_all_itineraries, name='see_all_itineraries'),
    path('add_item/', views.add_item, name='add_item'),
    path('delete_booking/<int:booking_id>', views.delete_booking, name='delete_booking'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),

    path('delete_itinerary/<int:itinerary_id>', views.delete_itinerary, name='delete_itinerary'),
    
    path('mytruck/', views.mytruck, name='mytruck'),
    path('newdelivery/', views.newdelivery, name='newdelivery'),
    path('alldeliveries/', views.alldeliveries, name='alldeliveries'),
    path('input_time/<int:booking>', views.input_time, name='input_time'),
    path('delete_itinerary/<int:itinerary_id>', views.delete_itinerary, name='delete_itinerary'),
    path('load_truck/<int:itinerary>', views.load_truck, name='load_truck'),
    

    path('td_select_booking/<int:itinerary>', views.td_select_booking, name='td_select_booking'),
    path('td_take_booking/<int:itinerary>/<int:booking>', views.td_take_booking, name='td_take_booking'),

    

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
