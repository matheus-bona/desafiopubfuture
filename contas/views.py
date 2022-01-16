from django.shortcuts import render, redirect, get_object_or_404
from .models import Conta, TipoConta, FormConta, FormTipoConta
from django.contrib import messages
from decimal import Decimal


def index(request):
    contas = Conta.objects.all()
    return render(request, 'contas/index.html', {
        'contas': contas
    })


def transfer(request):
    if request.method != 'POST':
        return render(request, 'contas/transfer.html')
    conta_remetente = request.POST.get('conta_remetente')
    conta_destinatario = request.POST.get('conta_destinatario')
    valor_transferido = request.POST.get('valor_transferido')

    if not conta_remetente or not conta_destinatario or not valor_transferido:
        messages.error(request, 'Todos os campos devem estar preenchidos.')
        return render(request, 'contas/transfer.html')

    if conta_destinatario == conta_remetente:
        messages.error(request, 'O remetente não pode ser igual ao destinatário.')
        return render(request, 'contas/transfer.html')

    if len(valor_transferido) > 13:
        messages.error(request, 'Valor da transferência muito grande.')
        return render(request, 'contas/transfer.html')

    try:
        conta_remetente = int(conta_remetente)
        conta_destinatario = int(conta_destinatario)
        valor_transferido = Decimal(valor_transferido)
    except:
        messages.error(request, 'Digite apenas números.')
        return render(request, 'contas/transfer.html')


    obj_remetente = Conta.objects.get(id=conta_remetente)
    obj_destinatario = Conta.objects.get(id=conta_destinatario)

    obj_remetente.saldo = obj_remetente.saldo - valor_transferido
    obj_destinatario.saldo = obj_destinatario.saldo + valor_transferido

    obj_remetente.save()
    obj_destinatario.save()

    return redirect('index')


def editar_conta(request, conta_id):
    conta = get_object_or_404(Conta, id=conta_id)
    tipos = TipoConta.objects.all()

    if request.method != 'POST':
        return render(request, 'contas/editar_conta.html', {
            'conta': conta,
            'tipos': tipos,
        })

    novo_instituicao_financeira = request.POST.get('conta_instituicao_financeira')
    novo_saldo = request.POST.get('conta_saldo')
    novo_tipo_conta = request.POST.get('tipo_conta')
    novo_tipo_obj = tipos.filter(tipo_conta=novo_tipo_conta)

    if len(novo_saldo) > 13:
        messages.error(request, 'Valor excede limite de dígitos.')
        return render(request, 'contas/editar_conta.html', {
            'conta': conta,
            'tipos': tipos,
        })

    if not novo_instituicao_financeira or not novo_saldo:
        messages.error(request, 'Todos os campos devem estar preenchidos.')
        return render(request, 'contas/editar_conta.html', {
            'conta': conta,
            'tipos': tipos,
        })

    try:
        novo_saldo = Decimal(novo_saldo)
    except:
        messages.error(request, 'Digite apenas números no saldo.')
        return render(request, 'contas/editar_conta.html', {
            'conta': conta,
            'tipos': tipos,
        })

    obj_conta = Conta.objects.get(id=conta_id)
    obj_conta.instituicao_financeira = novo_instituicao_financeira
    obj_conta.saldo = novo_saldo
    obj_conta.tipo_conta = novo_tipo_obj.first()
    obj_conta.save()
    messages.success(request, 'Edição feita com sucesso!')
    return redirect('index')


def criar_conta(request):
    if request.method != 'POST':
        form = FormConta()
        return render(request, 'contas/criar_conta.html', {
            'form': form,
        })

    form = FormConta(request.POST)

    if not form.is_valid():
        messages.error(request, 'Preencha todos os campos')
        form = FormConta(request.POST)
        return render(request, 'contas/criar_conta.html', {
            'form': form,
        })
    form.save()
    messages.success(request, 'Cadastro feito com sucesso!')
    return redirect('index')


def criar_tipo_conta(request):
    if request.method != 'POST':
        form = FormTipoConta()
        return render(request, 'contas/criar_tipo_conta.html', {
            'form': form,
        })

    form = FormTipoConta(request.POST)

    if not form.is_valid():
        messages.error(request, 'Preencha todos os campos')
        form = FormTipoConta(request.POST)
        return render(request, 'contas/criar_tipo_conta.html', {
            'form': form,
        })
    form.save()
    messages.success(request, 'Cadastro feito com sucesso!')
    return redirect('index')


def deletar_conta(request):
    if request.method != 'POST':
        return render(request, 'contas/deletar_conta.html')
    conta_id = request.POST.get('conta_id')

    try:
        obj_conta = Conta.objects.get(id=conta_id)
        obj_conta.delete()
        messages.success(request, 'Conta deletada com sucesso!')
    except:
        messages.error(request, f'A conta {conta_id} não existe!')
        return render(request, 'contas/deletar_conta.html')

    return redirect('index')
