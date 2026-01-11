from django.shortcuts import render

from django.core.signing import Signer

from comments.models import Comment

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

from django.core.signing import dumps, loads
def cifrados(request):

    # Esto firma Y codifica el valor
    value = "hola mundo"
    signed_value = dumps(value) 
    print(signed_value) 
    # Resultado algo como: "ImhvbGEgbXVuZG8i:1t9Z2j:..." (No se lee "hola mundo")

    # Para recuperar el valor original
    original = loads(signed_value)
    print(original) # "hola mundo"
    return render(request,'pruebas/test.html')

import hashlib
def hash_python(request):

    value = "hola mundo"
    # Creamos el objeto hash sha256
    hash_object = hashlib.sha256(value.encode())
    # Obtenemos la representación hexadecimal
    hex_dig = hash_object.hexdigest()    

    # # Paso 2: Comparar
    # if hex_dig == passformlogin:
    #     print("¡Coincide! El texto es el original.")
    # else:
    #     print("No coincide. El texto es diferente.")

    return render(request,'pruebas/test.html')

from django.utils.crypto import salted_hmac, constant_time_compare
def hash_django(request):
    # Genera un hash usando tu SECRET_KEY como base
    value = "hola mundo"
    hash_resultado = salted_hmac('mi-sal-personalizada', value).hexdigest()
    print(hash_resultado)

    # # Generamos el hash con los mismos parámetros
    # nuevo_hash = salted_hmac(sal_usada, texto_usuario).hexdigest()

    # # TIP DE SEGURIDAD: Usa constant_time_compare para evitar ataques de tiempo
    # if constant_time_compare(nuevo_hash, hash_en_db):
    #     print("Verificado con éxito")

    return render(request,'pruebas/test.html')

def my_session(request):
    # request.session['comment_id'] = 5
    request.session['comments'] = [1,2,3,4,5]
    # request.session['comment'] = Comment.objects.get(pk=4)



    if 'comment' in request.session:
       print(f"Mostrando : {request.session['comment']}")


    # if 'comments' in request.session:
    #    print(f"Mostrando ID: {request.session['comments']}")


    # if 'comment_id' in request.session:
    #    print(f"Mostrando ID: {request.session['comment_id']}")
    #    del request.session['comment_id']
       

    return render(request,'pruebas/test.html')