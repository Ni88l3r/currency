from django.shortcuts import render

from rate.models import Rate


def show(request):
    params = ['created', 'amount', 'source', 'currency_type', 'type']
    rates = Rate.objects.all()
    for param in params:
        value = request.GET.get(param)
        if value:
            rates = rates.filter(**{param: value})
    context = {'rates': rates}
    return render(request, 'rates-show.html', context=context)
