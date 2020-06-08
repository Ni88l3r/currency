import csv

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, View

from rate.models import Rate
from rate.selectors import get_latest_rates
from rate.utils import display

import xlsxwriter


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'rates-list.html'


class LatestRateList(TemplateView):
    template_name = 'latest-rates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = get_latest_rates()
        return context


class RateDownloadCSV(View):
    HEADERS = (
        'id',
        'created',
        'source',
        'amount',
        'type',
    )
    queryset = Rate.objects.all().iterator()

    @property
    def prepare_response(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        return response

    def get(self, request):
        response = self.prepare_response
        writer = csv.writer(response)
        writer.writerow(self.__class__.HEADERS)
        for rate in self.queryset:
            values = []
            for attr in self.__class__.HEADERS:
                values.append(display(rate, attr))
            writer.writerow(values)
        return response


class RateDownloadXLSX(View):
    HEADERS = (
        'id',
        'created',
        'source',
        'amount',
        'type',
    )
    queryset = Rate.objects.all().iterator()

    @property
    def prepare_response(self):
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename="rates.xlsx"'
        return response

    def get(self, request):
        response = self.prepare_response
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        for col, data in enumerate(self.__class__.HEADERS):
            worksheet.write(0, col, data)
        for col, rate in enumerate(self.queryset, start=1):
            values = []
            for attr in self.__class__.HEADERS:
                values.append(display(rate, attr))
            for row, value in enumerate(values):
                worksheet.write(col, row, value)
        workbook.close()
        return response
