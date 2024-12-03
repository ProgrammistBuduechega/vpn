from django.http import JsonResponse
import subprocess

class VPNApp:
    @staticmethod
    def start_vpn(request):
        try:
            # Запуск VPN-сервера
            subprocess.run(["python", "path/to/vpn_server.py"])
            return JsonResponse({"status": "VPN server started successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    @staticmethod
    def stop_vpn(request):
        try:
            # Остановка VPN-сервера
            subprocess.run(["pkill", "-f", "vpn_server.py"])
            return JsonResponse({"status": "VPN server stopped successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
