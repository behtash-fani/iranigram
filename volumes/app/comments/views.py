# from django.views import View
# from .forms import CommentForm
# from django.shortcuts import render, redirect
# from django.contrib import messages
from .models import Comment, Response
from django.http import JsonResponse


def submit_comment(request):
    phone = request.GET.get('phone_number')
    name = request.GET.get('name')
    content = request.GET.get('content')
    page_id = request.GET.get('page_id')

    try:
        # Create a new comment
        comment = Comment.objects.create(
            phone_number=phone,
            name=name,
            content=content,
            page_id=page_id,
            status='not approved',
        )

        # Return a success response with comment details
        response_data = {
            'success': True,
            'message': 'Comment submitted successfully',
            'comment_id': comment.id,
        }

    except Exception as e:
        # Return an error response if there is an exception
        response_data = {
            'success': False,
            'message': f'Error submitting comment: {str(e)}',
        }

    return JsonResponse(response_data)

def submit_response(request):
    phone = request.GET.get('phone_number')
    comment_id = request.GET.get('comment_id')
    name = request.GET.get('name')
    content = request.GET.get('content')

    try:
        # Create a new response
        comment = Comment.objects.get(id=comment_id)
        response = Response.objects.create(
            comment=comment,
            phone_number=phone,
            name=name,
            content=content,
            status='not approved',
        )

        # Return a success response with comment details
        response_data = {
            'success': True,
            'message': 'Response submitted successfully',
            'response_id': response.id,
        }

    except Exception as e:
        # Return an error response if there is an exception
        response_data = {
            'success': False,
            'message': f'Error submitting comment: {str(e)}',
        }
    return JsonResponse(response_data)




# class SubmitComment(View):
#     template_name = 'comments/list.html'
#     form_class = CommentForm

#     def get(self, request, *args, **kwargs):
#         comment_form = self.form_class()
#         comments = Comment.objects.all()
#         context = {
#             'comment_form': comment_form,
#             'comments': comments
#             }
#         return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     ticket_form = self.form_class(request.POST, request.FILES)
    #     if ticket_form.is_valid():
    #         ticket = ticket_form.save(commit=False)
    #         ticket.user = request.user
    #         ticket.status = 'submitted'
    #         ticket.save()
    #         ticketCode = str(ticket.id)
    #         phone_number = request.user.phone_number
    #         messages.success(request, _('Your support ticket was submitted successfully.'), 'success')
    #         return redirect('accounts:ticket_detail', ticket.id)
    #     else:
    #         context = {'ticket_form': ticket_form}
    #         return render(request, self.template_name, context)