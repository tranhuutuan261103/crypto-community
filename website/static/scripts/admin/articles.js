const article_detail = async (article_id) => {
    window.location.href = "/admin/" + article_id;
};

function toggleIcon(element, status) {
    if (status === true) {
        element.classList.remove("fa-eye-slash");
        element.classList.add("fa-eye");
    } else {
        element.classList.remove("fa-eye");
        element.classList.add("fa-eye-slash");
    }
}

const update_status_article = async (article_id, status) => {
    const params = {
        article_id: article_id,
        status: status,
    };
    console.log(params);
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/admin/article/status",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(params),
            }
        );
        if (response.ok) {
            const data = await response.json();
            console.log(data.status);
            return data.status;
        }
        if (!response.ok) {
            throw new Error("Server responded with an error!");
        }
    } catch (error) {
        console.error("Error:", error);
    }
};

const toggle_status = async (element, article_id) => {
    element.classList.contains("fa-eye") ? (_status = false) : (_status = true);
    _status_ = await update_status_article(article_id, _status);
    console.log(_status_);
    toggleIcon(element, _status_);
};

function toggleIconHighLight(element, status) {
    if (status === true) {
        element.classList.remove("fa-regular");
        element.classList.add("fa-solid");
        element.classList.add("highlight_icon");
    } else {
        element.classList.remove("fa-solid");
        element.classList.remove("highlight_icon");
        element.classList.add("fa-regular");
    }
}

const update_highlight_article = async (article_id, status) => {
    const params = {
        article_id: article_id,
        status: status,
    };
    console.log(params);
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/admin/article/highlight",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(params),
            }
        );
        if (response.ok) {
            const data = await response.json();
            console.log(data.status);
            return data.status;
        }
        if (!response.ok) {
            throw new Error("Server responded with an error!");
        }
    } catch (error) {
        console.error("Error:", error);
    }
};

const toggle_highlight = async (element, article_id) => {
    element.classList.contains("fa-solid")
        ? (_status = false)
        : (_status = true);
    _status_ = await update_highlight_article(article_id, _status);
    console.log(_status_);
    toggleIconHighLight(element, _status_);
};

var showOnlyHighlighted = 0;

function filterHighLight(element) {
    showOnlyHighlighted += 1;
    if (showOnlyHighlighted > 2) {
        showOnlyHighlighted = 0;
    }

    var i = element.getElementsByTagName("i")[0];

    if (showOnlyHighlighted === 1) {
        i.classList.remove("fa-sort");
        i.classList.add("fa-star");
        i.classList.add("highlight_icon");
    } else if (showOnlyHighlighted === 2) {
        i.classList.remove("fa-solid");
        i.classList.remove("highlight_icon");
        i.classList.add("fa-regular");
    } else {
        i.classList.remove("fa-regular");
        i.classList.add("fa-solid");
        i.classList.add("fa-sort");
    }

    var rows = $(".content-item__table tr.content-item__table-row");

    rows.each(function () {
        var highlightIcon = $(this).find(".highlight_icon").length;

        if (showOnlyHighlighted == 1 && highlightIcon === 0) {
            $(this).hide();
        } else if (showOnlyHighlighted == 2 && highlightIcon === 1) {
            $(this).hide();
        } else {
            $(this).show();
        }
    });
}

var showOnlyDisplayed = 0;

function filterDisplay(element) {
    showOnlyDisplayed += 1;
    if (showOnlyDisplayed > 2) {
        showOnlyDisplayed = 0;
    }

    var i = element.getElementsByTagName("i")[0];

    if (showOnlyDisplayed === 1) {
        i.classList.remove("fa-sort");
        i.classList.add("fa-eye");
    } else if (showOnlyDisplayed === 2) {
        i.classList.remove("fa-eye");
        i.classList.add("fa-eye-slash");
    } else {
        i.classList.remove("fa-eye-slash");
        i.classList.add("fa-sort");
    }

    var rows = $(".content-item__table tr.content-item__table-row");

    rows.each(function () {
        var eyeIcon = $(this).find(".fa-eye").length;
        var eyeSlashIcon = $(this).find(".fa-eye-slash").length;

        if (showOnlyDisplayed == 1 && eyeIcon === 0) {
            $(this).hide();
        } else if (showOnlyDisplayed == 2 && eyeSlashIcon === 0) {
            $(this).hide();
        } else {
            $(this).show();
        }
    });
}
