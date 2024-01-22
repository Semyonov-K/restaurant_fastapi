from typing import Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from restaurant_app.models.restaurant_menu import MainMenu, SubMenu, Dish
from restaurant_app.schemas.restaurant import SubMenuCRU, DishCRU
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from http import HTTPStatus


async def create_entity(
        new: Union[SubMenuCRU, DishCRU],
        type_of_entity: str,
        id_sm: Optional[int],
        session: AsyncSession
) -> Union[MainMenu, SubMenu, Dish]:
    """Функция по созданию основного меню/подменю/блюда."""
    new = new.model_dump()
    if type_of_entity == 'menu':
        db = MainMenu(**new)
    elif type_of_entity == 'submenu':
        new['menu_id'] = id_sm
        db = SubMenu(**new)
    elif type_of_entity == 'dish':
        new['submenu_id'] = id_sm
        db = Dish(**new)
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Неверный тип данных!'
        )
    session.add(db)
    await session.commit()
    await session.refresh(db)
    return db


async def read_all_entity(
        type_of_entity: str,
        session: AsyncSession,
) -> Union[list[MainMenu], list[SubMenu], list[Dish]]:
    """Функция по get-получению всех меню/подменю/блюд."""
    if type_of_entity == 'menu':
        db = await session.execute(select(MainMenu))
    elif type_of_entity == 'submenu':
        db = await session.execute(select(SubMenu))
    elif type_of_entity == 'dish':
        db = await session.execute(select(Dish))
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Неверный тип данных!'
        )
    return db.scalars().all() 


async def get_entity_by_id(
        entity_id: int,
        type_of_entity: str,
        session: AsyncSession,
) -> Union[Optional[MainMenu], Optional[SubMenu], Optional[Dish]]:
    """Функция по get-получению меню/подменю/блюда по id."""
    if type_of_entity == 'menu':
        db = await session.execute(
            select(MainMenu).where(
                MainMenu.id == entity_id
            )
        )
    elif type_of_entity == 'submenu':
        db = await session.execute(
            select(SubMenu).where(
                SubMenu.id == entity_id
            )
        )
    elif type_of_entity == 'dish':
        db = await session.execute(
            select(Dish).where(
                Dish.id == entity_id
            )
        )
    db = db.scalars().first()
    return db


async def update_entity(
        db_entity: Union[MainMenu, SubMenu, Dish],
        entity_upd: Union[SubMenuCRU, DishCRU],
        session: AsyncSession,
) -> MainMenu:
    """Функция по patch-обновлению меню/подменю/блюда."""
    obj_data = jsonable_encoder(db_entity)
    update_data = entity_upd.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_entity, field, update_data[field])
    session.add(db_entity)
    await session.commit()
    await session.refresh(db_entity)
    return db_entity


async def delete_entity(
        db: Union[MainMenu, SubMenu, Dish],
        session: AsyncSession,
) -> MainMenu:
    """Функция по удалению меню/подменю/блюда."""
    await session.delete(db)
    await session.commit()
    return db
