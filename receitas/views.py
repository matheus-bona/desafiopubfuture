from django.shortcuts import render, redirect, get_object_or_404
from .models import Receita, FormReceita, TipoReceita, FormTipoReceita
from contas.models import Conta
from django.contrib import messages
from decimal import Decimal


def index(request):
    receitas = Receita.objects.all()
    tipos_receitas = TipoReceita.objects.all()
    return render(request, 'receitas/index.html', {
        'receitas': receitas,
        'tipos_receitas': tipos_receitas
    })


def cadastrar_receita(request):
    if request.method != 'POST':
        form = FormReceita()
        return render(request, 'receitas/cadastrar_receita.html', {
            'form': form
        })
    form = FormReceita(request.POST)
    if not form.is_valid():
        messages.error(request, 'Preencha todos os campos corretamente.')
        form = FormReceita(request.POST)
        return render(request, 'receitas/cadastrar_receita.html', {
            'form': form
        })
    id_conta = str(form.cleaned_data['conta_receita'])
    obj_conta = Conta.objects.get(id=id_conta)
    obj_conta.saldo = obj_conta.saldo + Decimal(form.cleaned_data['valor'])
    obj_conta.save()
    form.save()
    messages.success(request, 'Receita cadastrada com sucesso!')

    return redirect('receitas')


def cadastrar_tipo_receita(request):
    if request.method != 'POST':
        form = FormTipoReceita()
        return render(request, 'receitas/cadastrar_tipo_receita.html', {
            'form': form
        })
    form = FormTipoReceita(request.POST)
    if not form.is_valid():
        messages.error(request, 'Preencha todos os campos corretamente.')
        form = FormTipoReceita(request.POST)
        return render(request, 'receitas/cadastrar_tipo_receita.html', {
            'form': form
        })

    form.save()
    messages.success(request, 'Tipo de Receita cadastrada com sucesso!')

    return redirect('receitas')


def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    tipos_receitas = TipoReceita.objects.all()
    contas = Conta.objects.all()

    if request.method != 'POST':
        return render(request, 'receitas/editar_receita.html', {
            'receita': receita,
            'tipos_receitas': tipos_receitas,
            'contas': contas,
        })

    novo_valor = request.POST.get('novo_valor')
    novo_data_recebimento = request.POST.get('novo_data_recebimento')
    novo_data_recebimento_esperado = request.POST.get('novo_data_recebimento_esperado')
    novo_tipo_receita = request.POST.get('novo_tipo_receita')
    novo_tipo_receita_obj = tipos_receitas.filter(tipo_receita=novo_tipo_receita).first()

    novo_conta_receita = request.POST.get('novo_conta_receita')
    novo_conta_receita_obj = contas.filter(id=novo_conta_receita).first()

    if len(novo_valor) > 13:
        messages.error(request, 'Valor excede limite de dígitos.')
        return render(request, 'receitas/editar_receita.html', {
            'receita': receita,
            'tipos_receitas': tipos_receitas,
            'contas': contas,
        })

    try:
        novo_valor = Decimal(novo_valor)
    except:
        messages.error(request, 'Digite apenas números no valor.')
        return render(request, 'receitas/editar_receita.html', {
            'receita': receita,
            'tipos_receitas': tipos_receitas,
            'contas': contas,
        })

    if not novo_data_recebimento or not novo_data_recebimento_esperado:
        messages.error(request, 'Informe corretamente as datas.')
        return render(request, 'receitas/editar_receita.html', {
            'receita': receita,
            'tipos_receitas': tipos_receitas,
            'contas': contas,
        })

    conta_atual = Conta.objects.get(id=str(receita.conta_receita))
    conta_atual.saldo = conta_atual.saldo - Decimal(receita.valor)
    conta_atual.save()

    conta_nova = Conta.objects.get(id=str(novo_conta_receita_obj))
    conta_nova.saldo = conta_nova.saldo + Decimal(novo_valor)
    conta_nova.save()

    receita.valor = novo_valor
    receita.data_recebimento = novo_data_recebimento
    receita.data_recebimento_esperado = novo_data_recebimento_esperado
    receita.tipo_receita = novo_tipo_receita_obj
    receita.conta_receita = novo_conta_receita_obj
    receita.save()
    messages.success(request, 'Receita editada e estornos feitos com sucesso. ')
    return redirect('receitas')


def deletar_receita(request, receita_id):
    if request.method != 'POST':
        receitas = Receita.objects.all()
        return render(request, 'receitas/index.html', {
            'receitas': receitas
        })

    receita = get_object_or_404(Receita, id=receita_id)
    conta_receita = Conta.objects.get(id=str(receita.conta_receita))

    try:
        conta_receita.saldo = conta_receita.saldo - receita.valor
        conta_receita.save()
        receita.delete()
        messages.success(request, 'Receita deletada e valor estornado para conta.')
    except:
        messages.error(request, f'A receita informada não existe!')

    receitas = Receita.objects.all()
    return render(request, 'receitas/index.html', {
        'receitas': receitas
    })


def filtro_receitas(request):
    if request.method != 'POST':
        receitas = Receita.objects.all()
        return render(request, 'receitas/index.html', {
            'receitas': receitas
        })

    data_recebimento_inicio = request.POST.get('data_recebimento_inicio')
    data_recebimento_fim = request.POST.get('data_recebimento_fim')
    tipo_receita = request.POST.get('tipo_receita')
    tipos_receitas = TipoReceita.objects.all()

    if data_recebimento_inicio and data_recebimento_fim:
        receitas = Receita.objects.filter(data_recebimento__range=[data_recebimento_inicio, data_recebimento_fim])
    else:
        receitas = Receita.objects.all()

    if tipo_receita != 'Todos':
        receitas = receitas.filter(tipo_receita__tipo_receita=tipo_receita)

    return render(request, 'receitas/index.html', {
        'receitas': receitas,
        'tipos_receitas': tipos_receitas
    })
