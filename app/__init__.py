from flask import Flask, jsonify
from .repositories.timer_repository import InMemoryTimerRepository
from .models.timer import Timer


import os
def create_app():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    timer_repository = InMemoryTimerRepository()
    default_timer = Timer()
    timer_repository.save("default", default_timer)
    
    from flask import render_template
    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/api/timer/start", methods=["POST"])
    def start_timer():
        timer = timer_repository.get("default")
        if timer and timer.start():
            timer_repository.save("default", timer)
            return jsonify({"status": "started"})
        return jsonify({"status": "error"}), 400
    
    @app.route("/api/timer/pause", methods=["POST"])
    def pause_timer():
        timer = timer_repository.get("default")
        if timer and timer.pause():
            timer_repository.save("default", timer)
            return jsonify({"status": "paused"})
        return jsonify({"status": "error"}), 400
    
    @app.route("/api/timer/reset", methods=["POST"])
    def reset_timer():
        timer = timer_repository.get("default")
        if timer and timer.reset():
            timer_repository.save("default", timer)
            return jsonify({"status": "reset"})
        return jsonify({"status": "error"}), 400
    
    @app.route("/api/timer/status", methods=["GET"])
    def get_timer_status():
        timer = timer_repository.get("default")
        if timer:
            return jsonify({
                "state": timer.state.value,
                "remainingTime": timer.remaining_time.total_seconds(),
                "completedSessions": timer.completed_sessions
            })
        return jsonify({"status": "error"}), 404
    
    return app
