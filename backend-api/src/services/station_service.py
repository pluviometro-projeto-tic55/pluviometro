from src.models import RaspClient

def get_all_stations():
    """
    Retorna todas as estações cadastradas no sistema.
    """
    try:
        stations = RaspClient.query.all()

        if not stations:
            return None

        return [
            {
                "rcId": station.rcID,
                "name": station.name,
                "local": station.local,
                "latitude": station.latitude,
                "longitude": station.longitude
            }
            for station in stations
        ]

    except Exception as e:
        print(f"Error searching for stations: {e}")
        raise


def get_station_details(user_id):
    """ 
    Retorna os detalhes de uma estação com base no usuário.
    """
    try: 
        stations = RaspClient.query.filter_by(rcID=user_id).all()

        if not stations:
            return None
    
        return [
            {
                "rcId": s.rcID,
                "name": s.name,
                "local": s.local,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "email": s.email,
                "contact": s.contact,
                "height": s.height,
                "height_sea_level": s.height_sea_level,
                "status": s.status,
                "timestamp": s.timestamp.isoformat() if s.timestamp else None
            }
            for s in stations
        ]
    
    except Exception as e:
        print(f"Error searching for stations: {e}")
        raise
