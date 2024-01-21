from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from restaurant_app.core.db import Base


class MainMenu(Base):
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=False)
    submenus = relationship("SubMenu")


class SubMenu(Base):
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=False)
    menu_id = Column(Integer, ForeignKey('mainmenu.id'))
    menu = relationship("MainMenu")
    dishes = relationship("Dish")


class Dish(Base):
    title = Column(String(), unique=True, nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(String(50), nullable=False)
    submenu_id = Column(Integer, ForeignKey('submenu.id'))
    submenu = relationship("SubMenu")
