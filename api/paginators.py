from rest_framework.pagination import PageNumberPagination


class FiftyResultsPaginator(PageNumberPagination):
    page_size = 50
    max_page_size = 50


class TwentyResultsPaginator(PageNumberPagination):
    page_size = 20
    max_page_size = 20
