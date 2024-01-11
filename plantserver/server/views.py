from django.shortcuts import render

def websocket_view(request):
    return render(request, "websocket_test.html")