"""Database models."""
# from . import db
from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """Base class"""
    pass


class Product(Base):
    """Data model for product."""

    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylecolor: Mapped[str] = mapped_column(String(100), index=False,
                                            unique=True,
                                            nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=False,
                                      unique=False,
                                      nullable=True)
    description: Mapped[str] = mapped_column(String(100), index=False,
                                             unique=False,
                                             nullable=True)
    price: Mapped[float] = mapped_column(Float, index=False,
                                         unique=False,
                                         nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, index=False,
                                                 unique=False,
                                                 nullable=True)
    reviews: Mapped[List["ProductReview"]] = relationship(
        back_populates="product")
    enabled: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f'<Product {self.stylecolor}>'


class ProductReview(Base):
    """Data model for product review."""

    __tablename__ = 'product_reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="reviews")
    source: Mapped[str] = mapped_column(String(100))
    account_id: Mapped[str] = mapped_column(String(100))
    account_name: Mapped[str] = mapped_column(String(100))
    review_user_id: Mapped[str] = mapped_column(String(100))
    review_user_name: Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[DateTime] = mapped_column(DateTime)
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    like_count: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String(1024))

    def __repr__(self):
        return f'<ProductReview {self.product}, {self.account_id}, {self.source}>'
