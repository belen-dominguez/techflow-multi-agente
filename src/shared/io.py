import json
from pathlib import Path


def save_results(results, root_dir: Path):
    """Guarda los resultados en outputs/test_results.json"""

    outputs_path = root_dir / "outputs"
    outputs_path.mkdir(exist_ok=True)

    results_file = outputs_path / "test_results.json"

    try:
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"[save_results] Error guardando resultados: {e}")