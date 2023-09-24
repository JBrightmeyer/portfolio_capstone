# portfolio_capstone

*Currently Deployed at https://portfolio-s6uu.onrender.com*

API - https://docs.github.com/en/rest/quickstart?apiVersion=2022-11-28&tool=javascript

This project is a resume/portfolio manager which can create shareable links to a dynamically updated portfolio/resume site for users.  The site uses HTML-bootstrap/CSS/JavaScript as the front end with Python-Flask/Postgresql as the backend.  

The project supports users signing up with information regarding their github url, contact information etc. The user can then add work experiences and education to be parsed and displayed in the "profile" section of the website.  The user can also add information regarding github portfolio projects where they will be able to add brief descriptions and serve the READme and Programming language breakdown for each project using the GITHUB API.  The application also supports feedback submission sections to gather feedback on the website for myself. 

Database Schema can be found in the "database_schema" section of the root directory.

Future Goals: 
 - Convert to RESTful API for the backend, update frontend to use React.js or another front end framework
 - Add Unit Tests so as to not just rely on Functional Testing
