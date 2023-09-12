import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_, and_, extract, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.DB.models import Contact
from utils.CRUD import create_contact, get_contacts, get_contact, update_contact, delete_contact
from src.DB.db import get_db
from src.schemas import ContactCreate, ContactResponse, ContactUpdate

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", tags=["contacts"], response_model=list[ContactResponse])
async def get_contacts_db(limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await get_contacts(limit, offset, db)


@router.get("/{id}", tags=["contacts"], response_model=ContactResponse)
async def get_contact_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_contact(id, db)


@router.post("/", tags=["contacts"], response_model=ContactResponse)
async def create_new_contact(body: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await create_contact(body, db)


@router.put("/{id}", tags=["contacts"], response_model=ContactResponse)
async def update_contact_db(id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)):
    return await update_contact(id, body, db)


@router.delete("/{id}", tags=["contacts"])
async def delete_contact_db(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_contact(id, db)


