
from .models import Categoria

def categorias(request):
    return {
        'categorias': Categoria.objects.all()#retorna esse dicionario que será acessível com essa chave
    }

