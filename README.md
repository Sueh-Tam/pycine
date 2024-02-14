About the Project: 

My project is a web application built with laravel. My project allows users to manage tasks, which are units of work that need to be done. Users can create tasks by providing a name, a description, and a full description of the task. Users can also read tasks by viewing their details, such as the name, the description, and the full description. Users can edit tasks by changing their name, description, or full description. Users can delete tasks by removing them from the database.
<br>
<br>
How to build the project:<br>

To build this project, you will need to have PHP and MySQL installed on your machine.;<br>
Copy the file named **.env.example** and paste it, rename the file to **.env**, and make this changes:<br>
1º - put the name of the database in the DB_DATABASE=<br>
2º - put the username in the DB_USERNAME=<br>
3º - put the password of the database in the DB_PASSWORD=<br>
<br>
After that, run the commands bellow in the main project: <br>
1º **composer install**<br>
2º **composer dump-autoload**<br>
3º **php artisan config:clear**<br>
4º **php artisan cache:clear**<br>
5º **php artisan migrate**<br>
6º **php artisan db:seed**<br>
7º **php artisan serve**<br>
