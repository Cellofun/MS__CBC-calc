from django.db import models


class CBCRange(models.Model):
    MALE_CHOICE = 'male'
    FEMALE_CHOICE = 'female'

    SEX_CHOICES = (
        (MALE_CHOICE, 'Мужской'),
        (FEMALE_CHOICE, 'Женский')
    )

    sex = models.CharField(
        verbose_name="Пол",
        max_length=50,
        choices=SEX_CHOICES,
        null=True,
        default=''
    )
    age_min = models.IntegerField(
        verbose_name="Возраст"
    )
    age_max = models.IntegerField(
        verbose_name=""
    )
    leukocyte_min = models.FloatField(
        verbose_name="Лейкоциты"
    )
    leukocyte_max = models.FloatField(
        verbose_name=""
    )
    erythrocyte_min = models.FloatField(
        verbose_name="Эритроциты"
    )
    erythrocyte_max = models.FloatField(
        verbose_name=""
    )
    hemoglobin_min = models.IntegerField(
        verbose_name="Гемоглобин"
    )
    hemoglobin_max = models.IntegerField(
        verbose_name=""
    )
    hematocrit_min = models.FloatField(
        verbose_name="Гематокрит"
    )
    hematocrit_max = models.FloatField(
        verbose_name=""
    )
    sed_rate_min = models.IntegerField(
        verbose_name="СОЭ"
    )
    sed_rate_max = models.IntegerField(
        verbose_name=""
    )

    class Meta:
        unique_together = ('sex', 'age_min', 'age_max')
        verbose_name = "Общий анализ крови"
        verbose_name_plural = "Общий анализ крови"

    def __str__(self):
        return f"{self.sex}: {self.age_min} - {self.age_max}"


class DiffRange(models.Model):
    RELATIVE_CHOICE = 'relative'
    ABSOLUTE_CHOICE = 'absolute'

    VALUE_CHOICES = (
        (RELATIVE_CHOICE, 'Относительное'),
        (ABSOLUTE_CHOICE, 'Абсолютное')
    )

    age_min = models.CharField(
        verbose_name="Возраст",
        max_length=20
    )
    age_max = models.CharField(
        verbose_name="",
        max_length=20
    )
    value_type = models.CharField(
        verbose_name="Тип значения результатов",
        max_length=50,
        choices=VALUE_CHOICES,
        default=VALUE_CHOICES[0][0]
    )
    promyelocyte_min = models.FloatField(
        verbose_name="Промиелоциты"
    )
    promyelocyte_max = models.FloatField(
        verbose_name=""
    )
    myelocyte_min = models.FloatField(
        verbose_name="Миелоциты"
    )
    myelocyte_max = models.FloatField(
        verbose_name=""
    )
    metamyelocyte_min = models.FloatField(
        verbose_name="Метамиелоциты"
    )
    metamyelocyte_max = models.FloatField(
        verbose_name=""
    )
    neutrophil_min = models.FloatField(
        verbose_name="Нейтрофилы"
    )
    neutrophil_max = models.FloatField(
        verbose_name=""
    )
    banded_neutrophil_min = models.FloatField(
        verbose_name="Палочкоядерные нейтрофилы"
    )
    banded_neutrophil_max = models.FloatField(
        verbose_name=""
    )
    segmented_neutrophil_min = models.FloatField(
        verbose_name="Сегментоядерные нейтрофилы"
    )
    segmented_neutrophil_max = models.FloatField(
        verbose_name=""
    )
    lymphocyte_min = models.FloatField(
        verbose_name="Лимфоциты"
    )
    lymphocyte_max = models.FloatField(
        verbose_name=""
    )
    monocyte_min = models.FloatField(
        verbose_name="Моноциты"
    )
    monocyte_max = models.FloatField(
        verbose_name=""
    )
    eosinophil_min = models.FloatField(
        verbose_name="Эозинофилы"
    )
    eosinophil_max = models.FloatField(
        verbose_name=""
    )
    basophil_min = models.FloatField(
        verbose_name="Базофилы"
    )
    basophil_max = models.FloatField(
        verbose_name=""
    )
    plasma_cell_min = models.FloatField(
        verbose_name="Плазмациты"
    )
    plasma_cell_max = models.FloatField(
        verbose_name=""
    )

    class Meta:
        unique_together = ('age_min', 'age_max', 'value_type')
        verbose_name = "Лейкоцитарная формула"
        verbose_name_plural = "Лейкоцитарная формула"

    def __str__(self):
        return f"{self.age_min} - {self.age_max} ({self.value_type})"


class IndexRange(models.Model):
    intoxicationKK_min = models.FloatField(
        verbose_name="Лейкоцитарный индекс интоксикации Я.Я. Кальф-Калифа"
    )
    intoxicationO_max = models.FloatField(
        verbose_name=""
    )
    intoxicationO_min = models.FloatField(
        verbose_name="Лейкоцитарный индекс интоксикации В. К. Островского"
    )
    intoxicationKK_max = models.FloatField(
        verbose_name=""
    )
    nuclear_min = models.FloatField(
        verbose_name="Ядерный индекс степени эндотоксикоза Г.Д. Даштаянца"
    )
    nuclear_max = models.FloatField(
        verbose_name=""
    )
    shift_min = models.FloatField(
        verbose_name="Индекс сдвига лейкоцитов Н. И. Ябучинского"
    )
    shift_max = models.FloatField(
        verbose_name=""
    )
    allergy_min = models.FloatField(
        verbose_name="Индекс аллергизации"
    )
    allergy_max = models.FloatField(
        verbose_name=""
    )

    def __str__(self):
        return "Индексы"

    class Meta:
        verbose_name = "Лейкоцитарные индексы"
        verbose_name_plural = "Лейкоцитарные индексы"


class ReferenceRange(models.Model):
    cbc = models.ForeignKey(
        CBCRange,
        on_delete=models.CASCADE,
        verbose_name="Общий анализ крови"
    )
    diff = models.ForeignKey(
        DiffRange,
        on_delete=models.CASCADE,
        verbose_name="Лейкоцитарная формула"
    )

    class Meta:
        unique_together = ('cbc', 'diff')
        verbose_name = "Референтные значения"
        verbose_name_plural = "Референтные значения"

    def __str__(self):
        return f"{self.cbc.sex}: {self.cbc.age_min} - {self.cbc.age_max} ({self.diff.value_type})"
