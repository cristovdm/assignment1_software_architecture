# Assignment 1 (Software Architecture)

This sample application allows users to simulate the management of book reviews, with various specific requirements and functionalities that need to be implemented. This belongs to Assignment 1 of the Software Architecture course.

## Docker Compose

The application has a docker-compose file to compose docker containers and run it on docker. To do this, all that needs to be done is run the following command on a terminal in the main path:

```bash
docker-compose up --build
```

That will build the containers and once they are up the app is ready to go.

# To run locally:

## 📦 Dependency Installation 📦

As a suggestion, it is recommended to be in a virtual environment for greater security. To do this, you must execute the following commands in the main path:

- 🔨 Creating a virtual environment:
```bash
py -3 -m venv .venv
```

- ✅ Activating the virtual environment:
```bash
.venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux
```

- ❌ Deactivating the virtual environment:

```bash
.venv\Scripts\deactivate  # Windows
source venv/bin/deactivate  # Linux
```

The necessary dependencies for the operation are in the requirements.txt file, and to easily install everything, you need to run the following:

```bash
pip install -r requirements.txt
```

## ▶️ Start Server ▶️

To start the server, run the following commands on the main folder:

```bash
cd .\reviews\
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 🕺 Populate Database 🕺

To populate the database, the Faker library is used. This is a library used to generate realistic fake data, making it easier to create sample data to populate the database. In this sense, Faker generates names, birthdates, countries of origin, and descriptions for authors, as well as book titles, summaries, publication dates, and sales for books. Additionally, it generates review texts, scores, and upvotes for reviews, and annual sales for each book, allowing a large amount of coherent and varied data to be quickly created for testing and development. To populate the database, use the following command:

```bash
python manage.py populate_db
```


