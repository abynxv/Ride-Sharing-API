> ## Development Status

This branch contains ongoing development for real-time ride tracking and matching ride requests. Updates and implementations are in progress and will be completed soon.


## API Endpoints

### Authentication Endpoints (Common)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register new user account |
| POST | `/auth/login/` | Login and receive authentication token |
| POST | `auth/token/refresh/` | Using refresh token creating new access token |


### Driver Endpoints

| HTTP Method | URL Path                                        | Description                                                                                                    |
| ----------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | 
| **GET**     | `api/driver/rides/`                                | List all nearby rides with status `'requested'` and no driver assigned (filtered by driver location)           |           
| **POST**    | `api/driver/rides/{ride_id}/accept-ride/`          | Driver accepts the ride, assigns themselves, sets status to `'accepted'`                                       |
| **PATCH**   | `api/driver/rides/{ride_id}/update_status/`        | Update ride status (e.g., `in_progress`, `completed`) by the assigned driver                                   | 
| **POST**    | `api/driver/update-location/`                      | Update the current GPS coordinates of the logged-in driver (update `current_latitude` and `current_longitude`) |
| **GET**     | `api/driver/rides/assigned-rides/`                 | List all rides assigned to the logged-in driver (all statuses)                                                 |
| **GET**     | `api/driver/rides/{ride_id}/assigned-ride-detail/` | Get detailed info for a specific ride assigned to the driver                                                   | 

### Rider Endpoints


