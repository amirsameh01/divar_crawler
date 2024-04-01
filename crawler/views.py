from django.http import JsonResponse
import json
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from crawler.crawl_view import PhoneNumScraper
from rest_framework.exceptions import ValidationError
from .models import PhoneNumbers

class SearchView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request):

        scraper = PhoneNumScraper()


        search_city = request.data.get('city')
        search_param = request.data.get('stext')
        search_count = request.data.get('scount')

        city_choices = [choice[0] for choice in PhoneNumbers._meta.get_field('city').choices]

        if search_city not in city_choices:
            raise ValidationError(f"Invalid city: {search_city}")



        #calling methods
        urls = scraper.get_urls(search_city, search_param, search_count)
        numbers, button_fails, num_fails = scraper.crawl_nums(urls)
        scraper.save_nums(numbers, search_city, search_param)
        
        return JsonResponse({'success': f"Crawled numbers: {len(numbers)}, button fails: {button_fails}, failed to crawl: {num_fails}"})



