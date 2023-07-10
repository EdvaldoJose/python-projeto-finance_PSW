from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from perfil.models import Categoria
import json


def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(
        request, 'definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor

    categoria.save()

    return JsonResponse({'status': 'Sucesso'})
# Desafio: colocar uma mensagem de 'Cadastro concluido com sucesso!'


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    # Desafio: Realizar barra com total ver modelo no figma (2:08)
    return render(request, 'ver_planejamento.html', {'categorias': categorias})
