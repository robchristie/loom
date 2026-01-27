#!/usr/bin/env bash

uv run uvicorn sdlc.server:app --reload --port 54321 --host 0.0.0.0
