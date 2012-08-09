# -*- coding: utf-8 -*-
"""
SQLAlchemy-powered model definitions for repoze.what SQL plugin.
Sets up Users, Groups and Permissions
"""

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, Boolean
from sqlalchemy.orm import relation
from datafinder.model.meta import metadata, Base
import os
from hashlib import sha1

__all__ = ['Datasets']


class SourceInfo(Base):
    """
    Table to store the source registration information 
    """

    __tablename__ = 'SourceInfo'

    # columns
    id = Column(Integer, autoincrement=True, primary_key=True)
    silo = Column(Unicode(50),nullable=False)
    title = Column(Unicode(75),nullable=False)
    description = Column(Unicode(255))
    notes = Column(Unicode(255))
    administrators = Column(Unicode(255))
    managers = Column(Unicode(255))
    users = Column(Unicode(255))
    disk_allocation = Column(Integer(10))
    activate = Column(Boolean)

