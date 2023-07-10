from datetime import datetime
from django.shortcuts import render, redirect
from extrato.models import Valores
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_equilibrio_financeiro, calcula_total

# from django.http import HttpResponse
# from django.db.models import Sum


def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo="E")
    saidas = valores.filter(tipo="S")

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')

    contas = Conta.objects.all()
    total_contas = calcula_total(contas, 'valor')

# susbstituir por uma funcao generica calcula_total()
    # total_contas = 0
    # for conta in contas:
    #     total_contas += conta.valor

# Resolver o bug dessa L29 para mostrar os gastos essenciais
# do equilibrio finaceiro
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    return render(
        request, 'home.html',
        {'contas': contas, 'total_contas': total_contas,
         'total_entradas': total_entradas, 'total_saidas': total_saidas,
         'percentual_gastos_essenciais':
             int(percentual_gastos_essenciais),
         'percentual_gastos_nao_essenciais':
             int(percentual_gastos_nao_essenciais)})


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_contas = calcula_total(contas, 'valor')

# susbstituir por uma funcao generica calcula_total()
    # total_contas = contas.aggregate(Sum('valor'))['valor__sum']
    # total_contas = 0
    # for conta in contas:
    #     total_contas += conta.valor
    # print(total_contas)  # verificacao imprimi uma list na cli

    return render(
        request, 'gerenciar.html',
        {'contas': contas,
         'total_contas': total_contas,
         'categorias': categorias})


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(
            request, constants.WARNING, 'Preencha todos os campos!')
        return redirect('/perfil/gerenciar/')
    # Fazer as validacoes para a variavel banco e tipo...

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()

    # print(request.POST) # verificacao imprimi um Dict na cli
    messages.add_message(
        request, constants.INFO, 'Conta cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Conta excluida com sucesso!')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    # Fazer as validacoes do campo nome e essencial
    # use o isinstance para validar o true ou false
    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(
        request, constants.SUCCESS, 'Categoria cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial

    categoria.save()

    messages.add_message(
        request, constants.INFO, 'Atualizacao concluida com sucesso!')
    return redirect('/perfil/gerenciar/')


def dashboard(request):
    dados = {}

    categorias = Categoria.objects.all()

    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)

        for vl in valores:
            total = total + vl.valor
        dados[categoria.categoria] = total

    # print(dados.keys())

    return render(request, 'dashboard.html',
                  {'labels': list(dados.keys()),
                   'values': list(dados.values())})

# Outra forma usando o aggregate()
    # for categoria in categorias:
    #     dados[categoria.categoria] = Valores.objects.filter(
    #         categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    # return render(request, 'dashboard.html', {'labels': list(
    #     dados.keys()), 'values': list(dados.values())})
