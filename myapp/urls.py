from django.conf.urls import url

from . import views, failure_logging

urlpatterns = [
    url('^$', views.index),
    url('^index/', views.index),
    url('^login/', views.login),
    url('^ulogin/', views.ulogin),
    url('^logout/', views.logout),
    url('^upload/', views.upload_file),
    url('^upload_file_option/', views.upload_file_option),
    url('^delete_all_show/', views.Delete_all_show),
    url('^delete_all_data/', views.Delete_all_data),
    url('^show_Data_overview/', views.Show_data_Overview),
    url('^show_Data_electricMachinery/', views.Show_data_ElectricMachinery),
    url('^show_Data_voltageLevel/', views.Show_data_VoltageLevel),
    url('^Show_Data_DeviceType/',views.Show_data_DeviceType),
    url('^show_Data_InstallationPosition/', views.Show_data_InstallationPosition),
    url('^show_Data_MaintenanceLevel/', views.Show_data_MaintenanceLevel),
    url('^show_Data_OverhaulContents/', views.Show_data_OverhaulContents),
    url('^show_Data_OverhaulType/', views.Show_data_OverhaulType),
    url('^show_Add_User/', views.Show_add_user),
    url('^add_User/', views.Add_user),
    url('^Show_User/', views.Show_user),

    url('^logs_show/', views.Logs_show),
    url('^documentation/', views.Documentation),

    url('^failure_upload/', failure_logging.upload_file),
    url('^failure_upload_option/', failure_logging.upload_file_option),
    url('^failure_delete_all_show/', failure_logging.Delete_all_show),
    url('^failure_delete_all_data/', failure_logging.Delete_all_data),
    url('^show_failure_list/', failure_logging.Downtime_listing),
    url('^Add_Equipment_Downtime/', failure_logging.Add_Equipment_Downtime),
    url('^Add_Equipment_Downtime_option/', failure_logging.Add_Equipment_Downtime_option),
    url('^a_test/', views.A_t),

]