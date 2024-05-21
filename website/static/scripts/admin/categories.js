function toggleIcon(element, status) {
    if (status === true) {
        element.classList.remove("fa-eye-slash");
        element.classList.add("fa-eye");
    } else {
        element.classList.remove("fa-eye");
        element.classList.add("fa-eye-slash");
    }
}

const update_status = async (category_id, status) => {
    const params = {
        category_id: category_id,
        status: status,
    };
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/admin/category/status",
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

const toggle_status = async (element, category_id) => {
    element.classList.contains("fa-eye") ? (_status = false) : (_status = true);
    _status_ = await update_status(category_id, _status);
    console.log(_status_);
    toggleIcon(element, _status_);
};
