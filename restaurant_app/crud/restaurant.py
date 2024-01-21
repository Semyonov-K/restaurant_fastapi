from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from restaurant_app.core.db import AsyncSessionLocal
from restaurant_app.models.restaurant_menu import MainMenu
from restaurant_app.schemas.restaurant import MenuCreate
from fastapi.encoders import jsonable_encoder


async def create_menu(
        new_menu: MenuCreate,
        session: AsyncSession
) -> MainMenu:
    """Функция по созданию основного меню."""
    new_menu_data = new_menu.model_dump()
    db_mainmenu = MainMenu(**new_menu_data)
    session.add(db_mainmenu)
    await session.commit()
    await session.refresh(db_mainmenu)
    return db_mainmenu


async def read_all_menus(
        session: AsyncSession,
) -> list[MainMenu]:
    db_menus = await session.execute(select(MainMenu))
    return db_menus.scalars().all() 


async def get_menu_by_id(
        menu_id: int,
        session: AsyncSession,
) -> Optional[MainMenu]:
    db_menu = await session.execute(
        select(MainMenu).where(
            MainMenu.id == menu_id
        )
    )
    db_menu = db_menu.scalars().first()
    return db_menu


async def update_menu(
        db_menu: MainMenu,
        menu_upd: MenuCreate,
        session: AsyncSession,
) -> MainMenu:
    obj_data = jsonable_encoder(db_menu)
    update_data = menu_upd.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_menu, field, update_data[field])
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


async def delete_menu(
        db_menu: MainMenu,
        session: AsyncSession,
) -> MainMenu:
    await session.delete(db_menu)
    await session.commit()
    return db_menu
