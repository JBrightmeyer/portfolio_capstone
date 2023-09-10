const login_Form = document.getElementById("login-form")
login_Form.addEventListener("submit", async function(event){
    event.preventDefault()
    const formData = new FormData(login_Form);
    try {
        const response = await axios.post("/api/login", formData);
        if (response.status === 200){
            window.location.href=`http://127.0.0.1:5000/private/${response.data.user}`
        }
    } catch (error) {
        console.log(error)
    }
})

const register_Form = document.getElementById("register-form")
register_Form.addEventListener("submit", async function(event){
    event.preventDefault()
    const formData = new FormData(register_Form);
    try{
        const response = await axios.post("/api/register", formData);
        if (response.status === 200){
            window.location.href=`http://127.0.0.1:5000/private/${response.data.user}`
        }
    } catch(error) {
        console.log(error)
    }
})

const login_Tab = document.getElementById("login-tab")
login_Tab.addEventListener("click", function(){
    document.getElementById("title-link").innerHTML = "Login"
})

const home_Tab = document.getElementById("home-tab")
home_Tab.addEventListener("click", function(){
    document.getElementById("title-link").innerHTML = "About This Website"
})

const register_Tab = document.getElementById("register-tab")
register_Tab.addEventListener("click", function(){
    document.getElementById("title-link").innerHTML = "Register"
})