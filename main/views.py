from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'app' : 'Strike Apparel',
        'name': 'Rheina Adinda Morani Sinurat',
        'class': 'PBP E'
    }

    return render(request, "main.html", context)
    