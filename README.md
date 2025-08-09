> This project is under development.

# Ride Sharing API

A backend API built with Django Rest Framework for ride-sharing applications. The system enables riders to request rides and drivers to manage ride requests through a comprehensive REST API.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abynxv/Ride-Sharing-API.git
   cd ride-sharing-api
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Features

### Rider Functionality
- Request rides with pickup and drop-off locations
- View personal ride history
- Edit ride details when status is REQUESTED
- Cancel rides

### Driver Functionality
- View all available ride requests
- Accept ride requests
- Start accepted rides
- Mark rides as completed
- 
## Technology Stack

- **Framework**: Django 5 with Django Rest Framework
- **Database**: SQLite3 (development environment)
- **Authentication**: JWT Authentication
- **API Design**: RESTful architecture using ModelViewSet

## API Endpoints

### Authentication Endpoints (Common)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register new user account |
| POST | `/auth/login/` | Login and receive authentication token |
| POST | `auth/token/refresh/` | Using refresh token creating new access token |

### Ride Management Endpoints
| Method | Endpoint | Description | 
|--------|----------|-------------|
| GET | `/api/rides/` | List rides (filtered by user role) |
| GET | `/api/rides/{id}/` | Fetch a ride by its id |
| POST | `/api/rides/` | Create new ride request |
| PATCH | `/api/rides/{id}/` | Update ride details |
| POST | `/api/rides/{id}/cancel-ride/` | Cancel ride request (status Requested only) |

### Driver Action Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `api/driver/rides/` | List available ride requests ( status Requested only) |
| POST | `api/driver/rides/{id}/accept-ride/` | Accept a ride request |
| PATCH | `api/driver/rides/{id}/update-status/` | Update status of a ride |


## API Testing with Postman

A Postman collection is included in this repository as `Ride Share API.postman_collection.json`.

### How to use:
1. Open Postman
2. Click **Import** → **Upload Files**
3. Select `Ride Share API.postman_collection.json`
4. The collection will be imported with all endpoints ready for testing


### User Auth

## User Register

**Method**: POST  
**URL**: `http://localhost:8000/auth/register/`  
**Headers**: 
```
Content-Type: application/json
```
**Body** (JSON):
```json
{
    "username": "rider1",
    "password": "password123",
    "email": "rider1@example.com",
    "role": "rider"
}
```

## User Login
**Method**: POST  
**URL**: `http://localhost:8000/auth/login/`  
**Headers**: 
```
Content-Type: application/json
```
**Body** (JSON):
```json
{
    "username": "rider1",
    "password": "password123"
}
```
**Response**:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Rider Endpoints

## Create Ride
**Method**: POST  
**URL**: `http://localhost:8000/api/rides/`  
**Headers**: 
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```
**Body** (JSON):
```json
{
    "pickup_location": "Calicut",
    "dropoff_location": "Kannur",
    "rider": "1"
}
```

## List All Rides
**Method**: GET  
**URL**: `http://localhost:8000/api/rides/`  
**Headers**: 
```
Authorization: Token your_rider_token_here
Content-Type: application/json
```

## Fetch Detail of a Ride
**Method**: GET  
**URL**: `http://localhost:8000/api/rides/3`  
**Headers**: 
```
Authorization: Token your_rider_token_here
Content-Type: application/json
```


## Update Ride Details
**Method**: PATCH  
**URL**: `http://localhost:8000/api/rides/1/`  
**Headers**: 
```
Authorization: Token your_rider_token_here
Content-Type: application/json
```
**Body** (JSON):
```json
{
    "pickup_location": "Updated pickup location",
    "dropoff_location": "Kannur",
}
```

## Cancel Ride (Rider Only)
**Method**: POST  
**URL**: `http://localhost:8000/api/rides/1/`  
**Headers**: 
```
Authorization: Token your_rider_token_here
```

### Driver Endpoints

## View Available Rides
**Method**: GET  
**URL**: `http://localhost:8000/api/driver/rides/`  
**Headers**: 
```
Authorization: Token your_driver_token_here
```

## Accept Ride
**Method**: POST  
**URL**: `http://localhost:8000/api/driver/rides/1/accept-ride/`  
**Headers**: 
```
Authorization: Token your_driver_token_here
```

## Status Change of a Ride
**Method**: PATCH  
**URL**: `http://localhost:8000/api/driver/rides/1/update-status/`  
**Headers**: 
```
Authorization: Token your_driver_token_here
```
