# The Dark Side - Testing details

[Back to README.md file](README.md)

[Live website](https://the-dark-side.herokuapp.com/)

## Code Validation

## Manual Testing
### Lighthouse Testing
### Functionality Testing

I used Google Chrome Dev Tools at all stage of this project to continuously check how each detail worked, particularly in ensuring responsiveness of each setion and feature as I worked on them. 

The following are the steps taken to manually test each feature of the website. 

Home Page as a non logged in user:

* Nav Bar
    + clicked on 'The Dark Side' logo at the left side of the nav bar to ensure home page loads. 
    + clicked on the 'Reviews' link to ensure dropdown menu expands as expected. Clicked on each link (Books, Movies, TV Shows, All reviews) to ensure it led me to relevant content page. 
    + clicked on the 'Home' link to ensure it returned me to home page.
    + clicked on the 'Register' link to ensure it brought me to the user registration page.
    + clicked on the 'Log In' link to ensure it loaded the user log in page.
    + clicked on the 'Contact' link to ensure it brought me to the Contact form page. 
    + all above were also checked with Navbar in the collapsible side nav state to ensure this sidenav element also functioned as expected.

* Footer
    + clicked on the 'Get in touch' link in the footer to ensure it brings user to the Contact Page.
    + clicked on each of the 3 social media links to ensure these opened in a new page and correctly brought the user to the relevent social media sites.

* Content
    + clicked on each link to ensure they function as expected:
        1. 'click here to see all reviews' link brings user to all reviews page
        2. 'Sign up now' link brings user to register page
        3. 'login page' brings user to the log in page
        4. 'Books' card link brings user to book reviews page
        5. 'Movies' card link brings user to movie reviews page
        6. 'TV shows' card link brings user to tv show reviews page

Home Page as a logged in user
* Nav Bar
    + visual check to ensure as a logged in user, the 'Register' and 'Log in links no longer display and are replaced with 'My Profile' and 'Add Review' links
    + click on 'My Profile' link to ensure is brings user to their unique profile page (this step was repeated using 3 different user logins I created)
    + click on 'Add Review' link to ensure it brings user to the add review form page
    + click on 'Log out' to ensure this logs out the current user and the nav bar links revert to original options and user is redirected to the log in page.

Books Review Page
* All of the above steps for the Navbar and Footer links were repeated to ensure all worked as expected from this page. 
* Steps repeated as a non logged in user as well as a logged in user.
    + click on each card display to ensure card is funtioning as expected and content can be revealed on clicking up arrow and hidden on clicking down arrow
    + Search bar:
        1. attempt to click search button with nothing entered in search field to ensure validation works
        2. enter a word known to not provide a match to test what is returned in a no results scenario  - 'No results found' flash message displays and 'Sort-by' bar is hidden as designed. 
        3. click on 'Reset' button - returns the user to the all reviews page with all reviews on the database showing. This functions as expected.
        4. enter a word known to match a title (or titles) to ensure results are returned as expected. This functions. Tested with a title know to bring up a single match, also tested with a title that should return mulitple matches (ie. 'haunted' returns two titles as expected). Also tested to ensure search is not required to be case sensitive. 
    + Sort-By feature:
        1. click on sort by arrow to ensure dropdown functions as expected and displays two options for the user - Title A-Z, Rating
        2. click on Title A-Z to ensure this returns only all book reviews in Title alphabetical order
        3. click on Rating to ensure this returns only all book reviews in order of rating (best to worst)

Movies Review Page/TV Shows Review Page/All Reviews page

* All the above steps for the book reviews page were repeated for each of the remaining review pages which all performed as expected. 
* Sort-by feature on each page returns only results from that category ie. on Movies page, sorting only deals with Movie reviews. This functioned as designed. On the reviews page, the sort-by returns all the results as expected. 

Register page
* All of the above steps for the Navbar and Footer links were repeated to ensure all worked as expected from this page. 
* Further steps taken:
    + tested username field valdiation by entering no characters, less characters than advised, special characters and tried registering, form validation functioned as expected and provides the user with feedback if not filled correctly
    + repeated these steps in the password field, all functions as expected. 
    + tested with entering a username known to already exist to ensure a duplicate is not accepted and a messsage is returned to user that that username already exists. 
    + tested link to log in page if user is already registered.
    + tested with creating a new user to ensure register form functions correctly and user is brought to their profile page and a success message is displayed to user, and nav links change to display correct options for a registered user

Log In Page
* Repeated all of the above steps with regard to checkin validation on username and password fields 
* Further steps taken:
    + attempted to log in with a username known to not be registered already, attempted to log in with an incorrect password for an already registered account - both steps resulted in log in failing, message being displayed to user that an incorrect username and or password was used and reloading the log in form to allow user make another attempt. 
    + logged in as registered user to ensure log in accepted as expected and user brought to their profile page
    + clicked on register link to ensure user is redirected to the register page if they have not yet done so.

Contact Page
* Repeated the above steps for all the navbar and footer links and functioning.
* Further steps taken:
    + attempted to send message form without the name field filled in, then with incorrect email format, and with message field left blank. The basic form validation functioned as expected to enusre form could not be submitted without the fields being filled in and provided feedback to the user indicating such. 
    + filled in all fields correctly and clicked send massage button to check that a message is displayed to the user indicating their message has been sent successfully. 

**Further User Logged in functionality testing** 





#### Responsiveness
#### Cross Browser

### User Stories Testing

### Bugs & Fixes
* After adding a couple of reviews with the title name in lowercase, I found that the Sort by Title function returned the non-capitalized titles at the end, sorted only as compared to each other as opposed to being sorted together with the capitalized names. I first tried to use the .lower() method as I was sorting the results but this resulted in an error. The solutions I was finding after googling the issue seemed overly complicated but I did find out it is common of MongoDB to return sort requests in this way, and so I decided to try the .capitalize() method as the title name is being sent to Mongo Db instead. This very simple solution worked to solve this problem. 


