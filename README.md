# Develop. This Employees website #

This project was made for Code Institue Data Centric Development Assignment
The aim was to 'build a full-stack site that allows your users to manage a common dataset about a particular domain.'

I have choosen to build a website for a construction company. This company before was using other sites like dropbox, emails and even paper. This site was to help the company to become 'lean'. Meaning instead of use a multitude of different sources, making one site for ease of access.
The company has grown from a tiny, to a medium company and as such wanted to become more professional to help the employees and owner in their day to day operations.


## UX ##
Develop This while small, has two distict groups, management and employees. As much, while management has full access to all content, employees has limited to information (Example: Other employees bank details). This website should provide a 'Lean' approach to their work.

Overall experience should feel clean, easy to use and simple. This is used as a work tool with styling for ease and practicality. The colors are choosen to show different areas of the page while the buttons stand out for ease. 

### Employees ###
Employees should have full access and edit their own information. Employees should have access to common information about projects and other employees.
As such employees experience should be:
1. As a new employee, with a given sign up password, the employee should be able to...
    - Give personal information such as name, address, date of birth.
    - Give bank details.
    - Give emergcy details.
    - Set a personal password.
1. Be able to get contact details about other co-workers... 
    - Also able to update their own information.
1. Get information about project...
    - Contact details 
    - Address 
    - Discriptions
    - Project number.
1. Time logs...
    - Create and update their work log using a weekly calendar.

### Administration ###
Mangement should have full access to all aviable information on this site. They should also be able to create/edit projects and get employees information.
As such employees Administration should be to do everything an employee can do plus:
1. Get employees information.
    - See their personal information.
    - Get their private information like:
        - Bank details
        - Address
    - Update information of the employee.
    - Delete employee. 

1. Create, edit and remove Projects.
    - Create a project with information like:
        - Name of client
        - Contact details
        - Address of site
        - Discription of work
        - Type of payment (by the hour or total)
        - Add payment  
        - If active or finished site
        - Delete a project after it's been de-active.

1.  Time logs...
    - Create and update their work log using a weekly calendar. 


## UX ##    
### Existing Features ###
1. Login in or sign up
    1. A new member can sign up and become a new employee with a 'Welcome Password'
        * The new employee can add their own personal information such as name, address, contact details....
    1. A employee can login back into the site with their own personal password.
1. Time Logs
    1. As employees should create/edit time log of their work.
        * A custom made weekly time line for quick access of dates and to show when they have worked.
        * Add project number. Only active projects can be selected.
        * Add hours worked.
        * Add details of that they did that day
1. Projects
    1. Administration 
        * Add a new project
        * A new project gets their own unique project number. This is created by finding the last highest number, then add 1. 
        * Edit existing projects
        * De-active projects if the project is complete.
            * Remove project if completed
    1. Employees
        * Read projects to get information   
1. Employees   
    1. Administration 
        * Edit employee information
        * Get full access to all information
        * Delete employee
    1. Employees
        * Get general contact information
        * Edit their own information    

### Future Implement ###
1. A weekly schudule so that the employees can find out about which future projects that they will work on.
1. A monthly report of their work.
1. Reset Passwords.

## Technologies Used ##
1. [Visual Studio Code](https://code.visualstudio.com/) to write the project.
1. [GitHub](http://github.com) and [Heroku](https://dashboard.heroku.com/) to store and showcase the project.
1. [MongoDB](https://www.mongodb.com/) to store backend data.
1. [Javascript](https://www.javascript.com/) and [JQuery](https://jquery.com/) for DOM manipulation and on screen calculations. 
1. [Bootstrap](https://getbootstrap.com/) and [Bootwatch]("https://bootswatch.com/4/cosmo/bootstrap.min.css"): To structure and style the site.
1. [Python](https://www.python.org/) Was the main language to write the site and access the backend data. 



### Add on libararies Used ###
1. bcrypt: To incrypt passwords for security on site
1. Calendar, datetime and itertools for use of calendars in the site.
1. Flask: For handling python control of url, pass mongodb data onto site and use of variables.
1. pep8: To insure python code is in a correct format.


## Testing ##
### Sign Up ###
#### First Page ####
1. Incorrect Password.
    * A warning pop up explaing the password is wrong and to contact administration.
1. Username empty.
    * Form is required as such the new employee must enter a name.  
#### Personal Information #### 
1. To create a new user a first name, last name and their date of birth must be entered. From these three inputs, a new employee can be created.
A new employee first name and last name creates a username. If there is already an employee with the same first name and last name, the year from date of birth is also entered to create a username. If there is a username with the same first name, last name and date of birth, an error to contact administration will be alerted. 
1. Password is encrypted and can not be accessed by anyone inculding administration.
### Login ###
1. If incorrect user or blank, alert to address that a user is not found.
1. If incorrect password or blank, alert to contact admin for password.
### Time Logs ### 
1. Form is all 'Required' there for the form needs to be complete before sending.
1. Dates can be entered manually or by clicking the day in the week. As such, manual clicking of each day to insure javascript code updates correct date is inputted. 
1. The calendar is automatically updated, thus showing connections to mongodb is correct. On clicking on the timelog, I can see the right information has been passed.
### Projects ###
1. Only Administration can create, edit or delete projects. 
1. Project number is automaticly created from the last highest number last created. 
1. Project form is meant to be able to be updated, so even if there is limited information, the form will pass.
1. The project is automatically updated, thus showing connections to mongodb is correct.
### Employees ###
1. Administration can only see all information of an employee. They can also update or delete employees. To delete an employee, the page is re-directed to another page as a safe guard.

### Overall ###
1. Manual clicking of all buttons to insure url end points are correct.
### Interesting ###
1. I had some issues with time log week calendar. To change the week, I had to add a variable to session. As the form would re-load, it would only show next or previous week. By adding the plus or negative to a session variable, I was allowed to go through all the week even though the form was reloaded. With more time, I believe I could find a better solution. As this works as intended, I left it in this project.

### Validation ###
1. HTML
    * Use [validator.w3](https://validator.w3.org/): For every 'a href' I got an error of...
    Error: Bad value {{ url_for( 'example') }} for attribute href on element a: Illegal character in path segment: { is not allowed.
    After going back to Code Institute course work and looking at 'Task Manager' I notice the same issue.

1. CSS
    * Use [validator.w3](https://jigsaw.w3.org/css-validator/)
    * intro_style.css: W3C CSS Validator results for TextArea (CSS level 3 + SVG) No errors
    * style.css: W3C CSS Validator results for TextArea (CSS level 3 + SVG) No errors

1. Javascript
    * Use [jshint.com](jshint.com)
    * intro_page.js: Passed
    * main.js: Using JQuery, $ undefined variable.

1. Python
    * I used a vs pep8 extension to insure my python code was up to standard.
    * ctrl + shift + p to check python code
    * Use [pep8online](http://pep8online.com/)
        * Many errors with line too long. 







  













<!-- login from flask doc    
https://flask-login.readthedocs.io/en/latest/ -->