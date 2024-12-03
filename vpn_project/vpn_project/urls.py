from django.urls import path
from .vpn_app import VPNApp

urlpatterns = [
    path('start_vpn/', VPNApp.start_vpn),
    path('stop_vpn/', VPNApp.stop_vpn),
]

