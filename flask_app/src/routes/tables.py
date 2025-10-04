from flask import Blueprint, jsonify, request
from ..models.table import TableModel
from ..utils import token_required


bp = Blueprint('tables', __name__, url_prefix='/api/tables')


@bp.route('', methods=['GET'])
@token_required
def list_tables():
tables = TableModel.list_tables()
return jsonify({'tables': tables, 'total': len(tables)})


@bp.route('/<int:table_id>', methods=['GET'])
@token_required
def get_table(table_id):
t = TableModel.get_table(table_id)
if not t:
return jsonify({'message': 'Table not found'}), 404
return jsonify(t)


@bp.route('/<int:table_id>/status', methods=['PUT'])
@token_required
def update_status(table_id):
data = request.json or {}
status = data.get('status')
detected_by = data.get('detected_by', 'manual')
confidence = float(data.get('confidence_score', 1.0))
notes = data.get('notes')
if status not in ('empty','occupied','reserved','cleaning'):
return jsonify({'message': 'Invalid status'}), 400
TableModel.update_status(table_id, status, detected_by, confidence, notes)
return jsonify({'message': 'Status updated'})


@bp.route('', methods=['POST'])
@token_required
def create_table():
data = request.json or {}
table_number = data.get('table_number')
capacity = int(data.get('capacity', 4))
x = float(data.get('x_position', 0))
y = float(data.get('y_position', 0))
if not table_number:
return jsonify({'message': 'table_number required'}), 400
tid = TableModel.create_table(table_number, capacity, x, y)
return jsonify({'id': tid}), 201


@bp.route('/<int:table_id>/history', methods=['GET'])
@token_required
def history(table_id):
limit = int(request.args.get('limit', 10))
db = __import__('..database', fromlist=['get_db']).database.get_db()
with db.cursor() as cur:
cur.execute('SELECT * FROM table_status WHERE table_id=%s ORDER BY created_at DESC LIMIT %s', (table_id, limit))
rows = cur.fetchall()
return jsonify({'history': rows})