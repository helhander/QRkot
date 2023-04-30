# QRKot
## About
QRKot - пan application for the Charity Fund for the support of cats.
The Foundation collects donations for various targeted projects: for medical care of tailed cats in need, for the arrangement of a cat colony in the basement, for food for cats left without care — for any purposes related to the support of the cat population.
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
