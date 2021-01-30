class Airport:
    def __init__(self, iata, latitude, longitude, city, country, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iata = iata
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.country = country
