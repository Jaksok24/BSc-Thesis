class Order():
    def __init__(self, oID, customer, vehicle, driver, status, load_location, unload_location, load_date, unload_date):
        self.oID = oID
        self.customer = customer
        self.vehicle = vehicle
        self.driver = driver
        self.status = status
        self.load_location = load_location
        self.unload_location = unload_location
        self.load_date = load_date
        self.unload_date = unload_date
