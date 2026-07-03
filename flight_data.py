class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, data):
        self.price = data["price"]
        self.airline = data["flights"][0]["airline"]

        self.stops = len(data["flights"]) - 1
