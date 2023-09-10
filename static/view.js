$(document).ready(function(){
    $("#profile-container").scrollspy({target:"#profile-scroll-bar", rootMargin:"0px 0px -80%", smoothScroll:true, threshold:[0.1] })
    $("#portfolio-nav").addClass("hidden")
})

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
