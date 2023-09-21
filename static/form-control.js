/* These functions provide functionality for the buttons located on the private_profile view.  The first is described but the rest follow a similar structure.  The functions are called through inline onClick properties assigned when the buttons are created*/

function constructAddProjectForm() {
    //URL for the form path
    const constructProjectUrl = `https://portfolio-s6uu.onrender.com/users/${document.querySelector("#user").getAttribute("data-id")}/projects/add`
    //retrieve the HTML of the form
    axios.get(constructProjectUrl).then((data) => {
        //assign the HTML of the placeholder form modal to the retrieved form HTML
        document.getElementById("utility-modal-content").innerHTML = data.data
        //update title on the form modal to reflect current form objective
        document.getElementById("utility-modal-label").innerHTML = "Add Project"
        //add a submit listener to the rendered form which will handle the form submission and response.  See Below
        constructFormListener(constructProjectUrl)
    })
}

function constructAddJobForm() {
    const constructJobUrl = `https://portfolio-s6uu.onrender.com/users/${document.querySelector("#user").getAttribute("data-id")}/jobs/add`
    axios.get(constructJobUrl).then((data) => {
        document.getElementById("utility-modal-content").innerHTML = data.data
        document.getElementById("utility-modal-label").innerHTML = "Add Job"
        constructFormListener(constructJobUrl)
    })
}

function constructAddEducationForm() {
    const constructEducationUrl =`https://portfolio-s6uu.onrender.com/users/${document.querySelector("#user").getAttribute("data-id")}/education/add`
    axios.get(constructEducationUrl).then((data) => {
        document.getElementById("utility-modal-content").innerHTML = data.data
        document.getElementById("utility-modal-label").innerHTML = "Add Education"
        constructFormListener(constructEducationUrl)
    })
}

function constructEditProjectForm(projectId) {
    const editProjectUrl = `https://portfolio-s6uu.onrender.com/users/${document.querySelector("#user").getAttribute("data-id")}/projects/${projectId}/edit`
    axios.get(editProjectUrl).then((data) => {
        document.getElementById("utility-modal-content").innerHTML = data.data
        document.getElementById("utility-modal-label").innerHTML = "Edit Project"
        constructFormListener(editProjectUrl)
    })
}

function constructEditUserForm(userId) {
    const editUserUrl = `https://portfolio-s6uu.onrender.com/users/${userId}/edit`
    axios.get(editUserUrl).then((data) => {
        document.getElementById("utility-modal-content").innerHTML = data.data
        document.getElementById("utility-modal-label").innerHTML = "Edit User"
        constructFormListener(editUserUrl)
    })
}

function constructEditJobForm(jobId) {
    const editJobUrl = `https://portfolio-s6uu.onrender.com/users/${document.querySelector("#user").getAttribute("data-id")}/jobs/${jobId}/edit`
    axios.get(editJobUrl).then((data) => {
        document.getElementById("utility-modal-content").innerHTML = data.data
        document.getElementById("utility-modal-label").innerHTML = "Edit Job"
        constructFormListener(editJobUrl)
    })
}


function constructEditEducationForm(degreeId) {
    const editDegreeUrl = `https://portfolio-s6uu.onrender.com/users/${document.querySelector("#user").getAttribute("data-id")}/education/${degreeId}/edit`
    axios.get(editDegreeUrl).then((data) => {
        document.getElementById("utility-modal-content").innerHTML = data.data
        document.getElementById("utility-modal-label").innerHTML = "Edit Education"
        constructFormListener(editDegreeUrl)
    })
}


function constructProjectReadMe(owner_name, project_name, project_title){
    axios.get(`https://api.github.com/repos/${owner_name}/${project_name}/readme`, {headers:{"accept":"application/vnd.github.html+json"}}).then((data) => {
        document.querySelector("#utility-modal-label").innerHTML = project_title
        document.querySelector("#utility-modal-content").innerHTML = data.data
    })
}

//function to submission event listeners to rendered forms
function constructFormListener(url){
    //add event listener to the form
    document.getElementById("form").addEventListener("submit", function(e){
        e.preventDefault()
        //gather form data
        const form = document.getElementById("form")
        const formData = new FormData(form)
        const formDataObject = {}
        //format formData into Object to be submitted with the post request
        formData.forEach((value,key) => {
            formDataObject[key] = value;
        })
        //submit form data to the url passed in.  
        axios.post(url, formDataObject).then((data) =>{
            //if response is okay, reload the page to reflect new changes
            location.reload()
        }).catch((error) => {
            //if an error is thrown, rerender the returned HTML to the placeholder form modal which will be populated with field errors
            console.log(error)
            document.getElementById("utility-modal-content").innerHTML = error.response.data
        })
    })
}