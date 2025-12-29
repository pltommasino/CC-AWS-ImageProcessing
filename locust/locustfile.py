from locust import HttpUser, task, between, LoadTestShape
import json
import random


class ImageConversionUser(HttpUser):
    """
    Locust user that simulates calls to the image conversion API.

    Behavior:
    - Randomly selects a category ("small" or "medium") with 60/40 weights.
    - Chooses a random filename from the corresponding list.
    - Sends a POST request to the /convert endpoint with the filename in the JSON body.
    """
    # Random wait time between requests (in seconds)
    wait_time = between(1, 3)

    # Set the API Gateway host
    host = "**********"

    # List of available "small" images for the simulation
    small_images = [f"small_img_{i}.jpg" for i in range(1, 103)]

    # List of available "medium" images for the simulation
    medium_images = [f"medium_img_{i}.jpg" for i in range(1, 32)]

    @task
    def convert_image(self):
        """
        Main task:
        1. Randomly selects the image category (small / medium) with 60/40 weights.
        2. Selects a random filename from the corresponding list.
        3. Builds the JSON payload with the filename.
        4. Executes a POST request to /convert, measuring response time and success.
        """

        category = random.choices(
            ["small", "medium"],
            weights=[0.60, 0.40],
            k=1
        )[0]

        # Select filename based on the category
        if category == "small":
            filename = random.choice(self.small_images)
        else:
            filename = random.choice(self.medium_images)

        # Request body in JSON format
        payload = {
            "filename": filename
        }

        # HTTP headers to indicate JSON body
        headers = {
            "Content-Type": "application/json"
        }

        # POST request to the /convert endpoint
        # catch_response=True allows manually marking the request as success/failure
        with self.client.post(
            "/convert",
            data=json.dumps(payload),
            headers=headers,
            name=f"convert_{category}",
            catch_response=True
        ) as res:

            # If the response is not 200, mark it as a failure including the filename
            if res.status_code != 200:
                res.failure(
                    f"Error during conversion of file '{filename}': "
                    f"{res.status_code} {res.text}"
                )
                return


# ========================
#  WORKLOAD SHAPE
# ========================
class StepLoadShape(LoadTestShape):
    """
    Custom load shape to generate a controlled traffic profile.

    Stages:
    - 0–60s:    Warm-up with 5 users              -1min
    - 60–240s:  Ramp up to 30 users               -1/4min
    - 240–480s: Plateau with 30 users             -4/8min
    - 480–600s: Ramp down to 5 users              -8/10min
    - 600–660s: Final ramp down to 0 users        -11min
    """

    stages = [
        {"duration": 60,  "users": 5,  "spawn_rate": 1},
        {"duration": 240, "users": 30, "spawn_rate": 1},
        {"duration": 480, "users": 30, "spawn_rate": 1},
        {"duration": 600, "users": 5,  "spawn_rate": 1},
        {"duration": 660, "users": 0,  "spawn_rate": 1},
    ]

    def tick(self):
        """
        Computes the current number of users and spawn rate
        based on the total test runtime.
        """
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        
        return None