
//Provides Functionality for the ReadMe buttons on the portfolio page.
function constructProjectReadMe(owner_name, project_name, project_title){
    //calls GitHub API to get readMe information about the project when the button is clicked
    axios.get(`https://api.github.com/repos/${owner_name}/${project_name}/readme`, {headers:{"accept":"application/vnd.github.html+json"}}).then((data) => {
        //sets the utility modal fields to the project_title and project ReadMe
        document.querySelector("#utility-modal-label").innerHTML = project_title
        document.querySelector("#utility-modal-content").innerHTML = data.data
    })
}