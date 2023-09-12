from fastapi import Depends, HTTPException
from sqlalchemy import or_, asc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.DB.db import get_db
from src.DB.models import Contact
from src.schemas import ContactCreate, ContactUpdate


async def create_contact(body: ContactCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        contact = Contact(**body.dict())
        db.add(contact)
        await db.flush()
        await db.refresh(contact)
        return contact


async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_data = await db.get(Contact, contact_id)
    if contact_data is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    result = await db.execute(contact_data)
    return result.scalars().first()


async def get_contacts(limit: int, offset: int, db: AsyncSession = Depends(get_db), query: str = ""):
    contacts_data = select(Contact).offset(offset).limit(limit).order_by(asc(Contact.id))
    result = await db.execute(contacts_data)
    return result.scalars().all()


async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact_data = await db.get(Contact, contact_id)
    if contact_data is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    for field, value in body.dict(exclude_unset=True).items():
        setattr(contact_data, field, value)

    await db.commit()
    await db.refresh(contact_data)
    return contact_data


async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_data = await db.get(Contact, contact_id)
    if contact_data is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact_name = f"{contact_data.first_name} {contact_data.last_name}"

    await db.delete(contact_data)
    await db.commit()

    return {
        "message": f"Contact '{contact_name}' successfully deleted"}
