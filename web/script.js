
function insert() {
    url = document.getElementById("insertUrl").value;
    console.log("Insert " + url)
    document.getElementById("insertUrl").value  = "";
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/insert?url="+url);
    xhr.send();
}

function deleteUrl(){
    url = document.getElementById("insertUrl").value;
    console.log("Delete " + url)
    document.getElementById("insertUrl").value  = "";
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/delete?url="+url);
    xhr.send();
}

function search () {
    url = document.getElementById('searchUrl').value;
    console.log("Searching for: " + url);
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/search?url="+url);
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
        console.log("Got response")
        if (xhr.readyState == 4 && xhr.status == 200) {
            resp = xhr.response;
            
            var img=document.createElement("img");
            img.src=resp[0][0].id
            img.id="picture"
            img.width = 400
            document.getElementById("result_1").appendChild(img);
            var img=document.createElement("img");
            img.src=resp[0][1].id
            img.id="picture"
            img.width = 400
            document.getElementById("result_2").appendChild(img);
            var img=document.createElement("img");
            img.src=resp[0][2].id
            img.id="picture"
            img.width = 400
            document.getElementById("result_3").appendChild(img);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
};

}