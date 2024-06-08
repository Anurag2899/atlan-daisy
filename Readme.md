### Authored by 
Anurag kumar

# Approach Analysis

- Microservices Architecture: This approach involves breaking down the system into smaller, independent services that communicate with each other via APIs. While this allows for greater scalability and flexibility, it adds complexity in terms of managing multiple services and inter-service communication.

This architecture allows for modularity and scalability while maintaining a separation of concerns. It enables each integration to be implemented as a separate service, promoting plug-n-play functionality.


# Project Setup

- Dockerfile

    ``` Docker build -t data_collection:v1```

    ```Docker run -d data_collection:v1 ```

- Local setup

    ```pip install -r requrements.txt```

    ```gunicorn data_collection.wsgi```

# Codebase Structure
The codebase for the solution will be organized following standard best practices. It will include the following components:
- Models: Contains the database models representing forms, questions, responses, and answers.
- Serializers: Defines the serialization and deserialization logic for the models.
- Views: Implements the API endpoints and handles the business logic for each endpoint.
- Utils(Integration Services): Separate services for each integration, such as Google Sheets and SMS notifications.

# Database
```
+--------------+       +----------------+
|    Form      |       |    Question    |
+--------------+       +----------------+
| - id (PK)    |       | - id (PK)      |
| - title      |<------|- form_id (FK)  |
| - email      |       | - text         |
| - created_by |       | - mandatory    |
+-------------+       +----------------+
        ^                      |
        |                      |
        |                      |
        |          +----------------+
        |          |    Response    |
        |          +----------------+
        |          | - id (PK)      |
        +----------|- form_id (FK)  |
                   +----------------+
                             |
                             |
                             |
                   +----------------+
                   |    Answer      |
                   +----------------+
                   | - id (PK)      |
                   | - response_id (FK)|
                   | - question_id (FK)|
                   | - text         |
                   +----------------+
```

- Each Form has a primary key (id) and can have multiple Question objects associated with it.
- Each Question has a primary key (id) and belongs to a single Form through the foreign key (form_id).
- Each Response has a primary key (id) and belongs to a single Form through the foreign key (form_id).
- Each Answer has a primary key (id) and is associated with a single Response through the foreign key (response_id) and a single Question through the foreign key (question_id).

The proposed solution involves implementing the database models using a python based framework Django and creating corresponding serializers and views to handle the RESTful API endpoints. The codebase will be structured following best practices, ensuring modularity, maintainability, and scalability.

# Solution
Task 2:

For the validation check,I have given a field in question model to define if the field is mandatory or not , based on that i thought of mapping of answers with question for the final submittion while submitting if the question is empty it would revert back with appropriate response to fill the question.
Due to time constraint i wasn't able to implement it.

Task 3&4:

The endpoint "form/id" provides comprehensive access to the complete dataset stored within the specified form. In order to streamline data management processes.

The "submit/form_id" endpoint serves the dual purpose of sending data to a Google Sheet and sending a message.

I have successfully incorporated the Google Sheets API to seamlessly transfer this data into a designated Google Sheet.


- I had to create a Service account by enabling the drive and google sheet api in the google cloud console.

- Then i created the keys from that service through which my application will hit the google api server for authenticationand authorisation.

- Then i added the gcp service account that we have created earlier as a collborator to the sheet and passed the sheet link in the function for uodating the sheet.(limitation).

I have implemented the Twilio API to enable the delivery of response copies to phone numbers.

- I have to generate the twilio account sid and auth token which will give access to my application to send message through server of twilio.

- Free users can send to their number only(limitation).



Limitation: 

To facilitate data addition, a service account has been created specifically to access the list and granted collaborator privileges. Consequently, the creation of new sheets for each subsequent data entry is not feasible due to the fact that we have to add the service account as collaborator.

The free account is limited in its ability to send messages to any recipient. It can only send messages to the verified phone number associated with the account you have signed in with. However, by purchasing credits, we can unlock the full capabilities and utilize the messaging service to its fullest extent. In order to enable this functionality, I have provided my own phone number. Alternatively, we can acquire a dedicated phone number specifically for receiving responses to ensure the function operates.


# RESTful API Endpoints

By carefully going through the collect website I implemented these endpoints to create the form , create questions , create responses and the answers associated with them.

Below are the RESTful API provides endpoints to perform CRUD (Create, Read, Update, Delete) operations on the entities. The following is an outline of the proposed endpoints:

