### Project Setup


1. Ensure that you have docker, docker-compose
2. Clone the existing repository
3. Start up the application
```bash
sudo docker-compose up -d
```
4. Run migrations
```bash
sudo docker-compose exec project_web python manage.py migrate
```
5. Create superuser
```bash
sudo docker-compose exec project_web python manage.py createsuperuser
```

### Instruction

This repository includes a basic Django application which can be run using Docker Compose.

Some basic models, views and templates using Bootstrap have been created, and it is now up to you to expand on this with some additional functionality. It will be important to write unit tests to test any bit of functionality you have implemented.

Once complete, commit your code to Github and share your project with us. You have 72 hours to complete as much as you are able to, and send your code back to us.

A list of functionality required includes:
- Validator which ensures the client's ID number is a valid South African ID number.
- Validator to ensure that a client with the same ID number doesn't already exist, notifying the user before the form is even submitted.
- Create a "New Client" form which allows you to add the client and address details at the same time and update both models. A client should have both a Physical and Postal address, unless the Postal address is the same as the Physical address.
- Create option to search for clients on the client list page, which updates as you type, but searches on the server side.
- Add a new "Relationship" Model which allows you to create relationship between clients (e.g Husband, Wife, Father, Daughter) and create a form to create these relationships, as well as a page to view them. A client cannot have a relationship with themself.
