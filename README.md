# Develop. This Employees website #

This project was made for Code Institue Data Centric Development Assignment
The aim was to 'build a full-stack site that allows your users to manage a common dataset about a particular domain.'

I have choosen to build a website for a construction company. This company before was using other sites like dropbox, emails and even paper. This site was to help the company to become 'lean'. Meaning instead of use a multitude of different sources, making one site for ease of access.
The company has grown from a tiny, to a medium company and as such wanted to become more professional to help the employees and owner in their day to day operations.




## UX ##
Develop This wanted a website with two sides, the employees and the owner/administrator.

### Employees ###
Employees should have access to general information about the projects and limited information about their follow workers.
Also their privite information should only be accessed by the owner/administrator.
It would be understood that the employees would not have access to a computer or ipad at work. As such, information and large clickable buttons on phone view point is a must.  

#### Projects ####
##### Read only as employees #####
Instead of sending emails of details about a project. A collection of the projects with information can be found in one place.
As projects start and finish at different times. The owner could just say, next project is '1010' and the employee can find the relavent information without asking about the address or type of work. 
1. Client 
    * Their name, contact details and address.
1. Discription
    * An understand of their purpose of work.

##### Design Ideas #####  
Projects should be easy to find with the important information ready to read.
If the user wants more details, a button click will show more indepth details such as a description of the project.
Further features to implement would be access to downloadable files. While detail plans of projects are not ideal to view from a phone, home access would be a good feature. 

#### Time Logs ####    
##### CRUD as employees #####
This site will keep all the timesheets in one place. The employee will not need to keep their own records or send the owner/administrator timesheets every week but can keep up to date records.
1. Time sheets should have the following information.
    * Date of days worked.
    * Hours worked on that day.
    * Where or which project work was performed.
    * A discription of what they did that day.
1. An overview of records
    * Should be able to see a review of any week or month.
    * An overview of total hours worked in a week or month. 

##### Design Ideas #####
As timesheet updates would be required on a regular bases, a clear view of the current week with hours worked, project number and even a total hours worked of the week should be clear. As such, to display all information, the week is displayed on a horizontal scroll. 
A quick eas 
          
#### Other Employees ####
##### Read only as employees #####
As the company grows in size, organation between employees about projects and travel details can be by passed from the owner. 
Also in emergcy situation, having the other employees next of kin information could save time.
1. Contact details
    * Their phone number to organise pick up arrangements or general contact.
1. Next of Kin
    * Accidents do happen. An access to emergcy phone number of the other employees.

#### Privite ####
##### CRUD as employees #####
Having one organised website allows up to date information between owner and employee. If the employee changes bank, the employee can update the relevent information without sending emails and the owner can not misplace the information. 
1. Address
    * For owner and adminstators use only. While this website strives for a paper-less world, occasionally post will be need to be sent.
1. Bank Details
    * For owner and adminstators use only.   


### Owner/Administrator ###  
Owner and Administrator has access to all avaible information and is not limited like the employees.
As such, Owner and Administrator can create, read, update and delete on every aspect of the site.
This site should have all the information, overviews and general day-to-day operations of the workers and projects.


#### Projects ####
Overview of projects 
1. New Project/Client:
    * Contact details.
    * Discription:
        * Brief: More of an indication on what project the employees are working.
        * Overview: A More detail plan of the project.
    * Price:
        * Price type: price per hour or total cost depending on quote/project.
        * Price: Arrange price per hour or total (numbers).   
    * Active Project:
        * If the project is current in operation or has been finished.       
    

#### Time Logs ####    
Instead of search though emails for each worker timesheet, then finding the different projects, this site should provide all the information in an organised fashion. The relavent information can be shown by worker, time period or project.
1. Employee:
    * An overview of individual hours to insure pay
1. Projects:
    * An overview of total hours in one project from many employees.    
          
#### Other Employees ####
A phone book of employees
1. Contact details
    * Their phone number to organise pick up arrangements or general contact.
1. Next of Kin
    * Accidents do happen. An access to emergcy phone number of the other employees.

#### Privite ####
Ease of access of information which can be kept up to date from employees leaving the owner to spend time on other endeavours.
1. Address
    * For owner and adminstators use only. While this website strives for a paper-less world, occasionally post will be need to be sent (for example: Contacts).
1. Bank Details
    * For owner and adminstators use only. 









<!-- login from flask doc    
https://flask-login.readthedocs.io/en/latest/ -->