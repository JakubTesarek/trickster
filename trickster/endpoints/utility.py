"""Utility API endpoints."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Blueprint, Response, jsonify, send_from_directory


endpoints = Blueprint('utility_api', __name__)

STATIC_ROOT = os.path.join(Path().resolve(strict=True), 'frontend/build')


@endpoints.route('/health', methods=['GET'])
def health() -> Response:
    """Returns internal app status."""
    return jsonify({'status': 'ok'})


@endpoints.route('/static', methods=['GET'])
def index() -> Response:
    """Returns internal app status."""
    return send_from_directory(STATIC_ROOT, 'index.html')


@endpoints.route('/static/<path:path>')
def serve_static_file(path):
    return send_from_directory(STATIC_ROOT, path)
