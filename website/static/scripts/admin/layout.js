function active_sidebar(active) {
    var className = "sidebar__item--" + active;
    var sidebar = document.getElementsByClassName(className);
    console.log(sidebar);
    sidebar[0].classList.add("sidebar__item--active");
}

const checkLogin = () => {
    console.log("Checking login");
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/account/info",
        headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
        },
        success: (response) => {
            if (response.status === "200") {
                console.log(response);
                if (response.profile.fullname !== "") {
                    $("#box-user__name").text(response.profile.fullname);
                    $("#user-welcome__username").text(
                        response.profile.fullname
                    );
                } else {
                    $("#box-user__name").text("User");
                    $("#user-welcome__username").text("User");
                }
                $("#box-user__email").text(response.profile.email);
                $("#box-user__avatar").attr("src", response.profile.avatar);

                $("#box-user__item-logout").css("display", "flex");
                $("#box-user__item-login").css("display", "none");
            } else {
                console.log("Not logged in");
                window.location.href = "/admin/login";
            }
        },
        error: (xhr, status, error) => {
            console.log("Not logged in");
            window.location.href = "/admin/login"; // Chuyển hướng đến trang đăng nhập khi có lỗi
        },
    });
};

const closeBoxUser = () => {
    const boxUser = document.getElementById("box-user");
    boxUser.classList.remove("box-user--show");
};

const openBoxUser = () => {
    const boxUser = document.getElementById("box-user");
    if (boxUser.classList.contains("box-user--show")) {
        boxUser.classList.remove("box-user--show");
    } else {
        boxUser.classList.add("box-user--show");
    }
};

const logout = () => {
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/admin/logout",
        headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
        },
        success: (response) => {
            console.log(response);
            checkLogin();
        },
    });
};
