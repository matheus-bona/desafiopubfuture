from django.shortcuts import render, redirect, get_object_or_404
from .models import Despesa, FormDespesa, TipoDespesa, FormTipoDespesa
from contas.models import Conta
from django.contrib import messages
from decimal import Decimal


def index(request):
    despesas = Despesa.objects.all()
    tipos_despesas = TipoDespesa.objects.all()
    return render(request, 'despesas/index.html', {
        'despesas': despesas,
        'tipos_despesas': tipos_despesas
    })


def cadastrar_despesa(request):
    if request.method != 'POST':
        form = FormDespesa()
        return render(request, 'despesas/cadastrar_despesa.html', {
            'form': form
        })
    form = FormDespesa(request.POST)
    if not form.is_valid():
        messages.error(request, 'Preencha todos os campos corretamente.')
        form = FormDespesa(request.POST)
        return render(request, 'despesas/cadastrar_despesa.html', {
            'form': form
        })
    id_conta = str(form.cleaned_data['conta_despesa'])
    obj_conta = Conta.objects.get(id=id_conta)
    obj_conta.saldo = obj_conta.saldo - Decimal(form.cleaned_data['valor'])
    obj_conta.save()
    form.save()
    messages.success(request, 'Despesa cadastrada com sucesso!')

    return redirect('despesas')


def cadastrar_tipo_despesa(request):
    if request.method != 'POST':
        form = FormTipoDespesa()
        return render(request, 'despesas/cadastrar_tipo_despesa.html', {
            'form': form
        })
    form = FormTipoDespesa(request.POST)
    if not form.is_valid():
        messages.error(request, 'Preencha todos os campos corretamente.')
        form = FormTipoDespesa(request.POST)
        return render(request, 'despesas/cadastrar_tipo_despesa.html', {
            'form': form
        })
    form.save()
    messages.success(request, 'Tipo de Despesa cadastrada com sucesso!')

    return redirect('despesas')


def editar_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id)
    tipos_despesas = TipoDespesa.objects.all()
    contas = Conta.objects.all()

    if request.method != 'POST':
        return render(request, 'despesas/editar_despesa.html', {
            'despesa': despesa,
            'tipos_despesas': tipos_despesas,
            'contas': contas,
        })

    novo_valor = request.POST.get('novo_valor')
    novo_data_pagamento = request.POST.get('novo_data_pagamento')
    novo_data_pagamento_esperado = request.POST.get('novo_data_pagamento_esperado')
    novo_tipo_despesa = request.POST.get('novo_tipo_despesa')
    novo_tipo_despesa_obj = tipos_despesas.filter(tipo_despesa=novo_tipo_despesa).first()

    novo_conta_despesa = request.POST.get('novo_conta_despesa')
    novo_conta_despesa_obj = contas.filter(id=novo_conta_despesa).first()

    if len(novo_valor) > 13:
        messages.error(request, 'Valor excede limite de dígitos.')
        return render(request, 'despesas/editar_despesa.html', {
            'despesa': despesa,
            'tipos_despesas': tipos_despesas,
            'contas': contas,
        })

    try:
        novo_valor = Decimal(novo_valor)
    except:
        messages.error(request, 'Digite apenas números no valor.')
        return render(request, 'despesas/editar_despesa.html', {
            'despesa': despesa,
            'tipos_despesas': tipos_despesas,
            'contas': contas,
        })

    if not novo_data_pagamento or not novo_data_pagamento_esperado:
        messages.error(request, 'Informe corretamente as datas.')
        return render(request, 'despesas/editar_despesa.html', {
            'despesa': despesa,
            'tipos_despesas': tipos_despesas,
            'contas': contas,
        })

    conta_atual = Conta.objects.get(id=str(despesa.conta_despesa))
    conta_atual.saldo = conta_atual.saldo + Decimal(despesa.valor)
    conta_atual.save()

    conta_nova = Conta.objects.get(id=str(novo_conta_despesa_obj))
    conta_nova.saldo = conta_nova.saldo - Decimal(novo_valor)
    conta_nova.save()

    despesa.valor = novo_valor
    despesa.data_pagamento = novo_data_pagamento
    despesa.data_pagamento_esperado = novo_data_pagamento_esperado
    despesa.tipo_despesa = novo_tipo_despesa_obj
    despesa.conta_despesa = novo_conta_despesa_obj
    despesa.save()
    messages.success(request, 'Despesa editada e estornos feitos com sucesso.')
    return redirect('despesas')


def deletar_despesa(request, despesa_id):
    if request.method != 'POST':
        despesas = Despesa.objects.all()
        return render(request, 'despesas/index.html', {
            'despesas': despesas
        })

    despesa = get_object_or_404(Despesa, id=despesa_id)
    conta_despesa = Conta.objects.get(id=str(despesa.conta_despesa))

    try:
        conta_despesa.saldo = conta_despesa.saldo + despesa.valor
        conta_despesa.save()
        despesa.delete()
        messages.success(request, 'Despesa deletada e valor estornado para conta.')
    except:
        messages.error(request, f'A despesa informada não existe!')

    despesas = Despesa.objects.all()
    return render(request, 'despesas/index.html', {
        'despesas': despesas
    })


def filtro_despesas(request):
    if request.method != 'POST':
        despesas = Despesa.objects.all()
        return render(request, 'despesas/index.html', {
            'despesas': despesas
        })

    data_pagamento_inicio = request.POST.get('data_pagamento_inicio')
    data_pagamento_fim = request.POST.get('data_pagamento_fim')
    tipo_despesa = request.POST.get('tipo_despesa')
    tipos_despesas = TipoDespesa.objects.all()

    if data_pagamento_inicio and data_pagamento_fim:
        despesas = Despesa.objects.filter(data_pagamento__range=[data_pagamento_inicio, data_pagamento_fim])
    else:
        despesas = Despesa.objects.all()

    if tipo_despesa != 'Todos':
        despesas = despesas.filter(tipo_despesa__tipo_despesa=tipo_despesa)

    return render(request, 'despesas/index.html', {
        'despesas': despesas,
        'tipos_despesas': tipos_despesas
    })
