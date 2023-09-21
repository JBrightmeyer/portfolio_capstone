//TODO Handle forms on unauthenticated homepage more elegantly and similarly to the form submissions in the private_profile page.  Examples of form submission can be found in form-control.js


//Add submit listener to login_form and handle it's submission
const login_Form = document.getElementById("login-form")
login_Form.addEventListener("submit", async function(event){
    event.preventDefault()
    const formData = new FormData(login_Form);
    try {
        //submit login formData to login endpoint
        const response = await axios.post("/api/login", formData);
        if (response.status === 200){
            //redirect to correct location if submission data is correct
            window.location.href=`http://127.0.0.1:5000/private/${response.data.user}`
        }
    } catch (error) {
        //if error is returned, console log it
        console.log(error)
    }
})

//Add submit listener to the register_form and handle it's submission
const register_Form = document.getElementById("register-form")
register_Form.addEventListener("submit", async function(event){
    event.preventDefault()
    const formData = new FormData(register_Form);
    try{
        //submit register formData to register endpoint
        const response = await axios.post("/api/register", formData);
        if (response.status === 200){
            //redirect to correct location if submission data is correct
            window.location.href=`http://127.0.0.1:5000/private/${response.data.user}`
        }
    } catch(error) {
        //if error is returned, console log it
        console.log(error)
    }
})

//edit the responsive side menu to reflect current page
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