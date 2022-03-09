# The Breakbuddy(TM) by Softlocked Ducks
PM Eric Guo - Front-end (Bootstrap, HTML)  
Michael Borczuk - Back-end (Flask, API linking)  
Josephine Lee - Back-end (Flask, API linking)  
Yoonah Chang - Front-end (Bootstrap, HTML)  

## Description
  The Breakbuddy(TM) is designed to be used whenever someone is doing work. To prevent overworking or working continuously without a break, The Breakbuddy(TM) will alert the user after a certain amount of time working that they should take a break. After the user accepts the much needed break, The Breakbuddy(TM) will display images from Harvard Art Museums, along with jokes and fun facts on top of them to provide some slight entertainment for the user as well.

## APIs Used
- Fun Facts: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_FunFacts.md
- Harvard Art Museums: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_HarvardArtMuseums.md
- Kanye.rest: https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_kanye.rest.md

## Launch Codes
### Clone Repository

Clone this repository to your computer with https link:
```shell 
$ git clone git@github.com:EGuo2004/P01.git
```

### Set up a Virtual Environment

1. Create a virtual environment
  ```shell
  $ python3 -m venv <path_to_virtual_environment>
  ```

2. Activate the virtual environment
  ```shell
  $ . <path_to_virtual_environment>/bin/activate
  ```

### Install Libraries Contained in ``` requirements.txt```

```shell
(<venv_name>)$ cd <path_to_P01>
(<venv_name>)$ pip3 install -r requirements.txt 
```

### Run Program

```shell
(<venv_name>)$ cd <path_to_P01>/app
(<venv_name>)$ python3 __init__.py
```

### Launch Site

Go to http://127.0.0.1:5000/ in your browser.
