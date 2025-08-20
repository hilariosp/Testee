from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Projeto
from .forms import ProjetoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
def index(request): 

    Projetos = Projeto.objects.all()
    return render(request, 'projeto/index.html', {'projetos': Projetos})

@login_required
def detail(request, id_projeto):  # CORRIGIDO

    projeto_obj = Projeto.objects.get(id=id_projeto)
    return render(request, 'projeto/detail.html', {'projeto': projeto_obj})

@login_required
@permission_required('projeto.add_Projeto', raise_exception=True)
def add(request): 

    if request.method == 'POST':

        form = ProjetoForm(request.POST)

        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.autor = request.user
            projeto.save()
            tags = form.cleaned_data.get('tags')
            if tags:
                projeto.tags.set(tags)
            membros = form.cleaned_data.get('membros_selecionados')
            orientador = form.cleaned_data.get('orientador_selecionado')

            if membros:
                projeto.membros.add(*membros)
            if orientador:
                projeto.membros.add(orientador)
            return HttpResponseRedirect('/projeto/')
    else:
        form = ProjetoForm()

    return render(request, 'projeto/add.html', { 'form': form })

@login_required
@permission_required('projeto.change_Projeto', raise_exception=True)
def update(request, id_projeto):  # CORRIGIDO

    projeto_obj = Projeto.objects.get(id=id_projeto)

    if request.method == 'POST':

        form = ProjetoForm(request.POST, instance=projeto_obj)

        if form.is_valid():
            projeto = form.save()
            tags = form.cleaned_data.get('tags')
            projeto.tags.set(tags)

            membros = form.cleaned_data.get('membros_selecionados')
            orientador = form.cleaned_data.get('orientador_selecionado')

            projeto.membros.clear()
            if membros:
                projeto.membros.add(*membros)
            if orientador:
                projeto.membros.add(orientador)

            return HttpResponseRedirect('/projeto/')
    else:

        initial_data = {
            'membros_selecionados': projeto_obj.membros.filter(tipo='Aluno'),
            'orientador_selecionado': projeto_obj.membros.filter(tipo='Orientador').first(),
        }
        form = ProjetoForm(instance=projeto_obj, initial=initial_data)
        form.fields['tags'].initial = projeto_obj.tags.all()


    return render(request, 'projeto/update.html', { 'form': form })

@login_required
@permission_required('projeto.delete_projeto', raise_exception=True)
def delete(request, id_projeto):  # CORRIGIDO
    #recuperar o Projeto do banco de dados 
    Projeto.objects.filter(id=id_projeto).delete()

    return HttpResponseRedirect('/projeto/')