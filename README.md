## Darma Backend Take Home Test

### Set up and run the project.
- Run `make recreate`

### Run the tests.
- Run `make test`

### Rationale behind key technical decisions.
## Framework
- The tech stack I used was Django (+ SQLite) because I use this framework usually these days and I can lay out a project quickly. Django offers way more features that are needed for this project but regardless Django covers the needs nicely.
- FastAPI would have been a good option too.
- I split the project in two Django apps: content_files and jobs. Those two fit well with the two main resources or domain models that the test talks about which are files submitted and summarized, and summarization jobs.

## DB schema
- I considered 3 models: SubmittedContentFile, ProcessedContentFile and SummarizationJob. The first two store in DB the metadata of the file submitted and processed, and the third one stores the job status and references through FKs to the submitted and processed file DB instances.

## Endpoints:
- Based on those resources mentioned in previous section and the requirements of the test the endpoints exposed are:

  - Submit file:
  /api/upload/

  - Retrieve job status:
  /api/jobs/<job_id>/status/ (although currently all fields of job are returned)

  - Retrieve summarized content:
  /api/jobs/<job_id>/summarized-content/

  - List all jobs:
  /api/jobs/

## Database
- I went with SQLite because it's works pretty much out of the box with Django and no additional Docker container is needed. Just it useful to add sqlite tooling to access DB shell when debugging. Of course SQLite won't be a good option for DB in production.

## LLM
- I used Google Gemini free tier as recommended.

## Future directions
- The local file system was used to store the fiels but S3 should be considered moving forward.

## Additional notes
- There is a bit of ambiguity with the concepts of summarized and processed in some parts of the projects but it was non-intentional. I thought of generalizing the summarization to processing since with an LLM we are processing text (even a prompt with no input file can be considered processing) but I didn't completely follow through. This should be fixed to avoid confusion in the project moving forward.

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
