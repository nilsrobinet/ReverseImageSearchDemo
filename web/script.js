

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
            img.height = 300
            document.getElementById("result_1").appendChild(img);
            var img=document.createElement("img");
            img.src=resp[0][1].id
            img.id="picture"
            img.width = 400
            img.height = 300
            document.getElementById("result_2").appendChild(img);
            var img=document.createElement("img");
            img.src=resp[0][2].id
            img.id="picture"
            img.width = 400
            img.height = 300
            document.getElementById("result_3").appendChild(img);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
};

}