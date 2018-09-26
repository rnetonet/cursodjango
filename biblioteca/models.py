# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError

class Campus(models.Model):
    nome = models.CharField('Nome', max_length=120, unique=True)

    def clean(self):
        if Campus.objects.exclude(pk=self.pk).filter(nome__icontains=self.nome):
            raise ValidationError("Nome já utilizado para outro campus")
        else:
            self.nome = self.nome.upper()
        

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'

class Biblioteca(models.Model):
    nome = models.CharField('Nome', max_length=120)
    campus = models.ForeignKey('biblioteca.Campus', verbose_name = 'Campus')

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Biblioteca'
        verbose_name_plural = 'Bibliotecas'

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=120)

    def __unicode__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Titulo(models.Model):
    nome = models.CharField('Nome', max_length=120)
    categorias = models.ManyToManyField('biblioteca.Categoria', verbose_name='Categorias')
    imagem = models.ImageField()

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'


class Exemplar(models.Model):
    biblioteca = models.ForeignKey('biblioteca.Biblioteca', verbose_name='Biblioteca')
    titulo = models.ForeignKey('biblioteca.Titulo', verbose_name='Título')
    data_aquisicao = models.DateField('Data de Aquisição', auto_now_add=True)

    def __unicode__(self):
        return self.titulo.nome
    
    class Meta:
        verbose_name = 'Exemplar'
        verbose_name_plural = 'Exemplares'


class PessoaFisica(models.Model):
    nome = models.CharField('Nome', max_length=120)
    username = models.CharField('Nome de Usuário', max_length=120)

    def __unicode__(self):
        return '{} {}'.format(self.nome, self.username)

    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'

class Emprestimo(models.Model):
    exemplar = models.ForeignKey('biblioteca.Exemplar', verbose_name='Exemplar')
    usuario = models.ForeignKey('biblioteca.PessoaFisica', verbose_name='Usuário')
    data_emprestimo = models.DateField('Data do Empréstimo', auto_now_add=True)
    data_previsto_devolucao = models.DateField('Data Prevista para Devolução', null=True, blank=True)
    data_devolucao = models.DateField('Data de Devolução', null=True, blank=True)

    def __unicode__(self):
        return '{} - por {} entre {} e {}'.format(self.exemplar, self.usuario, self.data_emprestimo, self.data_previsto_devolucao)