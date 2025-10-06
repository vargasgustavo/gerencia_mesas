from ..database import get_db


class TableModel:
    @staticmethod
    def list_tables():
        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT t.*, ts.status, ts.detected_by, ts.confidence_score, ts.created_at as status_updated_at FROM tables t LEFT JOIN (SELECT * FROM table_status WHERE id IN (SELECT MAX(id) FROM table_status GROUP BY table_id)) ts ON t.id = ts.table_id WHERE t.is_active=1")
        return cur.fetchall()


    @staticmethod
    def get_table(table_id):
        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT * FROM tables WHERE id=%s", (table_id,))
        return cur.fetchone()


    @staticmethod
    def update_status(table_id, status, detected_by='manual', confidence_score=1.0, notes=None):
        db = get_db()
        with db.cursor() as cur:
            cur.execute("INSERT INTO table_status (table_id, status, detected_by, confidence_score, notes) VALUES (%s,%s,%s,%s,%s)", (table_id, status, detected_by, confidence_score, notes))
        return cur.lastrowid


    @staticmethod
    def create_table(table_number, capacity=4, x=0, y=0):
        db = get_db()
        with db.cursor() as cur:
            cur.execute("INSERT INTO tables (table_number, capacity, x_position, y_position) VALUES (%s,%s,%s,%s)", (table_number, capacity, x, y))
        return cur.lastrowid