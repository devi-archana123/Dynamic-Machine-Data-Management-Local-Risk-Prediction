# Dynamic Machine Data Management & Local Risk Prediction

This project is a Flask web application for adding and managing machine details and predicting the risk level of a machine using a Random Forest model.

## Technologies Used

* Python
* Flask
* SQLAlchemy
* SQLite
* Scikit-learn
* HTML/CSS

## Setup and Run

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in the browser.

## ML Component

The Random Forest model is built using Python and Scikit-learn. It runs on the local machine. Flask calls the prediction function directly, so there is no separate ML server or external API.

## Application Architecture

Flask handles the web pages and requests. SQLAlchemy is used to store and retrieve data from SQLite. When a prediction is requested, the required machine values are passed to the Random Forest model, and the returned risk level is shown on the web page.

## Dynamic Fields

Machine fields are stored in the database, so a new field can be added without changing the database table.

The application supports Text, Number, and Dropdown fields, along with required and optional fields.

For example, `Humidity` can be added as a Number field and used when entering machine details.

The current Random Forest model uses Temperature, Pressure, and Vibration. The Humidity value can still be stored and displayed, but it is not used by the current model. If Humidity needs to be used for prediction later, the model will have to be retrained using Humidity as an additional feature.
