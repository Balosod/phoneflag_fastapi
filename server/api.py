from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .db import init_db
from server.routes.users import router as UserRouter
from server.routes.device import router as DeviceRouter
from server.routes.home_page import router as LandingPageRouter
from server.routes.explore import router as ExploreRouter
from server.routes.device_details import router as DetailsRouter
from server.routes.order import router as OrderRouter
from server.routes.review import router as ReviewRouter
from server.routes.rating import router as RatingRouter
from server.routes.reply import router as ReplyRouter
from server.routes.like import router as LikeRouter
from server.routes.admin import router as AdminRouter
from server.routes.tracking import router as TrackingRouter
from server.routes.insurance import router as InsuranceRouter
from server.routes.ads import router as AdsRouter


from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from .settings import CONFIG_SETTINGS
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@AuthJWT.load_config
def get_config():
    return CONFIG_SETTINGS

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(UserRouter, tags=["Users"], prefix="/users")
app.include_router(DeviceRouter, tags=["Device"], prefix="/device")
app.include_router(LandingPageRouter, tags=["Home Page"], prefix="/home")
app.include_router(ExploreRouter, tags=["Explore"], prefix="/explore")
app.include_router(DetailsRouter, tags=["Details"], prefix="/detail")
app.include_router(OrderRouter, tags=["Order"], prefix="/order")
app.include_router(ReviewRouter, tags=["Review"], prefix="/review")
app.include_router(RatingRouter, tags=["Rating"], prefix="/rating")
app.include_router(ReplyRouter, tags=["Reply"], prefix="/reply")
app.include_router(LikeRouter, tags=["Like"], prefix="/like")
app.include_router(AdminRouter, tags=["admin"], prefix="/admin")
app.include_router(TrackingRouter, tags=["tracking"], prefix="/track")
app.include_router(InsuranceRouter, tags=["insured"], prefix="/insured")
app.include_router(AdsRouter, tags=['ads'], prefix="/ads")



@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    
    return {"message": "Welcome to PhoneFlag"}




