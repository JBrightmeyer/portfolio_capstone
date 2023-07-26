document.addEventListener("DOMContentLoaded", function(){

    //TODO may convert this back to static HTML with loading
    axios.get(`http://127.0.0.1:5000/api/projects/${document.querySelector("#projects").getAttribute("data-id")}`).then((projects) => {
        let html = ""
        projects.data.forEach(project => {
            html += createProject(project)
        });
        document.querySelector("#projects").innerHTML = html
        projects.data.forEach(project => {
        axios.get(`https://api.github.com/repos/${project["owner_name"]}/${project["project_name"]}/readme`).then((data) =>{
            document.getElementById(`${project["id"]}-readme`).innerHTML = `<div class="col">${atob(data.data["content"])}</div>`
        })
        axios.get(`https://api.github.com/repos/${project["owner_name"]}/${project["project_name"]}/languages`).then((data) =>{
            createChart(data, project)
        })
        })
    })
})


function createChart(data, project){
    total = Object.values(data.data).reduce((x,y) => x+y)
    let percentageValues = []
    let i = 0
    for (let key in data.data){
        percentageValues.push(Math.round(data.data[key] / total * 100))
        i++;
    }
    new Chart(document.getElementById(`composition-${project["id"]}`), {
        type: 'doughnut',
        indexLabel: "{label} #percent%",
        data: {
            labels:Object.keys(data.data),
            datasets:[
                {
                    label:"Percent of Total",
                    data:Object.values(percentageValues)
                }
            ]
        }
    })
}

function createProject(project){
    html = `
    <div class="row">
        <div class="col-auto">
            <img src="${project["display_picture_url"]}" alt="temporary picture" style="width:300px; height:200px;">
        </div>
        <div class="col-auto" id="composition-graph-${project["id"]}">
            <div style="width: 200px;">
                <canvas id="composition-${project["id"]}">
                </canvas>
            </div>
        </div>
        <div class="col">
            <div class="row" >
                <h3>${project["title"]}</h3>
            </div>
            <div class="row list-group-item overflow-auto" id="${project["id"]}-decription" style="height:10vh">
                ${project["description"]}
            </div>
            <div class="row mt-2">`
    if (project["github_url"]){
        html += `
        <div class="col">
            <a class="btn btn-success" href="${project["github_url"]}">Github</a>
        </div>
        `
    }
    if (project["website_url"]){
        html += `
        <div class="col">
            <a class="btn btn-success" href="${project["website_url"]}">Website</a>
        </div>
        `
    }
    html += `
    <div class="col">
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#${project["id"]}">
        ReadMe
    </button>
    <!-- Modal -->
    <div class="modal fade" id="${project["id"]}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true" style="height:40vh;">
        <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="staticBackdropLabel">ReadMe for ${project["project_name"]}</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="${project["id"]}-readme">
            </div>
        </div>
        </div>
    </div>
</div>
</div>
</div>
</div>
    `
    return html
}