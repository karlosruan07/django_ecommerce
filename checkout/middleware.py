
from .models import Carrinho

def cart_item_middleware(get_response):

    def middleware(request):
        
        session_key = request.session.session_key#faz uma cópia da chave antes da requisição
        response = get_response(request)

        if session_key != request.session.session_key:
            Carrinho.objects.filter(chave_carrinho=session_key).update(
                chave_carrinho=request.session.session_key
            )#atualiza a chave para a chave antiga

        return response
    
    return middleware

