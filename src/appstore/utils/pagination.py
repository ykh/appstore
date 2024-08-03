from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page_number'
    page_size_query_param = 'page_size'
    max_page_size = 100


def paginate_query(queryset, page_number, page_size):
    if not queryset.query.order_by:
        queryset = queryset.order_by('id')

    paginator = Paginator(queryset, page_size)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def paginate_response(data, paginated_result):
    class PaginatedResponse(serializers.Serializer):
        result = serializers.ListField()
        count = serializers.IntegerField()
        total_pages = serializers.IntegerField()
        current_page = serializers.IntegerField()
        page_size = serializers.IntegerField()

    params_trf = PaginatedResponse(
        data={
            'result': data,
            'count': paginated_result.paginator.count,
            'total_pages': paginated_result.paginator.num_pages,
            'current_page': paginated_result.number,
            'page_size': paginated_result.paginator.per_page,
        }
    )

    params_trf.is_valid()

    return params_trf.validated_data
