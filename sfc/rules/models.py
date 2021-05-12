# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MinValueValidator
from django.db import models


class Rule(models.Model):
    class Meta:
        unique_together = (('station', 'route', 'material_group'))

    station = models.ForeignKey('line.Station', on_delete=models.CASCADE)
    material_group = models.CharField(max_length=255)
    route = models.ForeignKey('line.Route', on_delete=models.CASCADE)

    TYPE_CHOICES = (
        ('CSERIALNO', 'CSERIALNO'),
        ('CUSTPARTNO', 'CUSTPARTNO'),
        ('HHPNCSERIALNO', 'HHPNCSERIALNO'),
        ('OFFLINE', 'OFFLINE'))
    scan_type = models.CharField(max_length=30, null=False, blank=False, default="CSERIALNO")

    TYPE_CHOICES = (
        ('CSERIALNO', 'CSERIALNO'),
        ('CUSTPARTNO', 'CUSTPARTNO'),
        ('HHPNCSERIALNO', 'HHPNCSERIALNO'),
        ('OFFLINE', 'OFFLINE'))

    scan_type = models.CharField(max_length=30, null=False, blank=False, default="CSERIALNO")

    def __str__(self):
        return 'Route: ' + self.route.__str__() + ' Material Group: ' + self.material_group

# class RuleSet(models.Model):
#     # id
#     route = models.ForeignKey('line.Route', on_delete=models.CASCADE, unique=True)

#     def __str__(self):
#         return self.route.__str__()


