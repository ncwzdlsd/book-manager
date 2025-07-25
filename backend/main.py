from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import LoginRequest, BookCreate, NoticeCreate
from database import execute_single_query, execute_query, execute_update
from typing import Optional
from datetime import date, datetime
import json

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なドメインを設定すべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login(request: LoginRequest):
    try:
        # 役割に基づいてクエリするテーブルを選択
        table = request.role
        if table not in ['staff', 'reader']:
            raise HTTPException(status_code=400, detail="Invalid role")
        
        # ユーザーをクエリ
        query = f"SELECT * FROM {table} WHERE username = %s AND password = %s"
        user = execute_single_query(query, (request.username, request.password))
        
        if user:
            # パスワードフィールドを削除
            user.pop('password', None)
            
            # 簡単なトークンを生成（実際のアプリケーションではJWTを使用すべき）
            token = f"{request.role}_{user['id']}"
            
            return {
                "success": True,
                "message": "ログインに成功しました",
                "user": {**user, "role": request.role},
                "token": token
            }
        else:
            return {
                "success": False,
                "message": "ユーザー名またはパスワードが間違っています"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reservations")
async def get_reservations(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    date: Optional[str] = None
):
    try:
        # クエリ条件を構築
        conditions = []
        params = []
        
        if status:
            conditions.append("r.status = %s")
            params.append(status)
        
        if date:
            conditions.append("r.date = %s")
            params.append(date)
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # オフセットを計算
        offset = (page - 1) * size
        
        # 総数をクエリ
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM reservation r 
            LEFT JOIN reader rd ON r.reader_id = rd.id 
            LEFT JOIN book b ON r.book_id = b.id
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # データをクエリ
        query = f"""
            SELECT r.*, rd.name as reader_name, b.title as book_title
            FROM reservation r 
            LEFT JOIN reader rd ON r.reader_id = rd.id 
            LEFT JOIN book b ON r.book_id = b.id
            {where_clause}
            ORDER BY r.date DESC, r.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        reservations = execute_query(query, params)
        
        return {
            "success": True,
            "data": reservations,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/reservations/{reservation_id}/process")
async def process_reservation(reservation_id: int):
    try:
        # 予約状態を処理済みに更新
        query = "UPDATE reservation SET status = '処理済み' WHERE id = %s"
        result = execute_update(query, (reservation_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "予約は処理済みとしてマークされました"
            }
        else:
            return {
                "success": False,
                "message": "予約が存在しません"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int):
    try:
        # 予約記録を削除
        query = "DELETE FROM reservation WHERE id = %s"
        result = execute_update(query, (reservation_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "予約削除に成功しました"
            }
        else:
            return {
                "success": False,
                "message": "予約が存在しません"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/borrows")
async def get_borrows(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    lend_date: Optional[str] = None,
    due_date: Optional[str] = None
):
    try:
        # クエリ条件を構築
        conditions = []
        params = []
        
        if status:
            if status == "返却済み":
                conditions.append("l.return_date IS NOT NULL")
            elif status == "貸出中":
                conditions.append("l.return_date IS NULL AND l.due_date >= CURDATE()")
            elif status == "延滞":
                conditions.append("l.return_date IS NULL AND l.due_date < CURDATE()")
        
        if lend_date:
            conditions.append("l.lend_date = %s")
            params.append(lend_date)
        
        if due_date:
            conditions.append("l.due_date = %s")
            params.append(due_date)
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # オフセットを計算
        offset = (page - 1) * size
        
        # 総数をクエリ
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM lend l 
            LEFT JOIN reader rd ON l.reader_id = rd.id 
            LEFT JOIN book b ON l.book_id = b.id
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # データをクエリ
        query = f"""
            SELECT l.*, rd.name as reader_name, b.title as book_title
            FROM lend l 
            LEFT JOIN reader rd ON l.reader_id = rd.id 
            LEFT JOIN book b ON l.book_id = b.id
            {where_clause}
            ORDER BY l.lend_date DESC, l.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        borrows = execute_query(query, params)
        
        return {
            "success": True,
            "data": borrows,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/borrows/{borrow_id}")
async def delete_borrow(borrow_id: int):
    try:
        # 貸出記録を削除
        query = "DELETE FROM lend WHERE id = %s"
        result = execute_update(query, (borrow_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "貸出記録削除に成功しました"
            }
        else:
            return {
                "success": False,
                "message": "貸出記録が存在しません"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books")
async def get_books(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    title: Optional[str] = None,
    author: Optional[str] = None,
    publisher: Optional[str] = None
):
    try:
        # クエリ条件を構築
        conditions = []
        params = []
        
        if title:
            conditions.append("title LIKE %s")
            params.append(f"%{title}%")
        
        if author:
            conditions.append("author LIKE %s")
            params.append(f"%{author}%")
        
        if publisher:
            conditions.append("publisher LIKE %s")
            params.append(f"%{publisher}%")
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # オフセットを計算
        offset = (page - 1) * size
        
        # 総数をクエリ
        count_query = f"SELECT COUNT(*) as total FROM book{where_clause}"
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # データをクエリ
        query = f"""
            SELECT * FROM book{where_clause}
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        books = execute_query(query, params)
        
        return {
            "success": True,
            "data": books,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/books")
async def create_book(book: BookCreate):
    try:
        query = """
            INSERT INTO book (title, author, publisher, isbn, stock) 
            VALUES (%s, %s, %s, %s, %s)
        """
        result = execute_update(query, (
            book.title,
            book.author,
            book.publisher,
            book.isbn,
            book.stock
        ))
        
        if result > 0:
            return {
                "success": True,
                "message": "図書作成に成功しました",
                "id": result
            }
        else:
            return {
                "success": False,
                "message": "図書作成に失敗しました"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookCreate):
    try:
        query = """
            UPDATE book 
            SET title = %s, author = %s, publisher = %s, isbn = %s, stock = %s 
            WHERE id = %s
        """
        result = execute_update(query, (
            book.title,
            book.author,
            book.publisher,
            book.isbn,
            book.stock,
            book_id
        ))
        
        if result > 0:
            return {
                "success": True,
                "message": "図書更新に成功しました"
            }
        else:
            return {
                "success": False,
                "message": "図書が存在しません"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    try:
        # 删除图书记录
        query = "DELETE FROM book WHERE id = %s"
        result = execute_update(query, (book_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "図書削除に成功しました"
            }
        else:
            return {
                "success": False,
                "message": "図書が存在しません"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notices")
async def get_notices(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    content: Optional[str] = None,
    send_date: Optional[str] = None
):
    try:
        # 构建查询条件
        conditions = []
        params = []
        
        if content:
            conditions.append("n.content LIKE %s")
            params.append(f"%{content}%")
        
        if send_date:
            conditions.append("DATE(n.send_date) = %s")
            params.append(send_date)
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM notice n 
            LEFT JOIN staff s ON n.staff_id = s.id 
            LEFT JOIN reader r ON n.reader_id = r.id
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # 查询数据
        query = f"""
            SELECT n.*, s.name as staff_name, r.name as reader_name
            FROM notice n 
            LEFT JOIN staff s ON n.staff_id = s.id 
            LEFT JOIN reader r ON n.reader_id = r.id
            {where_clause}
            ORDER BY n.send_date DESC, n.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        notices = execute_query(query, params)
        
        return {
            "success": True,
            "data": notices,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notices")
async def create_notice(notice: NoticeCreate):
    try:
        query = """
            INSERT INTO notice (staff_id, reader_id, content, send_date) 
            VALUES (%s, %s, %s, NOW())
        """
        result = execute_update(query, (
            notice.staff_id,
            notice.reader_id,
            notice.content
        ))
        
        if result > 0:
            return {
                "success": True,
                "message": "通知送信に成功しました",
                "id": result
            }
        else:
            return {
                "success": False,
                "message": "通知送信に失敗しました"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/notices/{notice_id}")
async def delete_notice(notice_id: int):
    try:
        # 删除通知记录
        query = "DELETE FROM notice WHERE id = %s"
        result = execute_update(query, (notice_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "通知削除に成功しました"
            }
        else:
            return {
                "success": False,
                "message": "通知が存在しません"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions")
async def get_suggestions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    content: Optional[str] = None,
    comment_date: Optional[str] = None
):
    try:
        # 构建查询条件
        conditions = []
        params = []
        
        if content:
            conditions.append("c.content LIKE %s")
            params.append(f"%{content}%")
        
        if comment_date:
            conditions.append("c.comment_date = %s")
            params.append(comment_date)
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM `comment` c 
            LEFT JOIN reader r ON c.reader_id = r.id
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # 查询数据
        query = f"""
            SELECT c.*, r.name as reader_name
            FROM `comment` c 
            LEFT JOIN reader r ON c.reader_id = r.id
            {where_clause}
            ORDER BY c.comment_date DESC, c.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        suggestions = execute_query(query, params)
        
        return {
            "success": True,
            "data": suggestions,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/suggestions/{suggestion_id}")
async def delete_suggestion(suggestion_id: int):
    try:
        # 删除建议记录
        query = "DELETE FROM `comment` WHERE id = %s"
        result = execute_update(query, (suggestion_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "提案削除に成功しました"
            }
        else:
            return {
                "success": False,
                "message": "提案が存在しません"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 读者端API
@app.get("/reader/reservations")
async def get_reader_reservations(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    reader_id: int = Query(...),
    status: Optional[str] = None,
    date: Optional[str] = None
):
    try:
        # 构建查询条件
        conditions = ["r.reader_id = %s"]
        params = [reader_id]
        
        if status:
            conditions.append("r.status = %s")
            params.append(status)
        
        if date:
            conditions.append("r.date = %s")
            params.append(date)
        
        where_clause = " WHERE " + " AND ".join(conditions)
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM reservation r 
            LEFT JOIN book b ON r.book_id = b.id
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # 查询数据
        query = f"""
            SELECT r.*, b.title as book_title
            FROM reservation r 
            LEFT JOIN book b ON r.book_id = b.id
            {where_clause}
            ORDER BY r.date DESC, r.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        reservations = execute_query(query, params)
        
        return {
            "success": True,
            "data": reservations,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reader/reservations/{reservation_id}")
async def delete_reader_reservation(reservation_id: int):
    try:
        # 检查预约状态，只有待处理的预约才能取消
        check_query = "SELECT status FROM reservation WHERE id = %s"
        reservation = execute_single_query(check_query, (reservation_id,))
        
        if not reservation:
            return {
                "success": False,
                "message": "予約が存在しません"
            }
        
        if reservation['status'] != '処理待ち':
            return {
                "success": False,
                "message": "処理待ちの予約のみキャンセルできます"
            }
        
        # 更新预约状态为已取消
        query = "UPDATE reservation SET status = 'キャンセル済み' WHERE id = %s"
        result = execute_update(query, (reservation_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "予約キャンセルに成功しました"
            }
        else:
            return {
                "success": False,
                "message": "予約キャンセルに失敗しました"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reader/borrows")
async def get_reader_borrows(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    reader_id: int = Query(...),
    status: Optional[str] = None,
    lend_date: Optional[str] = None,
    due_date: Optional[str] = None
):
    try:
        # 构建查询条件
        conditions = ["l.reader_id = %s"]
        params = [reader_id]
        
        if status:
            if status == "返却済み":
                conditions.append("l.return_date IS NOT NULL")
            elif status == "貸出中":
                conditions.append("l.return_date IS NULL AND l.due_date >= CURDATE()")
            elif status == "延滞":
                conditions.append("l.return_date IS NULL AND l.due_date < CURDATE()")
        
        if lend_date:
            conditions.append("l.lend_date = %s")
            params.append(lend_date)
        
        if due_date:
            conditions.append("l.due_date = %s")
            params.append(due_date)
        
        where_clause = " WHERE " + " AND ".join(conditions)
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM lend l 
            LEFT JOIN book b ON l.book_id = b.id
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # 查询数据
        query = f"""
            SELECT l.*, b.title as book_title
            FROM lend l 
            LEFT JOIN book b ON l.book_id = b.id
            {where_clause}
            ORDER BY l.lend_date DESC, l.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        borrows = execute_query(query, params)
        
        return {
            "success": True,
            "data": borrows,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/reader/borrows/{borrow_id}/return")
async def return_book(borrow_id: int):
    try:
        # 检查借阅记录是否存在且未归还
        check_query = "SELECT return_date FROM lend WHERE id = %s"
        borrow = execute_single_query(check_query, (borrow_id,))
        
        if not borrow:
            return {
                "success": False,
                "message": "貸出記録が存在しません"
            }
        
        if borrow['return_date']:
            return {
                "success": False,
                "message": "この図書は既に返却されています"
            }
        
        # 更新归还日期
        query = "UPDATE lend SET return_date = NOW() WHERE id = %s"
        result = execute_update(query, (borrow_id,))
        
        # 检查更新是否成功（result > 0 表示有行被更新）
        if result > 0:
            return {
                "success": True,
                "message": "返却に成功しました"
            }
        else:
            return {
                "success": False,
                "message": "返却に失敗しました"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reader/books")
async def get_reader_books(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    reader_id: int = Query(...),
    title: Optional[str] = None,
    author: Optional[str] = None,
    publisher: Optional[str] = None
):
    try:
        # 构建查询条件
        conditions = []
        params = []
        
        if title:
            conditions.append("b.title LIKE %s")
            params.append(f"%{title}%")
        
        if author:
            conditions.append("b.author LIKE %s")
            params.append(f"%{author}%")
        
        if publisher:
            conditions.append("b.publisher LIKE %s")
            params.append(f"%{publisher}%")
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        count_query = f"SELECT COUNT(*) as total FROM book b{where_clause}"
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # 查询图书数据，彻底避免重复
        query = f"""
            SELECT b.*, 
                   r.id as reservation_id,
                   l.id as borrow_id,
                   CASE 
                       WHEN l.id IS NOT NULL THEN '貸出中'
                       WHEN r.id IS NOT NULL THEN '予約済み'
                       ELSE NULL
                   END as my_status
            FROM book b
            LEFT JOIN (
                SELECT book_id, MIN(id) AS id FROM reservation WHERE reader_id = %s AND status = '待处理' GROUP BY book_id
            ) r1 ON b.id = r1.book_id
            LEFT JOIN reservation r ON r.id = r1.id
            LEFT JOIN (
                SELECT book_id, MIN(id) AS id FROM lend WHERE reader_id = %s AND return_date IS NULL GROUP BY book_id
            ) l1 ON b.id = l1.book_id
            LEFT JOIN lend l ON l.id = l1.id
            {where_clause}
            ORDER BY b.id DESC
            LIMIT %s OFFSET %s
        """
        params = [reader_id, reader_id] + params + [size, offset]
        
        books = execute_query(query, params)
        
        return {
            "success": True,
            "data": books,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reader/reservations")
async def create_reader_reservation(request: dict):
    try:
        reader_id = request.get('reader_id')
        book_id = request.get('book_id')
        date = request.get('date')
        
        if not all([reader_id, book_id, date]):
            return {
                "success": False,
                "message": "必要なパラメータが不足しています"
            }
        
        # 检查是否已有未处理的预约
        check_query = "SELECT id FROM reservation WHERE reader_id = %s AND book_id = %s AND status = '処理待ち'"
        existing = execute_single_query(check_query, (reader_id, book_id))
        
        if existing:
            return {
                "success": False,
                "message": "この図書の未処理予約が既にあります"
            }
        
        # 检查是否正在借阅
        borrow_check = "SELECT id FROM lend WHERE reader_id = %s AND book_id = %s AND return_date IS NULL"
        borrowing = execute_single_query(borrow_check, (reader_id, book_id))
        
        if borrowing:
            return {
                "success": False,
                "message": "この図書を貸出中です。予約できません"
            }
        
        # 创建预约记录
        query = "INSERT INTO reservation (reader_id, book_id, date, status) VALUES (%s, %s, %s, '処理待ち')"
        result = execute_update(query, (reader_id, book_id, date))
        
        if result > 0:
            return {
                "success": True,
                "message": "予約に成功しました",
                "id": result
            }
        else:
            return {
                "success": False,
                "message": "予約に失敗しました"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reader/borrows")
async def create_reader_borrow(request: dict):
    try:
        reader_id = request.get('reader_id')
        book_id = request.get('book_id')
        days = request.get('days', 14)
        
        if not all([reader_id, book_id]):
            return {
                "success": False,
                "message": "必要なパラメータが不足しています"
            }
        
        # 检查图书库存
        book_query = "SELECT stock FROM book WHERE id = %s"
        book = execute_single_query(book_query, (book_id,))
        
        if not book:
            return {
                "success": False,
                "message": "図書が存在しません"
            }
        
        if book['stock'] <= 0:
            return {
                "success": False,
                "message": "図書の在庫が不足しています"
            }
        
        # 检查是否正在借阅
        borrow_check = "SELECT id FROM lend WHERE reader_id = %s AND book_id = %s AND return_date IS NULL"
        borrowing = execute_single_query(borrow_check, (reader_id, book_id))
        
        if borrowing:
            return {
                "success": False,
                "message": "この図書を貸出中です"
            }
        
        # 创建借阅记录
        query = "INSERT INTO lend (reader_id, book_id, lend_date, due_date) VALUES (%s, %s, NOW(), DATE_ADD(NOW(), INTERVAL %s DAY))"
        result = execute_update(query, (reader_id, book_id, days))
        
        if result > 0:
            # 减少库存
            update_stock = "UPDATE book SET stock = stock - 1 WHERE id = %s"
            execute_update(update_stock, (book_id,))
            
            return {
                "success": True,
                "message": "貸出に成功しました",
                "id": result
            }
        else:
            return {
                "success": False,
                "message": "貸出に失敗しました"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reader/notices")
async def get_reader_notices(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    reader_id: int = Query(...),
    content: Optional[str] = None,
    send_date: Optional[str] = None
):
    try:
        # 构建查询条件
        conditions = ["n.reader_id = %s"]
        params = [reader_id]
        
        if content:
            conditions.append("n.content LIKE %s")
            params.append(f"%{content}%")
        
        if send_date:
            conditions.append("DATE(n.send_date) = %s")
            params.append(send_date)
        
        where_clause = " WHERE " + " AND ".join(conditions)
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM notice n 
            LEFT JOIN staff s ON n.staff_id = s.id
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # 查询数据
        query = f"""
            SELECT n.*, s.name as staff_name
            FROM notice n 
            LEFT JOIN staff s ON n.staff_id = s.id
            {where_clause}
            ORDER BY n.send_date DESC, n.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        notices = execute_query(query, params)
        
        return {
            "success": True,
            "data": notices,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reader/suggestions")
async def get_reader_suggestions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    reader_id: int = Query(...),
    content: Optional[str] = None,
    comment_date: Optional[str] = None
):
    try:
        # 构建查询条件
        conditions = ["c.reader_id = %s"]
        params = [reader_id]
        
        if content:
            conditions.append("c.content LIKE %s")
            params.append(f"%{content}%")
        
        if comment_date:
            conditions.append("DATE(c.comment_date) = %s")
            params.append(comment_date)
        
        where_clause = " WHERE " + " AND ".join(conditions)
        
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM `comment` c
            {where_clause}
        """
        total_result = execute_single_query(count_query, params)
        total = total_result['total'] if total_result else 0
        
        # 查询数据
        query = f"""
            SELECT c.*
            FROM `comment` c
            {where_clause}
            ORDER BY c.comment_date DESC, c.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([size, offset])
        
        suggestions = execute_query(query, params)
        
        return {
            "success": True,
            "data": suggestions,
            "total": total,
            "page": page,
            "size": size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reader/suggestions")
async def create_reader_suggestion(request: dict):
    try:
        reader_id = request.get('reader_id')
        content = request.get('content')
        
        if not all([reader_id, content]):
            return {
                "success": False,
                "message": "必要なパラメータが不足しています"
            }
        
        if len(content) < 10:
            return {
                "success": False,
                "message": "提案内容は少なくとも10文字である必要があります"
            }
        
        if len(content) > 500:
            return {
                "success": False,
                "message": "提案内容は500文字を超えることはできません"
            }
        
        # 创建建议记录
        query = "INSERT INTO `comment` (reader_id, content, comment_date) VALUES (%s, %s, NOW())"
        result = execute_update(query, (reader_id, content))
        
        if result > 0:
            return {
                "success": True,
                "message": "提案を提出しました",
                "id": result
            }
        else:
            return {
                "success": False,
                "message": "提案を提出できませんでした"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reader/suggestions/{suggestion_id}")
async def delete_reader_suggestion(suggestion_id: int):
    try:
        # 检查建议记录是否存在
        check_query = "SELECT id FROM `comment` WHERE id = %s"
        suggestion = execute_single_query(check_query, (suggestion_id,))
        
        if not suggestion:
            return {
                "success": False,
                "message": "提案が存在しません"
            }
        
        # 删除建议记录
        query = "DELETE FROM `comment` WHERE id = %s"
        result = execute_update(query, (suggestion_id,))
        
        if result > 0:
            return {
                "success": True,
                "message": "提案を削除しました"
            }
        else:
            return {
                "success": False,
                "message": "提案を削除できませんでした"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/readers")
async def get_readers():
    try:
        query = "SELECT id, name FROM reader ORDER BY name"
        readers = execute_query(query)
        
        return {
            "success": True,
            "data": readers
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 