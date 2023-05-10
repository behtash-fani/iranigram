from django.views.generic import ListView
from .models import Transactions
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from common.mixins import LoginRequiredMixin


class TransactionsView(LoginRequiredMixin, ListView):
    model = Transactions
    template_name = 'transactions/transactions.html'
    context_object_name = 'Transactions'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Transactions.objects.filter(user=self.request.user).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')

        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)
        context['Transactions'] = transactions
        return context
