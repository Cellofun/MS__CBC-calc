from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CompleteBloodCount (models.Model):
    MALE_CHOICE = 'male'
    FEMALE_CHOICE = 'female'

    SEX_CHOICES = (
        (MALE_CHOICE, 'Мужской'),
        (FEMALE_CHOICE, 'Женский')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пациент"
    )
    age = models.IntegerField(
        verbose_name="Возраст",
        null=True,
        blank=True
    )
    sex = models.CharField(
        verbose_name="Пол",
        max_length=50,
        choices=SEX_CHOICES,
        null=True,
        default=''
    )
    analysis_date = models.DateField(
        verbose_name="Дата анализа",
    )
    leukocyte = models.FloatField(
        verbose_name="Лейкоциты"
    )
    erythrocyte = models.FloatField(
        verbose_name="Эритроциты"
    )
    hemoglobin = models.IntegerField(
        verbose_name="Гемоглобин"
    )
    hematocrit = models.FloatField(
        verbose_name="Гематокрит"
    )
    sed_rate = models.IntegerField(
        verbose_name="СОЭ"
    )
    type = models.IntegerField()
    sum = models.FloatField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-analysis_date']
        verbose_name = "Общий анализ крови"
        verbose_name_plural = "Общий анализ крови"

    def __str__(self):
        return f"{self.user}: {self.analysis_date}"


class ThreeDiff (models.Model):
    RELATIVE_CHOICE = 'relative'
    ABSOLUTE_CHOICE = 'absolute'

    VALUE_CHOICES = (
        (RELATIVE_CHOICE, 'Относительное'),
        (ABSOLUTE_CHOICE, 'Абсолютное')
    )

    cbc = models.OneToOneField(
        CompleteBloodCount,
        on_delete=models.CASCADE,
        verbose_name="Общий анализ крови"
    )
    value_type = models.CharField(
        verbose_name="Тип значения результатов",
        max_length=50,
        choices=VALUE_CHOICES,
        default=VALUE_CHOICES[0][0]
    )
    neutrophil = models.FloatField(
        verbose_name="Нейтрофилы"
    )
    lymphocyte = models.FloatField(
        verbose_name="Лимфоциты"
    )
    monocyte = models.FloatField(
        verbose_name="Моноциты"
    )

    class Meta:
        verbose_name = "Лейкоцитарная формула класса 3-диф"
        verbose_name_plural = "Лейкоцитарная формула класса 3-диф"

    def __str__(self):
        return f"{self.cbc.user}: {self.cbc.analysis_date}"


class FiveDiff (models.Model):
    RELATIVE_CHOICE = 'relative'
    ABSOLUTE_CHOICE = 'absolute'

    VALUE_CHOICES = (
        (RELATIVE_CHOICE, 'Относительное'),
        (ABSOLUTE_CHOICE, 'Абсолютное')
    )

    cbc = models.OneToOneField(
        CompleteBloodCount,
        on_delete=models.CASCADE,
        verbose_name="Общий анализ крови"
    )
    value_type = models.CharField(
        verbose_name="Тип значения результатов",
        max_length=50,
        choices=VALUE_CHOICES,
        default=VALUE_CHOICES[0][0]
    )
    neutrophil = models.FloatField(
        verbose_name="Нейтрофилы"
    )
    lymphocyte = models.FloatField(
        verbose_name="Лимфоциты"
    )
    monocyte = models.FloatField(
        verbose_name="Моноциты"
    )
    eosinophil = models.FloatField(
        verbose_name="Эозинофилы"
    )
    basophil = models.FloatField(
        verbose_name="Базофилы"
    )

    class Meta:
        verbose_name = "Лейкоцитарная формула класса 5-диф"
        verbose_name_plural = "Лейкоцитарная формула класса 5-диф"

    def __str__(self):
        return f"{self.cbc.user}: {self.cbc.analysis_date}"


