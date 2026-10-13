#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

# Add the parent directory (anlp_project) to sys.path so chandohasam can be imported
# This works whether the app is run from a venv or directly from the system Python
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask, jsonify, render_template, request
from meter_engine.chandohasam import analyze

import dawg_demo

app = Flask(__name__)

PROFILES = ["strict", "relaxed", "historical"]
KANDAM_EXAMPLE = (
    "పలికెడిది భాగవత మఁట,\n"
    "పలికించెడివాడు రామభద్రుం డఁట, నేఁ\n"
    "బలికిన భవహర మగునఁట,\n"
    "పలికెద, వేఱొండు గాథ బలుకఁగ నేలా?"
)


@app.route("/", methods=["GET", "POST"])
def index():
    poem_text = KANDAM_EXAMPLE if request.method == "GET" else request.form.get("poem", "")
    profile = request.form.get("profile", "strict")
    if profile not in PROFILES:
        profile = "strict"

    analysis = None
    error = None

    if request.method == "POST":
        text = poem_text.strip()
        if not text:
            error = "Please paste a poem before analyzing."
        else:
            try:
                analysis = analyze(text, profile=profile)
            except Exception as exc:
                error = f"Could not analyze this text: {exc}"

    return render_template(
        "index.html",
        poem_text=poem_text,
        profile=profile,
        profiles=PROFILES,
        analysis=analysis,
        error=error,
        example=KANDAM_EXAMPLE,
    )


@app.route("/dawg", methods=["GET", "POST"])
def dawg_page():
    """Akshara-by-akshara walk of a poem through the metre DAWG (three.js)."""
    poem_text = (request.values.get("poem") or "").strip() or KANDAM_EXAMPLE
    version = "v2" if request.values.get("version") == "v2" else "v1"
    return render_template("dawg_demo.html", poem_text=poem_text, version=version, examples=dawg_demo.EXAMPLES)


@app.route("/api/dawg/graph")
def dawg_graph():
    return jsonify(dawg_demo.graph_payload())


@app.route("/api/dawg/trace", methods=["POST"])
def dawg_trace():
    body = request.get_json(silent=True) or {}
    text = (body.get("poem") or "").strip()
    version = "v2" if body.get("version") == "v2" else "v1"
    if not text:
        return jsonify({"error": "Please paste a poem first."}), 400
    try:
        return jsonify(dawg_demo.trace_payload(text, version))
    except Exception as exc:
        return jsonify({"error": f"Could not trace this text: {exc}"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
