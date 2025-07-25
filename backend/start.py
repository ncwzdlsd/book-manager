#!/usr/bin/env python3
"""
図書管理システムバックエンド起動スクリプト
自動リロード機能をサポート
"""

import uvicorn

if __name__ == "__main__":
    print("図書管理システムバックエンドサービスを起動中...")
    print("サービスアドレス: http://localhost:8000")
    print("自動リロード: 有効")
    print("Ctrl+C でサービスを停止")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",  # インポート文字列を使用
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_dirs=["."],  # 現在のディレクトリの変更を監視
        log_level="info"
    ) 