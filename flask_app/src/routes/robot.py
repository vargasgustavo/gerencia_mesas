from flask import Blueprint, jsonify, request
return jsonify({'message': 'Erro', 'error': msg}), 500


@bp.route('/clean', methods=['POST'])
@token_required
def clean():
    data = request.json or {}
    table_id = data.get('table_id')
    if table_id is None:
    return jsonify({'message': 'table_id required'}), 400
    ok, msg = _robot.send_clean(table_id)
    if ok:
    return jsonify({'message': 'Comando de limpeza enviado'})
    return jsonify({'message': 'Erro', 'error': msg}), 500


@bp.route('/check', methods=['POST'])
@token_required
def check():
    data = request.json or {}
    table_id = data.get('table_id')
    ok, msg = _robot.send_check(table_id)
    if ok:
    return jsonify({'message': 'Comando de verificação enviado'})
    return jsonify({'message': 'Erro', 'error': msg}), 500


@bp.route('/return', methods=['POST'])
@token_required
def retbase():
    ok, msg = _robot.send_return()
    if ok:
    return jsonify({'message': 'Robô retornando'})
    return jsonify({'message': 'Erro', 'error': msg}), 500


@bp.route('/stop', methods=['POST'])
@token_required
def stop():
ok, msg = _robot.send_stop()
if ok:
return jsonify({'message': 'Robô parado'})
return jsonify({'message': 'Erro', 'error': msg}), 500


@bp.route('/commands/history', methods=['GET'])
@token_required
def history():
limit = int(request.args.get('limit', 50))
db = __import__('..database', fromlist=['get_db']).database.get_db()
with db.cursor() as cur:
cur.execute('SELECT * FROM robot_commands ORDER BY sent_at DESC LIMIT %s', (limit,))
rows = cur.fetchall()
return jsonify({'history': rows})