##Darma Backend Take Home Test

###Set up and run the project.
- Run `make recreate`

###Run the tests.
- Run `make test`

###Rationale behind key technical decisions.
- The tech stack I used was Django + SQLite because I use this framework more these days so I can lay out a project quickly. I didn't make the endpoint async but

###Build and run the Docker image.
- The docker container is built and run using `make recreate`. If it was already recreated can be stopped with `make down` and started with `make up`. 

###Interact with the API using a tool like Postman or curl.
- Submit a file for processing like shown below in Postman:

![](../../../../Desktop/Screenshots/Screenshot 2024-12-16 at 7.38.24 AM.png)

- Check the status of a summarization job:

![](../../../../Desktop/Screenshots/Screenshot 2024-12-16 at 7.41.58 AM.png)

- Retrieve the summarized content of a submitted file:

![](../../../../Desktop/Screenshots/Screenshot 2024-12-16 at 7.43.53 AM.png)

- List all jobs with their status:

![](../../../../Desktop/Screenshots/Screenshot 2024-12-16 at 7.45.19 AM.png)