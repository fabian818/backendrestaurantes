from rest_framework.pagination import PageNumberPagination


class FiftyResultsPaginator(PageNumberPagination):
    page_size = 50
    max_page_size = 50
