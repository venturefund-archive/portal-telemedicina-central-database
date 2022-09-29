import json
import random

from locust import HttpUser, TaskSet, task


class PatientsUser(TaskSet):
    @task
    def patients_list(self):
        headers = {"Authorization": f"Token {self.user.login_token}"}
        self.client.get("/patients/all/", headers=headers)

    @task
    def patients_detail(self):
        headers = {"Authorization": f"Token {self.user.login_token}"}
        for id in range(1, 5001):
            self.client.get(f"/patients/all/{id}", headers=headers)

    @task
    def vaccines_list(self):
        headers = {"Authorization": f"Token {self.user.login_token}"}
        self.client.get("/patients/all/", headers=headers)

    @task
    def vaccines_detail(self):
        headers = {"Authorization": f"Token {self.user.login_token}"}
        for id in range(1, 5001):
            self.client.get(f"/patients/vaccines/{id}", headers=headers)

    @task
    def vaccine_status_list(self):
        headers = {"Authorization": f"Token {self.user.login_token}"}
        self.client.get("/patients/all/", headers=headers)

    @task
    def vaccines_status_detail(self):
        headers = {"Authorization": f"Token {self.user.login_token}"}
        for id in range(1, 5001):
            self.client.get(f"/patients/vaccine-status/{id}", headers=headers)

    @task
    def patients_post(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.user.login_token}",
        }
        self.client.post(
            "/patients/all/",
            headers=headers,
            data=json.dumps(
                {
                    "full_name": "testname1",
                    "social_name": "testname1",
                    "date_birth": "2022-09-14",
                    "sex": "M",
                }
            ),
        )

    @task
    def vaccine_post(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.user.login_token}",
        }
        self.client.post(
            "/patients/vaccines/",
            headers=headers,
            data=json.dumps(
                {"limit_date": "2022-01-01", "name_of_vaccine": "testname"}
            ),
        )

    @task
    def vaccine_status_post(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.user.login_token}",
        }
        self.client.post(
            "/patients/vaccine-status/",
            headers=headers,
            data=json.dumps(
                {
                    "patient": random.randint(1, 5000),
                    "vaccine": random.randint(1, 5000),
                    "completed": bool(random.getrandbits(1)),
                }
            ),
        )


class WebsiteUser(HttpUser):
    tasks = [PatientsUser]
    login_token = ""

    def on_start(self):
        response = self.client.post(
            "/auth-token/", json={"username": "admin", "password": "admin"}
        )
        self.login_token = response.json()["token"]
