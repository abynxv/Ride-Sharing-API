> ## Development Status

This branch contains ongoing development for real-time ride tracking,matching ride requests and permission classes. Updates and implementations are in progress.

## API Endpoints

## Rider Endpoints
```bash
/api/rider/rides/	GET -	List all rides requested by the rider
/api/rider/rides/	POST -	Create a new ride request (Only if there is no active rides)
/api/rider/rides/{id}/	GET -	Retrieve details of a specific ride
/api/rider/rides/{id}/	PUT/PATCH	- Update ride info (only if status is 'requested')
/api/rider/rides/{id}/cancel-ride/ - POST	Cancel a ride (only if status is 'requested' or 'accepted')
/api/rider/rides/{id}/track-ride/	GET	- Get current ride status and driver location
```
<img width="1073" height="672" alt="image" src="https://github.com/user-attachments/assets/3dc18d3d-44fa-4266-897d-a27b534ca33b" />

## Driver Endpoints
```bash
api/driver/rides/ — List available ride requests nearby
api/driver/rides/{id}/accept-ride/ — Accept a ride request
api/driver/rides/{id}/update_status/ — Update the ride status
api/driver/update-location/ — Update driver’s current location (no ride ID needed)
api/driver/rides/assigned-rides/ — List all rides assigned to the driver
api/driver/rides/{id}/assigned-ride-detail/ — Get details of a specific assigned ride
```
<img width="1073" height="543" alt="image" src="https://github.com/user-attachments/assets/4307c3ea-0e0c-4b03-b3b1-45e6e5bfae2a" />

## Real-time Ride Tracking with Celery

To enable real-time ride tracking simulation in this project, you need to run both **Celery worker** and **Celery beat scheduler**. Celery worker executes asynchronous tasks, while Celery beat schedules periodic tasks, such as updating ride locations every few seconds.

### Running Celery and Celery Beat

Use the following commands in separate terminal windows:

```bash
# Start Celery worker
celery -A ride_sharing_api worker --loglevel=info
```
<img width="1256" height="626" alt="Screenshot from 2025-08-11 01-33-10" src="https://github.com/user-attachments/assets/1c05eec9-7b6a-4fad-a83a-14b451c63c75" />

```bash
# Start Celery beat scheduler
celery -A ride_sharing_api beat --loglevel=info
```
<img width="1256" height="626" alt="Screenshot from 2025-08-11 01-32-55" src="https://github.com/user-attachments/assets/7c994c3a-a630-42de-a24f-1f87eddca4bd" />




