# The Dark Side - Testing details

[Back to README.md file](README.md)

[Live website](https://the-dark-side.herokuapp.com/)

## Code Validation

## Manual Testing
### Lighthouse Testing
### Functionality Testing
#### Responsiveness
#### Cross Browser

### User Stories Testing

### Bugs & Fixes
* After adding a couple of reviews with the title name in lowercase, I found that the Sort by Title function returned the non-capitalized titles at the end, sorted only as compared to each other as opposed to being sorted together with the capitalized names. I first tried to use the .lower() method as I was sorting the results but this resulted in an error. The solutions I was finding after googling the issue seemed overly complicated but I did find out it is common of MongoDB to return sort requests in this way, and so I decided to try the .capitalize() method as the title name is being sent to Mongo Db instead. This very simple solution worked to solve this problem. 


