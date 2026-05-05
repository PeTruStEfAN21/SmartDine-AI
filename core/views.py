import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Produs, Comanda, ElementComanda

@login_required # Doar cei logați pot vedea
def dashboard_bucatarie(request):
    # Verificăm dacă e bucătar
    if request.user.groups.filter(name='Bucatar').exists() or request.user.is_superuser:
        return HttpResponse("Salut, Chef! Aici vor fi comenzile de gătit.")
    else:
        return HttpResponse("N-ai voie aici, doar bucătarii intră în bucătărie!", status=403)

def pagina_autentificare(request):
    return render(request, 'index.html')

def pagina_meniu(request):
    produse = Produs.objects.filter(disponibil=True)
    return render(request, 'meniu.html', {'produse': produse})

@csrf_exempt # Evităm blocajul CSRF pt simplitate deocamdată.
def plaseaza_comanda(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_items = data.get('cart', [])
            
            if not cart_items:
                return JsonResponse({'error': 'Coșul este gol!'}, status=400)

            comanda = Comanda.objects.create(total=0)
            total_comanda = 0

            for item in cart_items:
                produs = Produs.objects.get(id=item['id'])
                cantitate = item['quantity']
                pret_unitar = produs.pret
                
                ElementComanda.objects.create(
                    comanda=comanda, produs=produs,
                    cantitate=cantitate, pret_unitar=pret_unitar
                )
                total_comanda += (pret_unitar * cantitate)
            
            comanda.total = total_comanda
            comanda.save()
            return JsonResponse({'success': True, 'comanda_id': comanda.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Metodă nepermisă'}, status=405)