class BloodSmear (models.Model):
    RELATIVE_CHOICE = 'relative'
    ABSOLUTE_CHOICE = 'absolute'

    VALUE_CHOICES = (
        (RELATIVE_CHOICE, 'Относительное'),
        (ABSOLUTE_CHOICE, 'Абсолютное')
    )

    cbc = models.OneToOneField(
        CompleteBloodCount,
        on_delete=models.CASCADE,
        verbose_name="Общий анализ крови"
    )
    value_type = models.CharField(
        verbose_name="Тип значения результатов",
        max_length=50,
        choices=VALUE_CHOICES,
        default=VALUE_CHOICES[0][0]
    )
    promyelocyte = models.FloatField(
        verbose_name="Промиелоциты"
    )
    myelocyte = models.FloatField(
        verbose_name="Миелоциты"
    )
    metamyelocyte = models.FloatField(
        verbose_name="Метамиелоциты"
    )
    banded_neutrophil = models.FloatField(
        verbose_name="Палочкоядерные нейтрофилы"
    )
    segmented_neutrophil = models.FloatField(
        verbose_name="Сегментоядерные нейтрофилы"
    )
    lymphocyte = models.FloatField(
        verbose_name="Лимфоциты"
    )
    monocyte = models.FloatField(
        verbose_name="Моноциты"
    )
    eosinophil = models.FloatField(
        verbose_name="Эозинофилы"
    )
    basophil = models.FloatField(
        verbose_name="Базофилы"
    )
    plasma_cell = models.FloatField(
        verbose_name="Плазмациты"
    )

    def intoxicationKK(self):
        if self.value_type == "relative":
            return round(
                (4 * self.myelocyte + 3 * self.metamyelocyte + 2 * self.banded_neutrophil + self.segmented_neutrophil) *
                (self.plasma_cell + 1) / ((self.monocyte + self.lymphocyte) * (self.eosinophil + 1)),
                2
            )

        myel = self.myelocyte * 100 / self.cbc.leukocyte
        meta = self.metamyelocyte * 100 / self.cbc.leukocyte
        bn = self.banded_neutrophil * 100 / self.cbc.leukocyte
        sn = self.segmented_neutrophil * 100 / self.cbc.leukocyte
        plasm = self.plasma_cell * 100 / self.cbc.leukocyte
        mono = self.monocyte * 100 / self.cbc.leukocyte
        lymph = self.lymphocyte * 100 / self.cbc.leukocyte
        eo = self.eosinophil * 100 / self.cbc.leukocyte

        return round((4 * myel + 3 * meta + 2 * bn + sn) *(plasm + 1) / ((mono + lymph) * (eo + 1)), 2)

    def intoxicationO(self):
        if self.value_type == "relative":
            return round(
                (self.segmented_neutrophil + self.banded_neutrophil + self.metamyelocyte + self.myelocyte + self.plasma_cell) /
                (self.monocyte + self.lymphocyte + self.plasma_cell),
                2
            )

        sn = self.segmented_neutrophil * 100 / self.cbc.leukocyte
        bn = self.banded_neutrophil * 100 / self.cbc.leukocyte
        meta = self.metamyelocyte * 100 / self.cbc.leukocyte
        myel = self.myelocyte * 100 / self.cbc.leukocyte
        plasm = self.plasma_cell * 100 / self.cbc.leukocyte
        mono = self.monocyte * 100 / self.cbc.leukocyte
        lymph = self.lymphocyte * 100 / self.cbc.leukocyte

        return round((sn + bn + meta + myel + plasm) / (mono + lymph + plasm), 2)

    def nuclear(self):
        if self.value_type == "relative":
            return round(
                (self.monocyte + self.metamyelocyte + self.banded_neutrophil) / self.segmented_neutrophil,
                2
            )

        mono = self.monocyte * 100 / self.cbc.leukocyte
        meta = self.metamyelocyte * 100 / self.cbc.leukocyte
        sn = self.segmented_neutrophil * 100 / self.cbc.leukocyte
        bn = self.banded_neutrophil * 100 / self.cbc.leukocyte

        return round((mono + meta + bn) / sn, 2)

    def shift(self):
        if self.value_type == "relative":
            return round(
                (self.segmented_neutrophil + self.banded_neutrophil) / self.lymphocyte,
                2
            )

        sn = self.segmented_neutrophil * 100 / self.cbc.leukocyte
        bn = self.banded_neutrophil * 100 / self.cbc.leukocyte
        lymph = self.lymphocyte * 100 / self.cbc.leukocyte

        return round((sn + bn) / lymph, 2)

    def allergy(self):
        if self.value_type == "relative":
            return round(
                (self.lymphocyte + 10 * (self.eosinophil + 1)) /
                (self.banded_neutrophil + self.segmented_neutrophil + self.monocyte + self.basophil),
                2
            )

        lymph = self.lymphocyte * 100 / self.cbc.leukocyte
        eo = self.eosinophil * 100 / self.cbc.leukocyte
        bn = self.banded_neutrophil * 100 / self.cbc.leukocyte
        sn = self.segmented_neutrophil * 100 / self.cbc.leukocyte
        mono = self.monocyte * 100 / self.cbc.leukocyte
        baso = self.basophil * 100 / self.cbc.leukocyte

        return round((lymph + 10 * (eo + 1)) / (bn + sn + mono + baso), 2)

    class Meta:
        ordering = ['-cbc__analysis_date']
        verbose_name = "Микроскопия мазка крови"
        verbose_name_plural = "Микроскопия мазка крови"

    def __str__(self):
        return f"{self.cbc.user}: {self.cbc.analysis_date}"
