from django.shortcuts import render, redirect
  
from django.contrib.messages.views import SuccessMessageMixin
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.views.generic import UpdateView, View
from django.http import HttpResponse
from django.conf import settings
from .utils import Mailchimp
from .mixins import CsrfExemptMixin
MAILCHIMP_EMAIL_LIST_ID     = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID', None)
# Create your views here.

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
	form_class = MarketingPreferenceForm
	template_name = 'base/forms.html'
	success_url = '/settings/email/'
	success_message = 'Your email preferences have been updated. Thank you.'
	def dispatch(self, *args, **kwargs):
		user = self.request.user
		if not user.is_authenticated():
			return redirect("/login/?next=/settings/email/") # HttpResponse("Not allowed", status=400)
		return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Email Preference'
		return context

	def get_object(self):
		user = self.request.user
		obj, created = MarketingPreference.objects.get_or_create(user=user)
		return obj


'''
data[email]:
saikiran@gmail.com
Copy Path
•
Copy Value
data[email_type]:
html
data[id]:
52cf3a6b66
data[ip_opt]:
106.66.44.240
data[list_id]:
edc5c939a7
data[merges][ADDRESS]:
data[merges][BIRTHDAY]:
data[merges][EMAIL]:
saikiran@gmail.com
data[merges][FNAME]:
data[merges][LNAME]:
data[merges][PHONE]:
data[web_id]:
121234
fired_at:
2020-10-03 07:30:44
type:
subscribe

'''
class MailchimpWebhookView(CsrfExemptMixin, View):
	# def get(self, request, *args, **kwargs):
	# 	return HttpResponse("Thank You", status=200)
	def post(self, request, *args, **kwargs):
		data = request.POST
		list_id = data.get('data[list_id]')
		if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
			hook_type = data.get('type')

			email = data.get('data[email]')
			response_status, response = Mailchimp().check_subcription_status(email)
			sub_status = response['status']
			is_subbed = None
			mailchimp_subbed = None
			if sub_status == 'subscribed':
				is_subbed, mailchimp_subbed = (True, True)
			elif sub_status == 'subscribed':
				is_subbed, mailchimp_subbed = (False, False)
			if is_subbed is not None and mailchimp_subbed is not None:
				qs = MarketingPreference.objects.filter(user__email__iexact=email)
				if qs.exists():
					qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
			
		return HttpResponse("Thank You", status=200)


# def mailchimp_webhook_view(request):
# 	data = request.POST
# 	list_id = data.get('data[list_id]')
# 	if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
# 		hook_type = data.get('type')

# 		email = data.get('data[email]')
# 		response_status, response = Mailchimp().check_subcription_status(email)
# 		sub_status = response['status']
# 		is_subbed = None
# 		mailchimp_subbed = None
# 		if sub_status == 'subscribed':
# 			is_subbed, mailchimp_subbed = (True, True)
# 		elif sub_status == 'subscribed':
# 			is_subbed, mailchimp_subbed = (False, False)
# 		if is_subbed is not None and mailchimp_subbed is not None:
# 			qs = MarketingPreference.objects.filter(user__email__iexact=email)
# 			if qs.exists():
# 				qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
		
# 	return HttpResponse("Thank You", status=200)