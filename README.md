## Darma Backend Take Home Test

### Set up and run the project.
- Run `make recreate`

### Run the tests.
- Run `make test`

### Rationale behind key technical decisions.
- The tech stack I used was Django + SQLite because I use this framework more these days so I can lay out a project quickly. I didn't make the endpoint async but

### Build and run the Docker image.
- The docker container is built and run using `make recreate`. If it was already recreated can be stopped with `make down` and started with `make up`. 

### Interact with the API using a tool like Postman or curl.
- Submit a file for processing like shown below in Postman:

<img width="1376" alt="Screenshot 2024-12-16 at 7 38 24 AM" src="https://github.com/user-attachments/assets/8482df98-126e-497d-b13b-25bb5b04ef10" />


- Check the status of a summarization job:

<img width="1392" alt="Screenshot 2024-12-16 at 7 41 58 AM" src="https://github.com/user-attachments/assets/27018c19-bca4-4ed2-be96-bbe203e48613" />


- Retrieve the summarized content of a submitted file:

<img width="1402" alt="Screenshot 2024-12-16 at 7 43 53 AM" src="https://github.com/user-attachments/assets/2103d37b-8328-40ef-b7a2-f5ffceea00a0" />


- List all jobs with their status:

<img width="1399" alt="Screenshot 2024-12-16 at 7 45 19 AM" src="https://github.com/user-attachments/assets/6d786029-4752-45b5-8fd6-4efe3fd44ea6" />
