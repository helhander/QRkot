# ChariF
## About
ChariF - an application for the Charity Fund to control, accumulate, and spend it.

The Foundation collects donations for various targeted projects. 
Several target projects can be opened in the Foundation. Each project has a name, description and the amount that is planned to be collected. After the required amount is collected, the project is closed.
Donations to projects are received according to the First In, First Out principle: all donations go to the project opened earlier than others; when this project reaches the required amount and closes, donations begin to flow to the next project.

The API can be viewed in openapi.json
## How to launch a project
Clone the repository and go to it on the command line:
```
git clone 
```

```
cd cat_charity_fund
```

Create and activate a virtual environment:

```
python3 -m venv venv
```

* Linux/macOS

    ```
    source venv/bin/activate
    ```

* Windows

    ```
    source venv/scripts/activate
    ```

Install dependencies:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Launch the project:

```
uvicorn app.main:app
```
