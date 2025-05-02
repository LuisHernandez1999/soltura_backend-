from django.db import models
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo
from django.core.exceptions import ValidationError
from datetime import date,time
import datetime

class Soltura(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo')
    ]  
    
    TIPO_SERVICO = [("Seletiva","Seletiva"),
                    ("Coleta","Coleta"),
                    ("Remoção", "Remoção"),
                    ("Varrição","Varrição")
                ]
    
    TIPO_EQUIPE= [("Equipe1(Matutino)","Equipe1(Matutino)"),
                  ("Equipe2(Vespertino)","Equipe2(Vespertino)"),
                  ("Equipe3(Noturno)","Equipe3(Noturno)")]
    
    PAS = [('PA1','PA1'),
          ('PA2','PA2'), 
          ('PA3','PA3'),
          ('PA4','PA4')]

    TIPO_COLETA_CHOICES = [
        ('Seletiva', 'Seletiva'),
        ('Coleta', 'Coleta'),
        ('Cata Treco', 'Cata Treco'),
        ('Varrição', 'Varrição'),

    ]

    TURNO_CHOICES = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno')
    ]

    motorista = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        limit_choices_to={'funcao': 'Motorista', 'status': 'ATIVO'},  
        related_name='solturas_motorista'
    )
    coletores = models.ManyToManyField(
        Colaborador,
        limit_choices_to={'funcao': 'Coletor', 'status': 'ATIVO'},  
        related_name='solturas_coletor'
    )
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'ATIVO'},  
        related_name='solturas'
    )
    hora_entrega_chave = models.TimeField(null=False, blank=False,default= time(8, 0))
    hora_saida_frota = models.TimeField(null=False, blank=False,  default=  time(8, 10))
    frequencia = models.CharField(
        max_length=50,
        choices=[('Diária', 'Diária'), ('Semanal', 'Semanal'), ('Mensal', 'Mensal')],
        default='Diária'
    )
    
    STATUS_DA_FROTA = [('Em Andamento','Em Andamento'),
                        ('Finalizada','Finalizada')]
    TIPO_VEICULO=[('Baú','Baú'),
                  ('Baculante','Basculante'),
                  ('Seletolix','Seletolix')]

    rota=models.CharField(max_length=10,null=True,blank=False,default='AND1')
    garagem = models.CharField(max_length=10,null=False,choices=PAS,
        blank=False,default=' PA1')
    setores = models.CharField(max_length=55)  
    celular = models.CharField(max_length=20)  
    lider = models.CharField(max_length=55)  
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ATIVO')
    tipo_coleta = models.CharField(max_length=10, choices=TIPO_COLETA_CHOICES) 
    tipo_servico= models.CharField(max_length=10, choices=TIPO_SERVICO,null=False,
    blank=False,default='Seletiva') 
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    tipo_equipe = models.CharField(max_length=20, choices=TIPO_EQUIPE,null=False,
        blank=False,default='Equipe1(Matutino)')
    data = models.DateField(null=False, blank=False, default=date(2025, 1, 1))
    hora_chegada =models.TimeField(null=True, blank=False,default=time(14, 14))
    status_frota =models.CharField(max_length=14,null=True,choices=STATUS_DA_FROTA,blank=False,default='Finalizado')
    tipo_veiculo_selecionado= models.CharField(max_length=14,null=True,choices=TIPO_VEICULO,blank=False,default='Basculante')
    bairro = models.CharField(max_length=100,null=True,blank=False,default='Guanabara')
    def clean(self):
        if self.veiculo.status != 'ATIVO':
            raise ValidationError("O veículo associado deve ser ativo para cadastrar a soltura.")

    
    def __str__(self):
        return f"Soltura - {self.motorista.nome} ({self.veiculo.prefixo})"

     
    def rota_remocao(self):
        if self.tipo_servico == 'Remoção':
            return None

    def rota_coleta(self):
        if self.tipo_servico == 'Coleta':
            frequencias_validas_rotas1 = ['Segunda', 'Quarta', 'Sexta']
            frequencias_validas_rotas2 = ['Terça', 'Quinta', 'Sábado']

            if self.turno == 'Matutino' and self.frequencia in frequencias_validas_rotas1:
                if self.garagem == 'PA1':
                    return ['AD12', 'AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22', 'AD23', 'AD24', 'DD11']
                elif self.garagem == 'PA2':
                    return ['AD12', 'AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22']
                elif self.garagem == 'PA3':
                    return ['AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22', 'AD23', 'AD24']
                elif self.garagem == 'PA4':
                    return ['AD12', 'AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22', 'AD24']

            if self.turno == 'Matutino' and self.frequencia in frequencias_validas_rotas2:
                if self.garagem == 'PA1':
                    return ['AD12', 'AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22', 'AD23', 'AD24', 'DD11','BD12','BD13','BD14','BD15','BD16','BD17','BD19','BD21']
                elif self.garagem == 'PA2':
                    return ['AD12', 'AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22', 'AD24','BD12','BD13','BD14','BD15','BD16','BD17','BD18','BD19','BD20','BD21','BD22']
                elif self.garagem == 'PA3':
                    return ['AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22', 'AD23', 'AD24','BD13','BD14','BD16','BD17','BD18','BD19','BD20','BD21','BD22','BD23','BD24']
                elif self.garagem == 'PA4':
                    return ['AD13', 'AD14', 'AD15', 'AD16', 'AD17', 'AD18', 'AD19', 'AD20', 'AD21', 'AD22', 'AD24','BD12','BD13','BD14','BD15','BD16','BD17','BD18','BD19','BD20','BD21','BD22']

            elif self.turno == 'Noturno' and self.frequencia in frequencias_validas_rotas1:
                if self.garagem == 'PA1':
                    return ['AN09', 'AN10', 'DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06', 'DN07', 'DN08', 'AN20','BN20']
                elif self.garagem == 'PA2':
                    return ['AN07', 'AN08', 'AN09', 'AN10', 'AN11', 'DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06']
                elif self.garagem == 'PA3':
                    return ['DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06', 'DN07', 'DN08', 'DN09', 'DN10', 'DN11', 'DN12', 'AN15']
                elif self.garagem == 'PA4':
                    return ['AN07', 'AN08', 'AN09', 'AN10', 'AN11', 'DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06']

            elif self.turno == 'Noturno' and self.frequencia in frequencias_validas_rotas2:
                if self.garagem == 'PA1':
                    return ['BN09', 'BN10', 'DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06', 'DN07', 'DN08', 'BN20']
                elif self.garagem == 'PA2':
                    return ['BN07', 'BN08', 'BN09', 'BN10', 'BN11', 'DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06']
                elif self.garagem == 'PA3':
                    return ['DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06', 'DN07', 'DN08', 'DN09', 'DN10', 'DN11', 'DN12', 'BN15']
                elif self.garagem == 'PA4':
                    return ['BN07', 'BN08', 'BN09', 'BN10', 'BN11', 'DN01', 'DN02', 'DN03', 'DN04', 'DN05', 'DN06']
        return []
    
def rota_varricao(self):
    if self.tipo_servico == 'Varrição':
        self.setores = None
        self.coletores = None  # Limpa todos os coletores associados
        return []
    return []