from infrastructure.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM audit_logs"))
    logs = result.fetchall()
    
    if not logs:
        print("Kara kutu henüz boş, hiç log yok!")
    else:
        print("KARA KUTU KAYITLARI:")
        for log in logs:
            print(f"ID: {log[0]} | Görev: {log[1]} | İşlem: {log[3]} | Yapan: {log[4]}")