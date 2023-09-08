
const addProjectButton = document.getElementById("add-project-modal-button")
function constructAddProjectForm() {
    axios.get(`http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/projects/add`).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
    })
}

const addJobButton = document.getElementById("add-job-modal-button")
function constructAddJobForm() {
    axios.get(`http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/jobs/add`).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
    })
}

const addEducationButton = document.getElementById("add-education-modal-button")
function constructAddEducationForm() {
    axios.get(`http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/education/add`).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
    })
}

const editProjectButton = document.getElementById("edit-project-modal-button")
function constructEditProjectForm(projectId) {
    axios.get(`http://127.0.0.1:5000/users/<int:userid>/edit`).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
    })
}

const editUserButton = document.getElementById("edit-user-modal-button")
function constructEditUserForm(userId) {
    axios.get(`http://127.0.0.1:5000/users/${userId}/edit`).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
    })
}

const editJobButton = document.getElementById("edit-job-modal-button")
function constructEditJobForm(jobId) {
    axios.get(`http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/jobs/${jobId}/edit`).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
    })
}


const editEducationButton = document.getElementById("edit-education-modal-button")
function constructEditEducationForm(degreeId) {
    axios.get(`http://127.0.0.1:5000/users/${document.querySelector("#user").getAttribute("data-id")}/education/${degreeId}/edit`).then((data) => {
        document.getElementById("form-modal-content").innerHTML = data.data
    })
}




const profile_button = document.getElementById("profile-tab")

profile_button.addEventListener("click", function(event){
    axios.get("http://127.0.0.1:5000/users/1/projects/add").then((data) => {
        console.log(data)
        document.getElementById("form-content").innerHTML = data.data
        document.getElementById("cancel-button").addEventListener("click", function(event){
            $("#tab-content").addClass("slideMiddleFromLeft")
            $("#tab-content").removeClass("slideLeftFromMiddle")
            $("#form-content").addClass("slideRightFromMiddle")
            $("#form-content").removeClass("slideMiddleFromRight")
        })
})
})