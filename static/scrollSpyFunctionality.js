//Adds functionality for the scrollSpy feature on the user homepage.  Ensures that appropriate side nav-bar categories based on the current tab selected
//TODO either switch other functions to Jquery or remove Jquery from this one to keep consistency 


//Adds scrollSpy for the initially populated page/side-nav
$(document).ready(function(){
    $("#profile-container").scrollspy({target:"#profile-scroll-bar", rootMargin:"0px 0px -80%", smoothScroll:true, threshold:[0.1] })
    $("#portfolio-nav").addClass("hidden")
})

//Alters the side-nav display when another tab is clicked and adds the appropriate scrollSpy
$("#profile-tab").click(function(){
    $("#portfolio-nav").addClass("hidden")
    $("#profile-nav").removeClass("hidden")
    $("#profile-container").scrollspy({target:"#profile-scroll-bar", rootMargin:"0px 0px -80%", smoothScroll:true, threshold:[0.1] })
})
$("#portfolio-tab").click(function(){
    $("#portfolio-nav").removeClass("hidden")
    $("#profile-nav").addClass("hidden")
    $("#portfolio-container").scrollspy({target:"#portfolio-scroll-bar", rootMargin:"0px 0px -80%", smoothScroll:true, threshold:[0.1] })
})
