"""Database models."""
# from . import db
from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, DateTime, Float, Text
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
    start_time: Mapped[DateTime] = mapped_column(DateTime, index=False, unique=False, nullable=True)
    release_date: Mapped[DateTime] = mapped_column(DateTime, index=False, unique=False, nullable=True)
    reviews: Mapped[List["ProductReview"]] = relationship(
        back_populates="product")
    prices: Mapped[List["ProductPrice"]] = relationship(
        back_populates="product")
    enabled: Mapped[int] = mapped_column(Integer)
    rating: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f'<Product {self.stylecolor}, {self.rating}>'


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


class ProductCrawlRecord(Base):
    """Data model for crawl record."""

    __tablename__ = 'product_crawl_record'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer)
    stylecolor: Mapped[str] = mapped_column(String(100))
    platform: Mapped[str] = mapped_column(String(100))
    crawl_time: Mapped[DateTime] = mapped_column(DateTime)

    def __repr__(self):
        return f'<ProductCrawlRecord {self.product_id}, {self.stylecolor}, {self.platform}, {self.crawl_time}>'


class ProductPrice(Base):
    """Data model for product prices."""

    __tablename__ = 'product_prices'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="prices")
    price: Mapped[float] = mapped_column(Float)
    retailprice: Mapped[float] = mapped_column(Float)
    lastsaleprice: Mapped[float] = mapped_column(Float)
    stockxlowestprice: Mapped[float] = mapped_column(Float)
    stockxhighestprice: Mapped[float] = mapped_column(Float)
    check_date: Mapped[DateTime] = mapped_column(DateTime)

    def __repr__(self):
        return f'<ProductPrice {self.product_id}, {self.price}, {self.lastsaleprice}, {self.check_date}>'
