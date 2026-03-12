from fastapi import FastAPI
from solution.api.routers import categories_router,accounts_routers,transactions_router,transfer_router,report_router
app= FastAPI()
app.include_router(accounts_routers.router)
app.include_router(categories_router.router)
app.include_router(transactions_router.router)
app.include_router(transfer_router.router)
app.include_router(report_router.router)
@app.get("/")
async def root()->dict[str,str]:
    return{"message":"API is running"}
