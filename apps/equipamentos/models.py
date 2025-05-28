from django.core.exceptions import ValidationError
from django.db import models

IMPLEMENTOS = [
    ('Retroescavadeira', 'Retroescavadeira'),
    ('Caminhão Carroceiria', 'Caminhão Carroceiria'),
    ('Pá Carregadeira', 'Pá Carregadeira'),
]

STATUS_EQUIPAMENTO = [
    ('Ativo', 'Ativo'),
    ('Inativo', 'Inativo')
]

MOTIVO_INATIVIDADE = [
    ('Em garagem', 'Em garagem'),
    ('Manutenção', 'Manutenção')
]


class Equipamento(models.Model):
    prefixo_equipamento = models.CharField(max_length=20)
    implemento = models.CharField(max_length=20, choices=IMPLEMENTOS)
    status_equipamento = models.CharField(max_length=7, choices=STATUS_EQUIPAMENTO)
    motivo_inatividade = models.CharField(
        max_length=20,
        choices=MOTIVO_INATIVIDADE,
        blank=True,
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['prefixo_equipamento']),
            models.Index(fields=['implemento']),
        ]

    def clean(self):
        if self.status_equipamento == 'Inativo' and not self.motivo_inatividade:
            raise ValidationError("Motivo da inatividade deve ser informado quando o equipamento está inativo.")
        if self.status_equipamento == 'Ativo' and self.motivo_inatividade:
            raise ValidationError("Equipamento ativo não deve ter motivo de inatividade.")

    def __str__(self):
        return f"{self.prefixo_equipamento} - {self.implemento} ({self.status_equipamento})"
