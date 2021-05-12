from rest_framework import serializers
from django.apps import apps

Bom = apps.get_model('manufacturing', 'Bom')

class BomSerializer(serializers.HyperlinkedModelSerializer):
    part_no = serializers.CharField(source='bom_component')
    part_name = serializers.CharField(source='component_material_description')
    qty = serializers.IntegerField(source='component_quantity')
    class Meta:
        model = Bom
        fields = (
            'part_no',
            'part_name',
            'qty',
            'installation_point'
        )
