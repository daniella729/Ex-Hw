from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends

from solution.api.dependencies import (
    get_report_service,
    raise_bad_request,
)
from solution.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])

ReportServiceDep = Annotated[
    ReportService,
    Depends(get_report_service),
]


@router.get("/spending-by-category", response_model=list)
async def get_spending_breakdown_by_category(
    month: int,
    year: int,
    service: ReportServiceDep,
) -> list[dict[str, str | Decimal]]:
    try:
        return await service.get_spending_breakdown_by_category(
            month=month,
            year=year,
        )
    except ValueError as exception:
        raise_bad_request(str(exception))
