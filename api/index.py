"""
Vercel entrypoint for MyanTone AI.

Vercel sends /api/* requests to this function.
The existing backend keeps its normal FastAPI routes:
 /translate
 /translate-all
 /health
 /analyze
 ...
"""

from pathlib import Path
import importlib.util

from fastapi import FastAPI


ROOT = Path(__file__).resolve().parents[1]
BACKEND_FILE = ROOT / "api.py"


spec = importlib.util.spec_from_file_location(
    "myantone_backend",
    BACKEND_FILE,
)

if spec is None or spec.loader is None:
    raise RuntimeError(
        f"Unable to load backend: {BACKEND_FILE}"
    )


backend_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_module)

backend_app = backend_module.app


app = FastAPI(
    title="MyanTone AI API",
)

app.mount("/api", backend_app)