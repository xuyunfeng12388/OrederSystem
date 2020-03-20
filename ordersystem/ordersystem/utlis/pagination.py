from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 30


class OrderSystemStandardResultsSetPagination(StandardResultsSetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 30

    def get_paginated_response(self, data):
        """重写父类方法，自定义分页响应数据格式"""
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('results', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ])
