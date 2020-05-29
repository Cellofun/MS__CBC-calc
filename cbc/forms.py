from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from .models import CompleteBloodCount, ThreeDiff, FiveDiff, BloodSmear


class CBCModelForm(forms.ModelForm):
    class Meta:
        model = CompleteBloodCount
        exclude = [
            'user',
            'content_type',
            'object_id',
            'type'
        ]
        widgets = {
            'analysis_date': forms.DateInput(
                attrs={
                    'type': 'text',
                    'id': 'analysis_date',
                    'readonly': '',
                    'placeholder': ''
                }),
            'leukocyte': forms.NumberInput(),
            'erythrocyte': forms.NumberInput(),
            'hemoglobin': forms.NumberInput(),
            'hematocrit': forms.NumberInput(),
            'sed_rate': forms.NumberInput()
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CBCModelForm, self).__init__(*args, **kwargs)
        if self.user.is_authenticated:
            del self.fields['age']
            del self.fields['sex']
        self.label_suffix = ""

    def clean(self):
        date = self.cleaned_data.get('analysis_date')
        _sum = self.cleaned_data.get('sum')
        errors = {}

        if self.user.is_authenticated:
            if CompleteBloodCount.objects.filter(user=self.user, analysis_date=date).exists():
                date_formated = date.strftime('%d.%m.%Y')
                errors['analysis_date'] = ValidationError('Результаты анализа за %s уже добавлены.' % date_formated)

        if _sum < 98 or _sum > 102:
            errors['sum'] = ValidationError('Сумма компонентов лейкоцитарной формулы не равна 100%. Пожалуйста, '
                                             'проверьте введенные значения и повторите попытку')

        if errors:
            raise ValidationError(errors)

        return self.cleaned_data


ThreeDiffFormSet = inlineformset_factory(
    CompleteBloodCount,
    ThreeDiff,
    fields=[
        'value_type',
        'neutrophil',
        'lymphocyte',
        'monocyte'
    ],
    can_delete=False,
    extra=1,
    max_num=1
)


FiveDiffFormSet = inlineformset_factory(
    CompleteBloodCount,
    FiveDiff,
    fields=[
        'value_type',
        'neutrophil',
        'lymphocyte',
        'monocyte',
        'eosinophil',
        'basophil'
    ],
    can_delete=False,
    extra=1,
    max_num=1
)


BloodSmearFormSet = inlineformset_factory(
    CompleteBloodCount,
    BloodSmear,
    fields=[
        'value_type',
        'promyelocyte',
        'myelocyte',
        'metamyelocyte',
        'banded_neutrophil',
        'segmented_neutrophil',
        'lymphocyte',
        'monocyte',
        'eosinophil',
        'basophil',
        'plasma_cell'
    ],
    can_delete=False,
    extra=1,
    max_num=1
)
