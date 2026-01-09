from django.shortcuts import render

from django.core.signing import Signer

# Create your views here.
def crip(request):
    print('crip')

    # 1. Creamos la instancia
    signer = Signer()
    # 2. Firmamos un valor
    value = "hola mundo"
    signed_value = signer.sign(value)
    print(signed_value)
    original = signer.unsign(signed_value)
    print(original) # Resultado: ‘hola mundo’
    # Resultado: 'hola mundo:G9p8X...' (el texto original + la firma)
    signer_extra = Signer(salt='extra-proteccion')
    signed_with_salt = signer_extra.sign("hola mundo")
    print(signed_with_salt) # Resultado: ‘hola mundo’
    # print(signer_extra.unsign("hola mundo:dr1Xaz9cSdGO2LnfeascbAbfQmJ7Lcpmfavrmq3-iMw"))
    return render(request,'pruebas/test.html')