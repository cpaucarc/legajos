from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def datatable_page(queryset, request):
    """
    Returns queryset paginated with datatables parameters

    :param queryset: Queryset to paginate
    :param request: Django HTTP request containing datatables parameters: `length`, `start` and `draw`.
          `length`: Number of records that the table can display in the current draw.
           `start`: This is the start point in the current data set 0-indexed.
            `draw`: Draw counter. This is used by DataTables to ensure that the Ajax returns from
             server-side processing
                    requests are drawn in sequence by DataTables.
    :return:
        `draw`: The draw counter that this object is a response to - from the draw parameter.
        `page`: Page with resulting paginated objects from queryset.
    :rtype: Tuple
    """
    try:
        length = int(request.GET.get('length', 10))
    except ValueError:
        length = 10
    paginator = Paginator(queryset, length)
    try:
        start = int(request.GET.get('start', 0))
    except ValueError:
        start = 0
    page = (start // length) + 1
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    try:
        draw = int(request.GET.get('draw', 0))
    except ValueError:
        draw = 0
    return draw, page
