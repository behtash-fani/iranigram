from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TicketForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Ticket, Response
from .forms import ResponseForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views import View
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .tasks import send_submit_ticket_sms_task
from common.mixins import LoginRequiredMixin



class SupportView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'support/support.html'
    context_object_name = 'Tickets'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Ticket.objects.filter(user=self.request.user).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)
        context['Tickets'] = tickets
        return context


class SubmitTicket(View):
    template_name = 'support/submit_ticket.html'
    form_class = TicketForm

    def get(self, request, *args, **kwargs):
        ticket_form = self.form_class()
        context = {'ticket_form': ticket_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        ticket_form = self.form_class(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.status = 'submitted'
            ticket.save()
            ticketCode = str(ticket.id)
            phone_number = request.user.phone_number
            send_submit_ticket_sms_task.delay(phone_number, ticketCode)
            messages.success(request, _('Your support ticket was submitted successfully.'), 'success')
            return redirect('accounts:ticket_detail', ticket.id)
        else:
            context = {'ticket_form': ticket_form}
            return render(request, self.template_name, context)


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    responses = Response.objects.filter(ticket=ticket).order_by('created_at')
    if request.method == 'POST':
        response_form = ResponseForm(request.POST, request.FILES)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.user = request.user
            response.ticket = ticket
            response.save()
            messages.success(request, _('Your reply was submitted successfully.'), 'success')
            return redirect('accounts:ticket_detail', ticket_id)
    else:
        response_form = ResponseForm()
    return render(request, 'support/ticket_detail.html',
                  {'ticket': ticket, 'responses': responses, 'response_form': response_form})


def download_file(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.file:
        response = HttpResponse(ticket.file, content_type='application/force-download')


@login_required
def admin_ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    responses = Response.objects.filter(ticket=ticket).order_by('created_at')
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.ticket = ticket
            response.save()
            return redirect('accounts:admin_ticket_detail', ticket.id)
    else:
        form = ResponseForm()
    return render(request, 'support/admin_ticket_detail.html',
                  {'ticket': ticket, 'responses': responses, 'form': form})
