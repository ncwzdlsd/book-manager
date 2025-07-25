from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class StaffBase(BaseModel):
    username: str
    name: Optional[str] = None
    contact: Optional[str] = None

class StaffCreate(StaffBase):
    password: str

class Staff(StaffBase):
    id: int
    
    class Config:
        from_attributes = True

class ReaderBase(BaseModel):
    username: str
    name: Optional[str] = None
    contact: Optional[str] = None
    level: Optional[str] = "一般会員"

class ReaderCreate(ReaderBase):
    password: str

class Reader(ReaderBase):
    id: int
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class ReservationBase(BaseModel):
    reader_id: int
    book_id: int
    date: date
    status: Optional[str] = "処理待ち"

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    reader_name: Optional[str] = None
    book_title: Optional[str] = None
    
    class Config:
        from_attributes = True

class BorrowBase(BaseModel):
    reader_id: int
    book_id: int
    lend_date: date
    due_date: date
    return_date: Optional[date] = None

class BorrowCreate(BorrowBase):
    pass

class Borrow(BorrowBase):
    id: int
    reader_name: Optional[str] = None
    book_title: Optional[str] = None
    
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    isbn: Optional[str] = None
    stock: int = 0

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        from_attributes = True

class NoticeBase(BaseModel):
    staff_id: int
    reader_id: int
    content: str
    send_date: Optional[datetime] = None

class NoticeCreate(NoticeBase):
    pass

class Notice(NoticeBase):
    id: int
    staff_name: Optional[str] = None
    reader_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class SuggestionBase(BaseModel):
    reader_id: int
    content: str
    comment_date: Optional[date] = None

class SuggestionCreate(SuggestionBase):
    pass

class Suggestion(SuggestionBase):
    id: int
    reader_name: Optional[str] = None
    
    class Config:
        from_attributes = True 