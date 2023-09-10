document.addEventListener('DOMContentLoaded', function(){
    document.getElementById("share-button").addEventListener("click", function(){
        
        let text = `http://127.0.0.1:5000/public/${document.getElementById("user").getAttribute("data-id")}`
        const copyContent = async () => {
        try {
        await navigator.clipboard.writeText(text);
        console.log('Content copied to clipboard');
        } catch (err) {
        console.error('Failed to copy: ', err);
        }
  }
  copyContent()
    })
})

