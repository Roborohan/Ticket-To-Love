const imgDiv = document.querySelector(".profile-pic-div");
const img = document.querySelector("#photo");
const file = document.querySelector("#file");
const uploadBtn = document.querySelector("#uploadBtn");
const form = document.querySelector("form");
  
imgDiv.addEventListener("mouseenter", function(){
    uploadBtn.style.display = "block";
});

imgDiv.addEventListener("mouseleave", function(){
    uploadBtn.style.display = "none";
});

file.addEventListener("change", function(){
    const chooseFile = this.files[0];
    if(chooseFile){
        const reader = new FileReader();
        reader.addEventListener("load", function(){
            img.setAttribute("src", reader.result);
        });
        reader.readAsDataURL(chooseFile);
    }
});

form.addEventListener("submit", function(event){
    event.preventDefault();
    const formData = new FormData();
    formData.append("photo", file.files[0]);
    formData.append("username", document.querySelector("#username").value);
    formData.append("sexuality", document.querySelector("#sexuality").value);
    formData.append("gender", document.querySelector("#gender").value);
    formData.append("bio", document.querySelector("#bio").value);
    fetch("/auth/profile", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // do something with the response from the server
    })
    .catch(error => {
        console.error(error);
        // handle the error
    });
});
