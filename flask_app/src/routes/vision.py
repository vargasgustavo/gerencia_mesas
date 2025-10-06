from flask import Blueprint, jsonify, request, Response, current_app
from ..vision.table_detector import TableDetector
from ..utils import token_required


bp = Blueprint('vision', __name__, url_prefix='/api/vision')


# instantiate singleton detector (will be lazy)
_detector = TableDetector()


@bp.route('/start', methods=['POST'])
@token_required
def start_vision():
    _detector.start()
    return jsonify({'message': 'Sistema de visão iniciado com sucesso'})


@bp.route('/stop', methods=['POST'])
@token_required
def stop_vision():
    _detector.stop()
    return jsonify({'message': 'Sistema de visão parado'})


@bp.route('/status', methods=['GET'])
@token_required
def status():
    return jsonify({'is_running': _detector.running, 'camera_available': _detector.camera_available})


@bp.route('/results', methods=['GET'])
@token_required
def results():
    return jsonify({'results': _detector.get_results()})


@bp.route('/frame')
@token_required
def frame():
# MJPEG stream
    def gen():
        for frame in _detector.frame_generator():
            yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/regions', methods=['GET'])
@token_required
def regions():
    return jsonify({'regions': _detector.regions})


@bp.route('/regions', methods=['POST'])
@token_required
def add_region():
    data = request.json or {}
    _detector.add_or_update_region(data)
    return jsonify({'message': 'Region saved'})