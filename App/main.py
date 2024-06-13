from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, engine
from .models import Base
from .schemas import ConfigurationCreate, ConfigurationUpdate, Configuration
from .crud import create_configuration, get_configuration, update_configuration, delete_configuration

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/create_configuration", response_model=Configuration)
async def create_config(configuration: ConfigurationCreate, db: AsyncSession = Depends(get_db)):
    return await create_configuration(db, configuration)

@app.get("/get_configuration/{country_code}", response_model=Configuration)
async def read_config(country_code: str, db: AsyncSession = Depends(get_db)):
    db_config = await get_configuration(db, country_code)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_config

@app.post("/update_configuration/{country_code}", response_model=Configuration)
async def update_config(country_code: str, configuration: ConfigurationUpdate, db: AsyncSession = Depends(get_db)):
    db_config = await update_configuration(db, country_code, configuration)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_config

@app.delete("/delete_configuration/{country_code}")
async def delete_config(country_code: str, db: AsyncSession = Depends(get_db)):
    success = await delete_configuration(db, country_code)
    if not success:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"message": "Configuration deleted successfully"}
