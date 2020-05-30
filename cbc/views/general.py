from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView

from cbc.models import CompleteBloodCount, BloodSmear, FiveDiff, ThreeDiff
from range.models import CBCRange, IndexRange


class CBCListView(ListView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_list.html'

    def get_context_data(self, **kwargs):
        context = super(CBCListView, self).get_context_data(**kwargs)
        context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=self.request.user)
        return context

    def get_queryset(self):
        return CompleteBloodCount.objects.filter(user=self.request.user)


class CBCDeleteView(DeleteView):
    template_name = 'cbc/cbc_delete.html'
    success_url = reverse_lazy('cbc:cbc-list')

    def get_object(self, **kwargs):
        id_ = self.kwargs.get('id')
        return get_object_or_404(CompleteBloodCount, id=id_)

    def get_context_data(self, **kwargs):
        context = super(CBCDeleteView, self).get_context_data(**kwargs)
        context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=self.request.user)
        return context


class CommonChartsTemplateView(TemplateView):
    template_name = 'cbc/cbc_chart_common.html'

    def get_context_data(self, **kwargs):
        context = super(CommonChartsTemplateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['cbc'] = CompleteBloodCount.objects.filter(user=user)
        context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
        age = user.patient.get_age()
        context['range'] = CBCRange.objects.filter(
            sex=user.patient.sex,
            age_min__lt=age,
            age_max__gt=age
        ).first()
        return context


class IndexChartsTemplateView(TemplateView):
    template_name = 'cbc/cbc_chart_index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexChartsTemplateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['cbc'] = CompleteBloodCount.objects.filter(user=user)
        context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
        context['range'] = IndexRange.objects.filter().last()
        return context


class DiffChartsTemplateView(TemplateView):
    template_name = 'cbc/cbc_chart_diff.html'

    def get_context_data(self, **kwargs):
        context = super(DiffChartsTemplateView, self).get_context_data(**kwargs)
        user = self.request.user
        blood_smear = BloodSmear.objects.filter(cbc__user=user)
        context['cbc'] = CompleteBloodCount.objects.filter(user=user)
        context['three_dif'] = ThreeDiff.objects.filter(cbc__user=user)
        context['five_dif'] = FiveDiff.objects.filter(cbc__user=user)
        context['blood_smear'] = blood_smear
        context['blood_diagram'] = blood_smear
        return context


class HomeView(TemplateView):
    template_name = 'home/home.html'
