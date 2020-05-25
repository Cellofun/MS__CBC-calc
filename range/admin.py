from django.contrib import admin

from .models import CBCRange, DiffRange, IndexRange, ReferenceRange


class CBCAdmin(admin.ModelAdmin):
    fields = (
        ('age_min', 'age_max'),
        'sex',
        ('leukocyte_min', 'leukocyte_max'),
        ('erythrocyte_min', 'erythrocyte_max'),
        ('hemoglobin_min', 'hemoglobin_max'),
        ('hematocrit_min', 'hematocrit_max'),
        ('sed_rate_min', 'sed_rate_max')
    )


class FormulaAdmin(admin.ModelAdmin):
    fields = (
        ('age_min', 'age_max'),
        'value_type',
        ('promyelocyte_min', 'promyelocyte_max'),
        ('myelocyte_min', 'myelocyte_max'),
        ('metamyelocyte_min', 'metamyelocyte_max'),
        ('neutrophil_min', 'neutrophil_max'),
        ('banded_neutrophil_min', 'banded_neutrophil_max'),
        ('segmented_neutrophil_min', 'segmented_neutrophil_max'),
        ('lymphocyte_min', 'lymphocyte_max'),
        ('monocyte_min', 'monocyte_max'),
        ('eosinophil_min', 'eosinophil_max'),
        ('basophil_min', 'basophil_max'),
        ('plasma_cell_min', 'plasma_cell_max')
    )


class IndexAdmin(admin.ModelAdmin):
    fields = (
        ('intoxicationKK_min', 'intoxicationKK_max'),
        ('intoxicationO_min', 'intoxicationO_max'),
        ('nuclear_min', 'nuclear_max'),
        ('shift_min', 'shift_max'),
        ('allergy_min', 'allergy_max')
    )


admin.site.register(ReferenceRange)
admin.site.register(CBCRange, CBCAdmin)
admin.site.register(DiffRange, FormulaAdmin)
admin.site.register(IndexRange, IndexAdmin)
