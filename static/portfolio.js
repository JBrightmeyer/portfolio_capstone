document.addEventListener("DOMContentLoaded", function(){

    axios.get(`http://127.0.0.1:5000/api/projects/${document.querySelector("#user").getAttribute("data-id")}`).then((projects) => {
        if(projects.data.length > 0){
        projects.data.forEach(project => {
            console.log(`https://api.github.com/repos/${project["owner_name"]}/${project["project_name"]}/readme`)
            axios.get(`https://api.github.com/repos/${project["owner_name"]}/${project["project_name"]}/readme`, {headers:{"accept":"application/vnd.github.html+json"}}).then((data) =>{
                document.getElementById(`${project["id"]}-readme`).innerHTML = `<div class="col">${(data.data)}</div>`}).then((data) => {
            axios.get(`https://api.github.com/repos/${project["owner_name"]}/${project["project_name"]}/languages`).then((data) =>{
                console.log(document.getElementById("chart-container").innerHTML)
                document.getElementById("chart-container").innerHTML = `<canvas id="composition-${project.id}"style="min-height:23vh; min-width:23vh; margin:auto;"></canvas>`
                createChart(data, project)
            }).catch((error) => {
                console.log(error)
            })
            }).catch((error) => {
                console.log(error)
            })
        })
    }}).catch((error) => {
        console.log("Backend API Connection Error")
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
    Chart.defaults.color = "black"
    new Chart(document.getElementById(`composition-${project["id"]}`), {
        type: 'doughnut',
        indexLabel: "{label} #percent%",
        data: {
            labels: Object.keys(data.data),
            datasets:[
                {
                    label:"Percent of Total",
                    data:Object.values(percentageValues)
                }
            ]
        }
    })
}
