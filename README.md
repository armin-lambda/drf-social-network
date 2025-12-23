# Social Network API

This project is a backend API for a social network application. It is built with Django and Django REST Framework and provides endpoints for user accounts, posts, comments, and follow relationships.

---

## 📦 Installing

### Run the following commands:

    pip install -r requirements.txt

    python manage.py migrate

    python manage.py runserver

## API Endpoints

### Authentication

| Endpoint              | Method | Access Token Required | Required Fields            |
|-----------------------|--------|-----------------------|----------------------------|
| `/api/token/`         | POST   | No                    | username, password         |
| `/api/token/refresh/` | POST   | No                    | refresh                    |

---

### Accounts

| Endpoint              | Method | Access Token Required | Required Fields                                                                 |
|-----------------------|--------|-----------------------|---------------------------------------------------------------------------------|
| `/api/accounts/`      | GET    | Yes                    | None                                                                            |
| `/api/accounts/`      | POST   | No                    | username, email, first_name, last_name, phone_number, password, confirm_password |
| `/api/accounts/<username>/` | GET | No | None | 
| `/api/accounts/<username>/` | PUT/PATCH | Yes | All profile fields are optional in PATCH method (username, email, first_name, last_name, phone_number, password, confirm_password) | 
| `/api/accounts/<username>/` | DELETE | Yes | None |
| `/api/accounts/<username>/follow/`   | POST | Yes       | None                                                                            |
| `/api/accounts/<username>/unfollow/` | DELETE | Yes       | None                                                                            |
| `/api/accounts/<username>/followers/`| GET  | Yes        | None                                                                            |
| `/api/accounts/<username>/following/`| GET  | Yes        | None                                                                            |
| `/api/accounts/<username>/posts/`| GET  | Yes        | None                                                                            |
---

### Posts

| Endpoint              | Method | Access Token Required | Required Fields |
|-----------------------|--------|-----------------------|-----------------|
| `/api/posts/`         | GET    | Yes                    | None            |
| `/api/posts/`         | POST   | Yes                   | (description, body) |
| `/api/posts/<post_id>/` | GET  | Yes                    | None            |
| `/api/posts/<post_id>/`         | PUT/PATCH   | Yes                   | All post fields are optional in PATCH method (description, body) |
| `/api/posts/<post_id>/new-comment` | POST  | Yes                    | Body |
