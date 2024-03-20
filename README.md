
# BiteBurst
BiteBurst is a dynamic web platform that brings food enthusiasts together in a vibrant community space. Powered by HTML, CSS, JavaScript, Python with Flask, and PostgreSQL, BiteBurst offers an immersive experience where users can effortlessly create, read, update, and delete content. With its grid-style homepage, comprehensive CRUD system with a comment section, and a unique feature enabling users to showcase their favorite food within the discussion section, which is customizable in your profile, BiteBurst stands as the premier destination for engaging with food content and connecting with like-minded individuals. Join us today and explore the exciting universe of BiteBurst!

This is Milestone Project 3 for a Level 5 Diploma in Web Application Development.    

![alt text](README-images/ "Website Mockup")  

Link to live site: https://pythonlogin-017f233d45cf.herokuapp.com/

## CONTENTS

* [User Experience](#user-experience-ux)
  * [User Stories](#user-stories)

* [Design](#design)
  * [Colour Scheme](#colour-scheme)
  * [Typography](#typography)
  * [Layout](#layout)
  * [Imagery](#imagery)
  * [Wireframes](#wireframes)
  * [Data Model](#data-model)
  * [Security](#security)
  * [Future Updates](#future-updates)

* [Features](#features)
  * [Future Implementations](#future-implementations)
  * [Accessibility](#accessibility)

* [Technologies Used](#technologies-used)
  * [Languages Used](#languages-used)
  * [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used)

* [Testing](#testing)

* [Deployment](#deployment)

* [Credits](#credits)
  * [Code Used](#code-used)
  * [Content](#content)
  * [Media](#media)
  * [Acknowledgments](#acknowledgments)
  
  ---

## User Experience (UX)  

### User Stories

**User Story 1:** 



**User Story 2:** 



**User Story 3:** 



**User Story 4:** 



## Design  

### Colour Scheme





### Typography


### Layout



### Accessibility  


 

### Imagery  


### Wireframes


### Data Model  


# Database Relationships Schema

**User to Posts**
- One to Many.
- Each user can have multiple posts.
- The user object will have a `posts` property to query all related posts. This allows users to create and manage their own posts.

**Post to User**
- Many to One.
- Each post belongs to one user.
- The post object will have a `user` property to query the related user object. This associates each post with its author.

**Post to Comment**
- One to Many.
- Each post can have multiple comments.
- The post object will have a `comments` property to access all comments related to it.

**Comment to Post**
- Many to One.
- Each comment belongs to one post.
- The comment object will have a `post` property to access the post it belongs to. This allows comments to be associated with specific posts.

**User to Comments**
- One to Many.
- Each user can make many comments.
- The user object will have a `comments` property to fetch all comments authored by that user.

**Comment to User**
- Many to One.
- Each comment is authored by one user.
- The comment object will have a `user` property to access the user who authored it. This links comments to their respective authors.


### Security  

A number of different security considerations were taken into account when putting together this project.  

**Use of .env file**  
Important credentials including DATABASE_URL and SECRET_KEY are located within .env file which is subsequently in a .gitignore file to ensure it remains secure. SECRET_KEY was initially located in __init__.py file, it has since been changed and moved to a more secure location in .env file, the database was also subsequently destroyed and rebuilt to produce a different DATABASE_URL.  

**Defensive Programming**  
Measures have been put in place throughout the site to prevent users from doing things they are not authorised to do. For example, A user who has not signed up to the site, cannot access any of the individual BiteBurst pages or unable to add a post. This has been implemented using @login_required decorators.  

**Password Hashing**  
 

**Input Validation**  
The code checks if the email already exists in the database to prevent duplicate registrations. Validation checks on the length of the email, username, and password ensure that users provide sufficiently complex information. Passwords entered during the registration process are confirmed by having the user enter them twice. If they don't match, an error is shown.  

**Feedback to Users**  
Flash messages provide feedback to users about the status of their actions. For example, 'successful login or reasons for authentication failure'. However, care is taken not to provide overly specific errors. For example, rather than saying "incorrect password for given email," the feedback messages are generalised like 'Email does not exist' or 'Incorrect password, try again.'  


## Features

### General features  
**Sign up**  
Users have the ability to sign up, and must choose their favourite food.

![Image of sign-up page](README-images/ "Optional title")

**Log in**  
Users can login using the information that they provided at the sign up process.  

![Image of login page](README-images/ "Optional title")

**Home page**  
Users are presented with an overview page that includes interactive images of 12 Food card receipes that the site currently facilitates (Fish Receipes, Chicken Receipes, Chinese Receipes, Taco Receipes, Sweet Treat Receipes, Baking Receipes, Meat Receipes, Pasta Receipes). When users hover over the images, they scale up slightly causing the image to be zoom out a little, leading to a better user experience. 

![Image of overview page](README-images/ "Optional title")


**Meals page**  
Individual page where users can go through and look at pictures of meals to create and inspire.

**Receipes page**  
Individual page where users can select any of the cards, which will then show them a receipe with instructions on how to make it.

**Discussion**  
Individual page where users can go to post and interact with other users about Food.  

**Post feature**  
Users can post content onto the discussion page, they can also browse other posts that users have already posted. The most recent posts will populate at the top of the page so that users are immediately displayed with the most recent posts.  

![Image of post feature](README-images/ "Optional title")

**Comment feature**  
Users can comment on posts made by themselves or other users, comments can be deleted once they have been added. The most recent comments are populated towards the bottom of the comments section, this way users can browse the older comments towards the top and the most recent responses towards the bottom.  

![Image of comment feature](README-images/ "Optional title")

**Delete modal**  
Users can delete posts and comments once they have added them. A confirmation 'delete modal' is displayed once the user clicks the 'delete' button.  

![Image of delete modal](README-images/ "Optional title")

**My profile**  
Users can navigate to the 'My profile' page, here they can add to their bio, change their favourite food that is displayed on their profile page. This can be viewed in any posts/comment.

![Image profile page](README-images/ "Optional title")


**Logout**  
Once users are finished on the site, they can click click the logout button which will take them to the home page.  

**Footer**  
Users can navigate to respective social media sites that are present in the footer.

![Image of footer](README-images/ "Optional title")  

**Flash Messages**  
I chose to use flash messages as a positive feedback to users whenever they made an action on the site. Everything from logging in, to adding a post to try something they aren't authorised to do.  

![Image of flash message](README-images/ "Optional title")  

**Creative timestamping**  
I decided to included a date and time that informed users when the post was posted. I think this makes it easier to remember when the post was created.

![Image of timestamp](README-images/ "Optional title")


### Future Implementations
There are a number of different features that could be implemented in the future;  
- Private messaging function that allows users to message directly.
- More interactive profiles that allow users to upload images and other content.
- The ability to view other users profiles.  

## Technologies Used

### Languages Used

**HTML5**  
Used for creation of markup for the website content.  
**CSS**  
Cascading style sheets used to style the individual pages.  
**Javascript**  
Used to toggle visibility of certain aspects of the site.  
**Python**  
Used to run the app.  


### Frameworks, Libraries & Programs Used

[Bootstrap 4.4.1](https://getbootstrap.com/)  
Boostrap was predominantly used throughout the site for responsiveness, modals to confirm deleting posts/comments and image carousel.

[CDN jsdelivr](https://www.jsdelivr.com/)  
CDN jsdeliver was used to serve static assets bootstrap and jquery to improve performance and reliability.

[Google Fonts](https://fonts.google.com/)  
Used to import '' font.  

[Font awesome](https://fontawesome.com/)  
Used to import icons on to the site to improve user experience.  

[Github](https://github.com/)   
GitHub is used to store the projects code after being pushed from Git.  

[Balsamiq](https:/balsamiq.com)  
Balsamiq was used to create the wireframes during the design process.  

[Heroku](https://id.heroku.com/login)  
Used to deploy the project.  

[Flask](https://flask.palletsprojects.com/en/3.0.x/#)  
Python framework that has provided tools and features to build my web application.  

[Jinja](https://jinja.palletsprojects.com/en/3.1.x/)  
Assisted me in generating dynamic HTML content based on templates and data.  

[PostgreSQL](https://www.postgresql.org/)  
Hosted the database used in my project.  

[Visual Studio Code](https://code.visualstudio.com/download)  
Visual Studio Code was use to create files pages and where i produced the code for the project.  

[Google Chrome Dev Tools](https://developer.chrome.com/docs/devtools/)    
Google Chrome Dev Tools was used during the testing phase to test the responsiveness of the site and to check for any bugs.

[Pixabay](https://www.pixabay.com/)  
Pixabay was used to source images used throughout the individual sports pages and overview page.  
 
[W3schools](https://www.w3schools.com/)    
W3schools was used as a guide for HTML, CSS and Python basic principles.  


## Testing 
Testing process can be found [here]() 


## Deployment

**How was this site deployed?**

The website was initially deployed on Heroku.

**Deploying on Heroku**  
The following steps will need to be taken to deploy the application using Heroku.

- Create a requirements.txt file.  
- Create a Procfile by typing echo web: python app.py > Procfile. Ensure it starts with a capital P.  
- Go to Heroku. Log in or create an account.  
- Click the 'New' button and click 'Create new app'.  
- Enter a unique name for your project with no capital letters or spaces and select your region. Click 'Create App'.  
- Inside your project, go to the Resources tab and create a Heroku Postgres Database.  
- Inside your project, go to the 'Settings' tab. Scroll down and click 'Reveal Config Vars'.  
- Add in the following variables.
   - SECRET_KEY : Your secret key
   - DATABASE_URL: your postgres database URL
- Deploy your project by going to the Deploy tab and choose 'Connect to Github'
- Find your repository name and select Connect.

**Create a new repository on GitHub**  
- Add the necessary files to the repository.
- Go to the settings page of the repository, located on the menu bar towards the top of the page, scroll down to the GitHub Pages section which is located at the bottom of the 'Code and automation' sub-section.
- Select the main branch and the root folder, then click save.
- The website will now be live at the URL provided in the GitHub Pages section.

**How to clone the repository**

- Go to the (https://github.com/)  repository on GitHub.
- Click the "Code" button to the right of the screen, click HTTPs and copy the link there.
- Open a GitBash terminal and navigate to the directory where you want to locate the clone.
- On the command line, type "git clone" then paste in the copied url and press the Enter key to begin the clone process.  

**How to Fork the repository**  

- Go to the https://github.com/ repository on GitHub.
- Click on the 'Fork' option towards the top left of the page.  
- Click the dropdown button and click 'create a new fork'.  
- This will bring up a page with details of the repository, fill in boxes as required.
- Click 'create fork'.  

For further guidance [click here](https://docs.github.com/en/get-started/quickstart/fork-a-repo)  

Forking this repository will allow changes to be made without affecting the original repository.

## Credits

### Code Used

Bootstrap v4.4.1 
- Image carousels used from bootstrap.
- Delete Modal used from bootstrap.  

Code Institute training material  

Followed front-end tutorials from [Atheros] https://www.youtube.com/@Atheroslearning for footer and overview cards.
- Code referenced in html and CSS files that was inspired by Atheros learning.  

Followed tutorials from [Corey Schafer](https://www.youtube.com/@coreyms) to better understanding.  
 
Used [Flask tutorials](https://flask.palletsprojects.com/en/2.3.x/tutorial/views/) to better understanding.  

### Content


###  Media

**Images**  

  
###  Acknowledgments

Code Institute training material.  
