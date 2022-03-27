let doctors;
let detailsection = document.getElementById('pDetail');
let appended = false;
let revealed = false;
let patient = {};
const fetchDoctors = () =>{
    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/getDoctors', true);
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    xhr.send(JSON.stringify({ HID: "ksldhfjshdkjfshgdkjgkbjfkbgsjf" }));
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status == 200) {
            var data = JSON.parse(this.responseText);
            // console.log(data);
            doctors = data;
            avSpecility();
        }
    };

}
const success = () =>{
    document.getElementsByClassName('success')[0].style.display = 'none';
}
function closebox(){
    detailsection.style.display = 'none';
    document.getElementsByClassName('close')[0].style.display = 'none';
}
const config = (data) =>{
    detailsection.style.display = 'flex';
    document.getElementsByClassName('close')[0].style.display = 'flex';
    let b = detailsection.childNodes[1].childNodes
    detailsection.childNodes[0].childNodes[0].src = data['image'];
    for(let j =0;j<b.length;j++){
        // console.log(b[j].childNodes[1]);
        b[j].childNodes[1].innerHTML  = data[Object.keys(data)[j]]
        // console.log(data[j]);
    }
    // avSpecility();
}
function search() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/getPatient', true);
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    xhr.send(JSON.stringify({ pid: document.getElementById('searchPatient').value }));
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status == 200) {
            var data = JSON.parse(this.responseText);
            config(data);
        }
    };
    
}

const avSpecility = () =>{
    let wrap = document.getElementById('selectspacility');
    for(let i=0;i<wrap.childNodes.length;i++){
        wrap.removeChild(wrap.childNodes[i]);
    }
    let a = [];
    for(let i=0;i<Object.keys(doctors).length;i++){
        a.push(doctors[i]['domain'])
    }
    let sel = document.createElement('option');
    sel.innerHTML = "Select Speciality";
    wrap.appendChild(sel);
    for (let i=0;i<a.length;i++){
        let sel = document.createElement('option');
        sel.innerHTML = a.pop();
        wrap.appendChild(sel);
    }
    return "Fetched";
}
const submitTreat = () =>{
    data = {}
    data['PRNO'] = document.getElementById('searchPatient').value;
    for(let i=0;i<Object.keys(doctors).length;i++){
        if(doctors[i]['domain'] == document.getElementById('selectspacility').value){
            data['assert'] = doctors[i]['assert'];
        }
    }
    console.log(data);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/startTreatment', true);
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    xhr.send(JSON.stringify(data));
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status == 200) {
            var data = JSON.parse(this.responseText);
            detailsection.style.display = 'none';
            document.getElementsByClassName('success')[0].style.display = 'flex';
            const myTimeout = setTimeout(success, 1000);

        }
        if (this.status == 500) {
            window.alert("Something went wrong")
        }
    };
}
const startTreat = () =>{
    if( revealed == true){
        document.getElementsByClassName('docdetail')[0].removeChild(document.getElementById('jweybvku'));
        revealed = false;
    }
    let btn = document.createElement("button");
    btn.innerHTML = "Submit";
    btn.setAttribute('onclick','submitTreat()');
    btn.setAttribute('id','jweybvku');
    document.getElementsByClassName('docdetail')[0].appendChild(btn);
    revealed = true;
}
const selectedGenre = () =>{
    if(appended == true){
        document.getElementsByClassName('docdetail')[0].removeChild(document.getElementById('jhsgdfsd'));
        appended = false;
    }
    let sel = document.createElement('select');
    sel.setAttribute('id','jhsgdfsd');
    sel.setAttribute('onchange','startTreat()')
    let spe = document.getElementById('selectspacility').value;
    let ele = document.createElement('option');
    ele.innerHTML = "Select Doctor";
    sel.appendChild(ele);
    for(let i=0;i<Object.keys(doctors).length;i++){
        let ele = document.createElement('option');
        if(doctors[i]['domain'] == spe)
            ele.innerHTML = doctors[i].name;
            sel.appendChild(ele);
    }
    document.getElementsByClassName('docdetail')[0].appendChild(sel);
    appended = true;
}
fetchDoctors();
var input = document.getElementById("searchPatient");
input.addEventListener("keyup", function(event) {
if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("searchbtn").click();
    }
})