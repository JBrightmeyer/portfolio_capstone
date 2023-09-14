
const addProjectButton = document.getElementById("add-project-modal-button")
function constructAddProjectForm() {
    const constructProjectUrl = `http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/projects/add`
    axios.get(constructProjectUrl).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
        document.getElementById("form-modal-label").innerHTML = "Add Project"
    })
}

const addJobButton = document.getElementById("add-job-modal-button")
function constructAddJobForm() {
    const constructJobUrl = `http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/jobs/add`
    axios.get(constructJobUrl).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
        document.getElementById("form-modal-label").innerHTML = "Add Job"
        constructFormListener(constructJobUrl)
    })
}

const addEducationButton = document.getElementById("add-education-modal-button")
function constructAddEducationForm() {
    const constructEducationUrl =`http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/education/add`
    axios.get(constructEducationUrl).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
        document.getElementById("form-modal-label").innerHTML = "Add Education"
        constructFormListener(constructEducationUrl)
    })
}

const editProjectButton = document.getElementById("edit-project-modal-button")
function constructEditProjectForm(projectId) {
    const editProjectUrl = `http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/projects/${projectId}/edit`
    axios.get(editProjectUrl).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
        document.getElementById("form-modal-label").innerHTML = "Edit Project"
        constructFormListener(editProjectUrl)
    })
}

const editUserButton = document.getElementById("edit-user-modal-button")
function constructEditUserForm(userId) {
    const editUserUrl = `http://127.0.0.1:5000/users/${userId}/edit`
    axios.get(editUserUrl).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
        document.getElementById("form-modal-label").innerHTML = "Edit User"
        constructFormListener(editUserUrl)
    })
}

const editJobButton = document.getElementById("edit-job-modal-button")
function constructEditJobForm(jobId) {
    const editJobUrl = `http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/jobs/${jobId}/edit`
    axios.get(editJobUrl).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
        document.getElementById("form-modal-label").innerHTML = "Edit Job"
        constructFormListener(editJobUrl)
    })
}


const editEducationButton = document.getElementById("edit-education-modal-button")
function constructEditEducationForm(degreeId) {
    const editDegreeUrl = `http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/education/${degreeId}/edit`
    axios.get(editDegreeUrl).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
        document.getElementById("form-modal-label").innerHTML = "Edit Education"
        constructFormListener(editDegreeUrl)
    })
}




function constructFormListener(url){
    document.getElementById("form").addEventListener("submit", function(e){
        e.preventDefault()
        const form = document.getElementById("form")
        const formData = new FormData(form)
        const formDataObject = {}
        formData.forEach((value,key) => {
            formDataObject[key] = value;
        })
        axios.post(url, formDataObject).then((data) =>{
            location.reload()
        }).catch((error) => {
            document.getElementById("form-modal-content").innerHTML = error.response.data
        })
    })
}