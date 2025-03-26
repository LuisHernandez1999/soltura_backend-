from django.db import models
from django.core.exceptions import ValidationError
import re


def validar_nome(value):
    if not re.match("^[A-Za-záéíóúÁÉÍÓÚàáãâêôûçÇ ]+$", value):
        raise ValidationError('formato errado')
    
def validar_pa(value):
    if value not in ["1", "2", "3", "4"]:
        raise ValidationError('numero de PA errado')

def validar_colaborador(value):
    if value not in ["Motorista", "Coletor", "Operador"]:
        raise ValidationError('tipo de colaborador errado ')
    
class Colaborador(models.Model):
    TIPOS_FUNCAO = ['Motorista', 'Operador', 'Coletor']
    TIPOS_TURNO = ['Matutino", "Vespertino", "Noturno']
    TIPOS_STATUS = ['ATIVO', 'INATIVO']
    TIPOS_PA = ['PA1', 'PA2', 'PA3', 'PA4']


 
    
    nome = models.CharField(max_length=255, validators=[validar_nome])
    matricula = models.IntegerField(unique=True)
    pa = models.CharField(max_length=3, choices=[(x, x) for x in TIPOS_PA], validators=[validar_pa])
    turno = models.CharField(max_length=9, choices=[(y, y) for y in TIPOS_TURNO])  
    tipo = models.CharField(max_length=9, choices=[ (w,w) for w in TIPOS_FUNCAO
    ], validators=[validar_colaborador])
    status= models.CharField(max_length=9,choices=[(z, z) for z in TIPOS_STATUS])

    def __str__(self):
        return self.nome
    