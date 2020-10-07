from django.conf import settings
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from .models import BillingProfile,Card
# Create your views here.
import stripe

STRIPE_SECRET_KEY =getattr(settings,"STRIPE_SECRET_KEY","sk_test_51HXLE9CyPGKubfUmP2TC7PmSQ1eYZaVUVgJUX6R9ZSY6lpK3gcz8FQABEgZDwoe0fQgRIxMVQi70rfBXweABT1mG00NhQPfuLN")
STRIPE_PUB_KEY=getattr(settings,"STRIPE_PUB_KEY","pk_test_51HXLE9CyPGKubfUmEwMsXYwSrgBZDNO79URLxZH2hFAxa2JqPaQaqBw7fxUwGK2xVKyMlv7Hpi3nex0HhukAFJEq0010Rw3H8y")

stripe.api_key =STRIPE_SECRET_KEY




def payment_method_view(request):
    #next_url = 
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})




def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        customer_id = billing_profile.customer_id
        if token is not None:
            card_response = stripe.Customer.create_source(
  						customer_id,
  						source=token,
				)
            new_card_obj = Card.objects.add_new(billing_profile, card_response)
            # new_card_obj = Card.objects.add_new(billing_profile, token)
            print(new_card_obj) # start saving our cards too!
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status_code=401)