The RESTful API provides endpoints to perform CRUD (Create, Read, Update, Delete) operations on the entities. The following is an outline of the proposed endpoints:


### Health
- GET /health/: Health ok.

#### Forms

- GET /forms/: Get a list of all forms.
- POST /forms/: Create a new form.
- GET /forms/{pk}/: Get details of a specific form.
- DELETE /forms/{pk}/: Delete a specific form.

#### Questions

- GET /questions/: Get a list of all questions.
- POST /questions/: Create a new question.
- GET /questions/{pk}/: Get details of a specific question.
- PUT /questions/{pk}/: Update a specific question.
- DELETE /questions/{pk}/: Delete a specific question.

#### Responses

- GET /responses/: Get a list of all responses.
- POST /responses/: Create a new response.
- GET /responses/{pk}/: Get details of a specific response.
- PUT /responses/{pk}/: Update a specific response.
- DELETE /responses/{pk}/: Delete a specific response.

#### Answers

- GET /answers/: Get a list of all answers.
- POST /answers/: Create a new answer.
- GET /answers/{pk}/: Get details of a specific answer.
- PUT /answers/{pk}/: Update a specific answer.
- DELETE /answers/{pk}/: Delete a specific answer.

#### Additional Endpoints

- GET /forms/{form_id}/: Get details of a specific form.
- GET /submit/{form_id}/: Submit form data and perform additional actions.

The API endpoints allow clients to interact with the data store, perform CRUD operations, and retrieve specific details as needed.


# System Health Monitoring

## Monitoring part with prometheus 

- installation

    ```pip install django-prometheus```

- setup

    ```
    INSTALLED_APPS = [
    ...
    'django_prometheus',
    ...
    ]
    

    MIDDLEWARE = [
        'django_prometheus.middleware.PrometheusBeforeMiddleware',
        # All your other middlewares go here, including the default
        # 'django_prometheus.middleware.PrometheusAfterMiddleware',
    ]
    

    urlpatterns = [
        ...
        path('', include('django_prometheus.urls')),
    ]```

- Monitor database
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django_prometheus.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
    ```

- Monitor my models 

    - Present class

    ```
    class Question(models.Model):
        form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
        text = models.CharField(max_length=255)
        mandatory = models.BooleanField(default=False)
    ```
    - Modified class
    ```
    from django_prometheus.models import ExportModelOperationsMixin
    class Question(ExportModelOperationsMixin(‘question'),models.Model):
        form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
        text = models.CharField(max_length=255)
        mandatory = models.BooleanField(default=False)
    ```

- This will export these 3 metrics 
    ```
    django_model_inserts_total{model=“question”}, django_model_updates_total{model="question"} and django_model_deletes_total{model="question"}.
    ```

    ## Logging 

    - We can use loki for this application.But right now it's not that big application.So we can sys log itself.
    - Just define this line in the Gunicorn.conf.py file and you are good to go

            errorlog = "/var/log/gunicorn.error.log"

            capture_output = True

## Third-Party Considerations

When integrating with third-party services like Google Sheets and twillio sms, it's essential to be aware these things:

- API Rate Limits
- API Deprecation

# Kubernetes files 

I have used db.sqlite3 for the sake of easy setup while running the code, But in production we will have databse hosted, So taking into consideration i have writeen the manifests for depolyment but taking hypothetical storage path for storage claims.the folder consists of :

- Deployment.yaml
- Service.yaml
- Persisten-volume.yaml
- Persistent-volume-claim.yaml

# Gunicorn server
Django builtin server is singlr thread so for handling concurrent requests efficiently i have used gunicorn.It utilizes multiple worker processes to handle incoming requests in parallel, providing better performance and scalability.

    workers = multiprocessing.cpu_count() * 2 + 1

    worker_connections = 1000

For example, if our server has 4 CPU cores, Gunicorn will create 9 workers (4 * 2 + 1).
Each worker is capable of handling up to 1000 simultaneous connections, meaning that your application has the potential to serve up to 9000 concurrent users (9 workers * 1000 connections per worker).
This is the ideal case it will also depend on code complexity,workload.To get more accurate of application capacity we will have to perform load test.

## Conclusion

The proposed solution for the Collect data collection platform addresses the problem statement by leveraging a relational database model and a RESTful API architecture.The solution allows for seamless integration with third-party services and includes system health monitoring practices.
For detailed code implementation and further information, please refer to the delivered zip file.
If you have any further questions or need additional assistance, feel free to ask!
