

function login() {
    var username = document.getElementById("id_username").value;
    var password = document.getElementById("id_password").value;
    var data = {
        "username": username,
        "password": password
    }
    // console.log(data);
    console.log(data);
    $.ajax({
        type: "POST",
        url: "/citizen/login/ajax/",
        headers: { 'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value },
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            if (data.status == "success") {
                window.location.href = "/";
            } else {
                alert("Wrong username or password");
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

