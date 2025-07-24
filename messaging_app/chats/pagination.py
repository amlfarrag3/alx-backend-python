from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # Number of messages per page
    page_size_query_param = 'page_size'  # Optional: allow client to set page size
    max_page_size = 100  # Optional: prevent abuse by limiting max size
