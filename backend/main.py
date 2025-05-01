import uvicorn
import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True) 