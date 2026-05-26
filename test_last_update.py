from dotenv import load_dotenv
load_dotenv()

from backend_api.main import app
from backend_api.src.services.forecast_services import get_station_data_by_id
from datetime import datetime, timezone

with app.app_context():
    data = get_station_data_by_id(2)
    print(f"last_update retornado: {data.get('last_update')}")
    print(f"timestamp: {data.get('timestamp')}")
    
    ts = datetime.fromisoformat(data['timestamp'])
    diff_seconds = (datetime.now(timezone.utc) - ts).total_seconds()
    diff_minutes = diff_seconds / 60
    print(f"\nDiferença em segundos: {diff_seconds:.0f}")
    print(f"Diferença em minutos: {diff_minutes:.1f}")
    print(f"\nThreshold frontend atual (5s):")
    print(f"  Seria online? {diff_seconds <= 5}")
    print(f"\nThreshold sugerido (5 minutos = 300s):")
    print(f"  Seria online? {diff_seconds <= 300}")
