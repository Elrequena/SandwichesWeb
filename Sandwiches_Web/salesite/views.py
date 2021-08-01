from django.shortcuts import render


def index(request):
    return render(request,'main_menu.html')

def sale_index(request):
    return render(request,'index.html')

