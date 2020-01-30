# Tool Shed

## Organization & Name Scheme
Default django project organization.

Try and keep filenames to one word and either use camel case, or dashes.

## Version Control Procedures

Git will be used for version control, with our remote repository on github located at https://github.com/IanMacfarlane/cs3450-toolshed

### Git Workflow

https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow

This project will use the git feature branch workflow. 
Instead of having a fork of the main repository we will only be using the single remote github repository and pushing to that. 
Any time you are working on a new feature make a new branch.
Before you push your code to github first git pull to make sure that you are not pushing without having your local repository up to date. 
This will make it easier for us to resolve merge conflicts by making sure that there are not any conflicts before you push your code.
Once you push your branch to remote, make a pull request so we can check and make sure everythin is working before merging the branch to master.
As far as branch naming conventions go we should stick to lower case with dashes separating words. 
Try and make branch names as descriptive as you can. 
We also don't need to specify who made the branch in the branch name because git shows who makes which commits.

## The Tool Stack 
Django backend framework. 
https://docs.djangoproject.com/en/3.0/

Reactjs frontend framework.
https://reactjs.org/docs/getting-started.html

AWS for web page hosting.
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

This is a simple web application so use any text editor you want. 
This project will be written in Python and Javascript, along with some HTML and CSS. 
We can use Reactjs to embed the majority of the HTML in the js files.
For CSS we can make a custom style sheet, or we can do custom css embedded in our js files with React.
We could also use a CSS framework such as Bootstrap https://react-bootstrap.github.io/getting-started/introduction

## Build Instructions

## Unit Testing Instructions

## System Testing Instructions

## Other Notes

