from django import forms

from models import Campus, Titulo, Categoria


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ('nome',)

class TituloForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        help_text='Selecione uma ou mais categorias',
        widget=forms.CheckboxSelectMultiple()
    )
    class Meta:
        model = Titulo
        fields = ('nome', 'categorias', 'imagem')