//TODO Considering changing the ReadMe population from an automatic process to a "per click" process.  Unsure of which will lead to fewer API calls at this time.  The "on-Click" call would allow me use only one placeholder modal which would simplify the HTML

//handles population of the user projects page of the profile
document.addEventListener("DOMContentLoaded", function(){
    //gets list of projects from the backend using the "user" div inside of the private_profile html document
    axios.get(`https://portfolio-s6uu.onrender.com/api/projects/${document.querySelector("#user").getAttribute("data-id")}`)
        .then((projects) => {
            //checks to see if there are any projects available
            if(projects.data.length > 0){
            //if there are projects returned
                projects.data.forEach(project => {
                //queries the GitHub API to retrieve Language information
                    axios.get(`https://api.github.com/repos/${project["owner_name"]}/${project["project_name"]}/languages`).then((data) =>{
                    //creates chart with language information and adds it to the page
                    document.getElementById("chart-container").innerHTML = `<canvas id="composition-${project.id}"style="min-height:23vh; min-width:23vh; margin:auto;"></canvas>`
                    createChart(data, project)})
                })
            }
        })
        //console log errors
        .catch((error) => {
            console.log(error)
        })
})

//Using Chart.JS, create chart for the languages associated with the project
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
