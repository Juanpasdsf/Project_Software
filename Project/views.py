from django.http import HttpResponse

#Esto es una vista
def bienvenida(request): #Pasamos un objeto de tipo request como argumento 
    return HttpResponse("Proyecto de Ingenieria de Software")