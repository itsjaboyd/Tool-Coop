# Tool Shed Inventory Application

## Organization & Name Scheme

**Repository Organization**\
Our application source code is found under the src/ directory, where the file structure then follows django's defaults.\
Any documentation needed for the project including diagrams, requirements, and the project plan is found inside the docs/ directory.\
This README file is found in the top level directory.

**Application Schemes**\
Filenames will be limited to one word and either use camel case or dashes in between words.

## Version Control Procedures

Git will be used for version control, with our remote repository on Github located on [Ian's Github.](https://github.com/IanMacfarlane/cs3450-toolshed)\
See "Git Workflow" for more information on how we will use git for our project.

## Git Workflow

Our project will follow the standard workflow outlined by git.\
The official documentation for the procedures can by found on [Atlassian's Website.](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)

This project will use the _git_ feature branch workflow.\
Instead of having a fork of the main repository, only use the single remote Github repository and pushing to that.\
Any time you are working on a new feature make a new branch.

Before you push your code to Github first git pull to make sure that you are not pushing without having your local repository up to date.\
This will make it easier for us to resolve merge conflicts by making sure that there are not any conflicts before you push your code.\
Once you push your branch to remote, make a pull request so we can check and make sure everything is working before merging the branch to master.

As far as branch naming conventions go we should stick to lower case with dashes separating words.\
Try and make branch names as descriptive as you can.\
We also don't need to specify who made the branch in the branch name because git shows who makes which commits.

## The Tool Stack 

1. [Django backend framework](https://docs.djangoproject.com/en/3.0/)
2. [Reactjs frontend framework](https://reactjs.org/docs/getting-started.html)
3. [AWS for web page hosting](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

(Click on the links to visit their corresponding websites)

This is a simple web application so use any text editor you want.\
This project will be written in Python and JavaScript, along with some HTML and CSS.\
We can use Reactjs to embed the majority of the HTML in the js files.\
For CSS we can make a custom style sheet, or we can do custom css embedded in our js files with React.\
We could also use a CSS framework such as [_Bootstrap_](https://react-bootstrap.github.io/getting-started/introduction)

## Build Instructions

This project is built using the **django** framework.\
To run the webpage on a local server navigate to src/ and run:

```$ python manage.py runserver```

Once the local server is up and running, open up a browser and pull up your localhost on port 8000:

```http://localhost:8000/```

## Unit Testing Instructions

Unit testing instructions will appear here once we are far enough into the project.

## System Testing Instructions

System testing instructions will appear here once we are far enough into the project.

## Other Notes
**Phase 2**:\

* High fidelity prototype files are located in the src/template folder, which includes a home, inventory, and tool checkout page.
* Low fidelity wireframe is found in the docs/diagrams folder.
* Screenshots that include our Github issues page and srum bored are located in the docs/phase2screenshots folder.
    - [Scrum board](https://docs.google.com/spreadsheets/d/115-6lCkCsZA2XjLZDjx7ftg_P1KPQyFkSXc2TrXL4D8/edit?usp=sharing)



##Ian's TODO
set up virtual environment for the django project to make running on beanstock easier
or manage requirements.txt manually

set up tool stack so that everything is ready for development to actuallys start
