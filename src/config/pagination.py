from math import ceil
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page.paginator.count,
            "pages": ceil(self.page.paginator.count / self.page_size),
            "current_page": self.page.number,
            'results': data,
        })