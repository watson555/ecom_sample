from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
# from django.db.models import Q
# Create your views here.
class SearchProductView(ListView):
	# queryset = Product.objects.all()
	template_name = 'search/view.html'

	def get_context_data(self, *args, **kwargs):
		context = super(SearchProductView, self).get_context_data(*args, **kwargs)
		
		query = self.request.GET.get('q')
		context['query'] = query
		#S earchQuery.objects.create(query=query)
		return context
	
	def get_queryset(self, *args, **kwargs):
		request = self.request
		# print(request.GET)
		method_dict = request.GET
		query = method_dict.get('q', None)  #method_dict['q'] it gives error it the q is not their on search
		if query is not None:
			# lookups = Q(title__icontains=query)| Q(description__icontains=query)
			# return Product.objects.filter(lookups).distinct()
			return Product.objects.search(query)
		return Product.objects.featured()