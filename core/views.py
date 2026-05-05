
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required # Doar cei logați pot vedea
def dashboard_bucatarie(request):
    # Verificăm dacă e bucătar
    if request.user.groups.filter(name='Bucatar').exists() or request.user.is_superuser:
        return HttpResponse("Salut, Chef! Aici vor fi comenzile de gătit.")
    else:
        return HttpResponse("N-ai voie aici, doar bucătarii intră în bucătărie!", status=403)

def pagina_meniu(request):
    return HttpResponse("Aici va fi meniul digital pe care îl vede toată lumea.")