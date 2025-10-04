from ..database import get_db
from ..utils import hash_password


class AuthModel:
@staticmethod
def create_user(username, email, password):
db = get_db()
with db.cursor() as cur:
pw_hash = hash_password(password)
sql = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
cur.execute(sql, (username, email, pw_hash))
return cur.lastrowid


@staticmethod
def find_by_username(username):
db = get_db()
with db.cursor() as cur:
cur.execute("SELECT * FROM users WHERE username=%s", (username,))
return cur.fetchone()


@staticmethod
def find_by_id(user_id):
db = get_db()
with db.cursor() as cur:
cur.execute("SELECT id, username, email, is_active, created_at FROM users WHERE id=%s", (user_id,))
return cur.fetchone()