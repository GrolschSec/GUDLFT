from locust import HttpUser, task

class TestProjectPerformance(HttpUser):
    
    @task
    def home(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", data={"competition": "Spring Festival","club": "Simply Lift", "places": "2"})

    @task
    def clubs_points(self):
        self.client.get("/clubs/points")

    @task
    def logout(self):
        self.client.get("/logout")