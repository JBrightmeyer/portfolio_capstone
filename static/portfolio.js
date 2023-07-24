document.addEventListener("DOMContentLoaded", function(){
    axios.get("https://api.github.com/repos/JBrightmeyer/portfolio_capstone/readme").then((data) =>{
        console.log(data["content"])
        document.querySelector(".container").innerHTML = atob(data.data["content"])
    })
})