# GPA Discord Bot

Ever want to know what your GPA is without having to track every single assignment and grade? Well now you can with the GPA Discord Bot! This bot will calculate your GPA based on the grades you input. This bot is perfect for students who want to know what their GPA is or what they need to get in the future to achieve a certain GPA. To add the bot to your server, click [here](https://discord.com/oauth2/authorize?client_id=1188281911014076416&permissions=1099981390848&scope=bot).

## Commands and Usage

Note: All commands must be preceded by the prefix ```$``` and arguments DO NOT need to be surrounded by quotes

 ```$addUser ``` is to use the bot and any of its commands, you must first add yourself to the bot's database.

 ```$commands ``` will list all the commands that the bot has to offer in case you forget some of these

 ```$addCourse 'COURSE' ``` adds a course to your profile with the name of the course

 ```$removeCourse 'COURSE' ``` removes a course from your profile with the name of the course

 ```$addAssignment 'COURSE', 'ASSIGNMENT', 'GRADE', 'WEIGHT' ``` adds an assignment to your profile of the specified course, assignment name, grade, and its weight

 ```$removeAssignment 'COURSE', 'ASSIGNMENT' ``` removes an assignment from your profile of the specified course and assignment name

 ```$removeAllAssignments 'COURSE' ``` removes all assignments from your profile of the specified course

 ```$removeAllCourses ``` removes all courses from your profile

 ```$gpa 'COURSE'``` calculates your GPA based on the grades you have inputted

 ```$wantedGPA 'COURSE', 'GRADE' ``` calculates the grade you need to get on the final to achieve the specified grade in the specified course

 ```$listCourses ``` lists all the courses you have added to your profile

 ```$listAssignments 'COURSE' ``` lists all the assignments you have added to your profile of the specified course

 ```$removeUser``` removes you from the bot's database


## Built With 
* [Discord.js](https://discord.js.org/#/) - The framework used to create the bot
* [MongoDB](https://www.mongodb.com/) - The database used to store user information
* [DigitalOcean](https://www.digitalocean.com/) - The server used to host the bot

 ## License
 This project is licensed under the [MIT License](LICENSE).
