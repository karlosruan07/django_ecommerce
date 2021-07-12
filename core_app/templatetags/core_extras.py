
from django import template

register = template.Library()

@register.inclusion_tag('arquivos_html/paginacao.html', takes_context=True)#takes_context recebe True para não ser preciso passar parâmetro pelo template
def paginacao(context):
      
    return{#vai retornar esses objetos para o arquivo paginacao.html
        'paginator' : context['paginator'],
        'request' : context['request'],
        'page_obj' : context['page_obj']
    }
 
 