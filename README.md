# How to run the service

## Method 1 (Using docker)

- Build the image `docker build -t fastapi-app .`
- Run the image `docker run -p 8000:8000 fastapi-app`

## Method 2 (Using uv)

- Install uv https://docs.astral.sh/uv/getting-started/installation/#standalone-installer
    - If mac: `brew install uv`
    - If mac/linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Install dependencies `uv sync`
- Activate virtual environment `source .venv/bin/activate`
- Run application: `fastapi dev`

# Running tests

## Method 1 (Using uv)

- Install uv https://docs.astral.sh/uv/getting-started/installation/#standalone-installer
    - If mac: `brew install uv`
    - If mac/linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Install dependencies `uv sync`
- Activate virtual environment `source .venv/bin/activate`
- Run application: `pytest .`

## Method 2 (Using pip)

- Create a virtual environment `python -m venv venv`
- Activate it
    - Windows `venv\Scripts\activate`
    - macOS/Linux: `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Run tests: `pytest .`

# Project structure

- `billing` contains all the relevant code for the usage API
- `billing/router` contains the logic for the API endpoint itself
- `billing/services` contains the logic for the services that the API uses
- `billing/services/credit_calculation_service.py` contains the logic for calculating credits from a message
- `billing/services/message_service.py` contains the logic for getting messages from the API
- `billing/services/report_service.py` contains the logic for getting reports from the API
- `billing/services/util.py` contains utility functions
- `billing/models.py` contains general models used throughout the project
- `billing/schemas.py` contains models which are returned by the /usage API
- `billing/dataclasses.py` contains dataclasses used throughout the project
- `tests` contains all the tests for the project, similarly laid out as the `billing` directory

# Decisions/assumptions made

- A lot of the decisions/assumptions made are documented in the code itself. I will outline some top level decisions made here:
    - Separating out services
        - I separated out the services into their distinct functionalities e.g. calculating credits, getting reports,
          getting messages etc. I did this for separation of concerns reasons and to make the code more maintainable and testable in isolation. This was a trade-off between simplicity and flexibility, favoring flexibility to allow for easier future changes and extensions. I know some people might call it over-engineering, so I am mindful of that.
    - Creating a Credit value object
        - I decided to create a "Credit" value object, borrowing an idea from domain driven design. Some benefits include type-safety (using mypy), self-documenting code, business logic encapsulation
    - Testing
        - I've tried to unit test all the different components (i.e. from the api, all the way to services and util functions)
    - Assuming API call is quick
      - I've made assumptions that the API calls are short enough to carry out within one request would take (for example in a real-world scenario it could take much longer). The current method of getting all the messages and then potentially having to do a report fetch for each message is slow. I've outline potential solutions near the code.
    - Using sync instead of async
      - I used sync instead of async just for the sake of simplicity whilst developing + ease of testing
    - Using dataclasses
      - I think perhaps the Credit and BillingParameters dataclasses should have been pydantic models in the end, but I didn't have time to change them. I think it would have been more consistent with the rest of the project and avoided the unnecessary models/dataclasses.py file separation.
    - Commit history
      - I've tried to make commits atomic and meaningful, but I've also squashed some commits to make the history cleaner. I think I could have been more descriptive/granular in my commits, but I was trying to balance that with the time constraints.

# If I had more time
This is a list of things I could have expanded on/added if I had more time to develop the project.
- Monitoring
    - Sentry
    - Newrelic/Prometheus/Grafana
- Authentication + Database modelling
- Using async instead of sync
- Structured logging
- Pagination
- Search functionalities? (e.g. for specific time-frame)
- Caching (e.g. memcached/redis)
- Performance monitoring
- Test coverage
- API Versioning
- CORS
- CI/CD
