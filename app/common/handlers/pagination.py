from django.core.paginator import Paginator, EmptyPage

class PaginationHandler:

    def __init__(self, page: int, limit: int, path: str = None, params = None):
        self.page = page
        self.limit = limit
        self.path = path
        self.params = params

    def build_url(self, page: int):
        parameters = {key: value for key, value in self.params.items()}
        parameters['page'] = str(page)

        parameter_string_list = [f"{key}={str(value)}" for key, value in parameters.items()]
        parameter_string = "&".join(parameter_string_list)

        url = f"{self.path}?{parameter_string}"
        return url

    def get_next_url(self, results: list, known_length: int=0):
        if not self.path:
            return ""

        if not known_length:
            try:
                result_length = results.count()
            except TypeError:
                result_length = len(results)
            except AttributeError:
                result_length = len(results)
        else:
            result_length = known_length

        if self.page == 1:
            next_pointer = self.limit
        else:
            next_pointer = (self.page * self.limit)

        if next_pointer < result_length:
            next_url = self.build_url(self.page + 1)
        else:
            next_url = ""

        return next_url

    def get_prev_url(self):
        if not self.path or self.page == 1:
            return ""

        current_records = self.page * self.limit
        prev_page_records = current_records - self.limit

        if prev_page_records > 0:
            prev_url = self.build_url(self.page - 1)
        else:
            prev_url = ""

        return prev_url

    def get_offset(self):
        if self.page <= 1:
            offset = 0
        else:
            offset = (self.page - 1) * self.limit
        return offset

    def get_paginated_results(self, results):
        if self.page <= 1:
            paginated_results = results[0:self.limit]
        else:
            offset = (self.page - 1) * self.limit
            paginated_results = results[offset:offset + self.limit]

        return paginated_results

    def get_pagination_data(self, results):
        data = dict(results=list(), next_url=str(), prev_url=str())

        paginator = Paginator(results, self.limit)
        try:
            _paginated = paginator.page(self.page)
        except EmptyPage as exception:
            return data

        data['results'] = _paginated.object_list
        if _paginated.has_next():
            data['next_url'] = self.get_next_url(results)

        if _paginated.has_previous():
            data['prev_url'] = self.get_prev_url()

        return data

