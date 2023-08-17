Accept
•	The function is created by using Python.
•	The function has a role with permissions to collect metrics and write them to a storage.
•	The function is tested and verified to collect the required metrics once a day using cloud SDK (for scheduling in AWS use AWS EventBridge, for scheduling in GCP use Cloud Scheduler which calls HTTP triggered Cloud Function).
•	The function stores the collected metrics as JSON files in cloud storage.
•	The storage is configured with encryption, lifecycle policies, and access control.

Quality
•	All commented code is removed from the project.
•	Proper exception handling is incorporated in the code.
•	Passwords or other secrets are not visible as plain text in the code.
•	Sensitive logs are appropriately suppressed.
•	Hardcoding of values is avoided. 
