from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from models import Campus, Categoria, Emprestimo, PessoaFisica, Titulo, Exemplar


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ('nome',)

class TituloForm(forms.ModelForm):
    nome = forms.CharField(
        min_length=3, 
        max_length=10, 
        strip=True
    )

    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        help_text='Selecione uma ou mais categorias',
        widget=forms.CheckboxSelectMultiple()
    )

    def clean_categorias(self):
        categorias_selecionadas = self.cleaned_data.get('categorias')
        if len(categorias_selecionadas) < 3:
            raise ValidationError("Por favor, selecione ao menos 3 categorias.")
        return categorias_selecionadas

    class Meta:
        model = Titulo
        fields = ('nome', 'categorias', 'imagem')


class PessoaFisicaForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if PessoaFisica.objects.filter(username__exact=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Nome em uso!")
        return username
    

    class Meta:
        model = PessoaFisica
        fields = ('nome', 'username')

class EmprestimoForm(forms.ModelForm):
    exemplar = forms.ModelChoiceField(
        queryset=Exemplar.objects,
        
    )

    def __init__(self, *args, **kwargs):
        super(EmprestimoForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['data_devolucao'].redonly = False
            
            self.fields['exemplar'].readonly = True
            self.fields['exemplar'].queryset = Exemplar.objects.exclude(pk__in=Emprestimo.objects.exclude(pk=self.instance.pk).filter(Q(data_devolucao__isnull=True) | Q(data_previsto_devolucao__gt=datetime.today())).values_list('exemplar'))
        else:
            self.fields['data_devolucao'].widget = forms.HiddenInput()
            self.fields['exemplar'].queryset = Exemplar.objects.exclude(pk__in=Emprestimo.objects.filter(Q(data_devolucao__isnull=True) | Q(data_previsto_devolucao__gt=datetime.today())).values_list('exemplar'))

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.data_previsto_devolucao = datetime.now() + timedelta(days=30)
        
        return super(EmprestimoForm, self).save(*args, **kwargs)

    class Meta:
        model = Emprestimo
        fields = ('exemplar', 'usuario', 'data_devolucao')

