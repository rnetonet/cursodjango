# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

import forms
import models

# Config admin
admin.site.site_header = 'Curso Python e Django'
admin.site.index_title = 'Aplicações'

# Register your models here.
class CampusAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    form = forms.CampusForm

class BibliotecaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'campus')
    list_filter = ('campus', )

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


class TituloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'get_categorias', 'get_imagem')
    form = forms.TituloForm
    # fieldsets = (
    #     ('Dados Gerais', {
    #         'fields': ('nome', 'categorias')
    #     }),
    #     ('Upload de arquivos', {
    #         'fields': ('imagem', )
    #     }),
    # )

    def get_imagem(self, obj):
        return u'<img width=64 height=64 src="{}" />'.format(obj.imagem.url)

    get_imagem.short_description = 'Capa'
    get_imagem.allow_tags = True

    def get_categorias(self, obj):
        return "\n".join([c.nome for c in obj.categorias.all()])

class ExemplarAdmin(admin.ModelAdmin):
    list_display = ('id', 'biblioteca', 'titulo', 'data_aquisicao')
    list_filter = ('biblioteca', 'titulo', 'data_aquisicao')
    search_fields = ('titulo__nome', 'biblioteca__nome', 'biblioteca__campus__nome')
    data_hierarchy = 'data_aquisicao'

class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'username')


class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'exemplar', 'usuario', 'data_emprestimo', 'data_previsto_devolucao', 'data_devolucao')
    fields = ('exemplar', 'usuario')

admin.site.register(models.Campus, CampusAdmin)
admin.site.register(models.Biblioteca, BibliotecaAdmin)
admin.site.register(models.Categoria, CategoriaAdmin)
admin.site.register(models.Titulo, TituloAdmin)
admin.site.register(models.Exemplar, ExemplarAdmin)
admin.site.register(models.PessoaFisica, PessoaFisicaAdmin)
admin.site.register(models.Emprestimo, EmprestimoAdmin)
