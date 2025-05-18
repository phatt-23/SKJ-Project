from dataclasses import dataclass
from typing import Optional, List
from django.db.models import QuerySet
from django.http import HttpRequest

# source: https://github.com/geordi/kelvin  api/views/default.py
@dataclass
class SearchParams:
    count: Optional[int] = None
    start: Optional[int] = None
    order_by: Optional[str] = None
    sort: str = "desc"

    @staticmethod
    def from_request(
        request: HttpRequest,
        max_count: int,
        allowed_order_by_columns: List[str],
        default_order_by: Optional[str],
    ) -> "SearchParams":
        count = max_count
        if "count" in request.GET:
            count = min(max_count, int(request.GET["count"]))

        start = None
        if "start" in request.GET:
            start = int(request.GET["start"])

        order_by = default_order_by
        if "order_by" in request.GET:
            order_req = request.GET["order_by"]
            if order_req in allowed_order_by_columns:
                order_by = order_req

        sort = "desc"
        if request.GET.get("sort") == "asc":
            sort = "asc"
        return SearchParams(count=count, start=start, order_by=order_by, sort=sort)

    def apply(self, query: QuerySet) -> QuerySet:
        if self.order_by is not None:
            if self.sort != "desc":
                order = (self.order_by, "id")
            else:
                order = (f"-{self.order_by}", "-id")

            query = query.order_by(*order)

        if self.start is not None:
            query = query[self.start :]

        if self.count is not None:
            query = query[: self.count]
        return query


