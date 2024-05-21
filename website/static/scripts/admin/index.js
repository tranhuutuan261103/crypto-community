let isCrawling = false; // Biến cờ toàn cục để theo dõi trạng thái crawl

window.onbeforeunload = function (e) {
    if (isCrawling) {
        e.preventDefault();
        e.returnValue = ""; // Đặt returnValue là một chuỗi trống để tương thích với Chrome.
        return "Quá trình crawl vẫn đang diễn ra. Bạn có chắc chắn muốn rời đi không?";
    }
};

const closeModalAuth = () => {
    const modalAuth = document.getElementById("modal-auth");
    modalAuth.classList.remove("modal-auth--show");
};

const crawl = async (url, type) => {
    const params = {
        url: url,
        type: type,
    };
    try {
        const response = await fetch("http://127.0.0.1:5000/admin/crawl", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(params),
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data.num_article);
            console.log(data.num_unique);
            return data;
        }
        if (!response.ok) {
            throw new Error("Server responded with an error!");
        }
    } catch (error) {
        console.error("Error:", error);
    }
};

const openModalAuth = async () => {
    isCrawling = true; // Đặt trạng thái crawl thành true khi bắt đầu
    try {
        document.getElementById("btn-close").hidden = true;
        const rows = $(".crawlData__table tr.crawlData__table-row");
        let modalContent = ""; // Prepare a string to hold all the new HTML content
        let numChecked = 0;
        urls = {};
        rows.each(function () {
            const checkbox = $(this).find("input[type='checkbox']");
            if (checkbox.is(":checked")) {
                console.log("Checkbox in this row is checked.");
                numChecked += 1;

                // Retrieve category data from the row
                const iconName = $(this)
                    .find(".fa-solid")
                    .attr("class")
                    .split(" ")[1]; // Assumes the icon's class follows the pattern fa-solid <iconClass>
                var categoryName = $(this).find(
                    ".crawlData__table-row-item--name"
                );
                categoryName = categoryName.text().trim();
                console.log(iconName);
                console.log(categoryName);

                // Append the HTML block for this category
                modalContent += `
                <div class="crawl-item">
                    <i class="fa-solid ${iconName}"></i>
                    <div class="crawl-item__info">
                        <p class="crawl-item__name">${categoryName}</p>
                        <p class="crawl-item__data ${categoryName}">
                            <i class="fa-solid fa-download fa-bounce"></i>
                        </p>
                        <p class="crawl-item__data_duplicate ${categoryName}">
                        </p>
                        <p class="crawl-item__data_unique ${categoryName}">
                        </p>
                    </div>
                </div>`;
                urls[categoryName] = $(this)
                    .find(".crawlData__table-row-item--url")
                    .text();
            } else {
                console.log("Checkbox in this row is not checked.");
            }
        });

        if (numChecked !== 0) {
            const modalAuth = document.getElementById("modal-auth");
            const modalRow = modalAuth.querySelector(".modal-row");
            modalRow.innerHTML = modalContent;
            modalAuth.classList.add("modal-auth--show");
            console.log(urls);
            for (const [key, value] of Object.entries(urls)) {
                data = await crawl(value, key);
                $(`.crawl-item__data.${key}`).text(
                    data.num_article + " articles has been crawled"
                );
                num_exist = data.num_article - data.num_unique;
                $(`.crawl-item__data_duplicate.${key}`).text(
                    num_exist + " articles have existed"
                );
                $(`.crawl-item__data_unique.${key}`).text(
                    data.num_unique +
                        " articles have been saved to the database"
                );
            }
        }
    } catch (error) {
        console.error("Error:", error);
    } finally {
        isCrawling = false; // Đặt trạng thái crawl thành false khi kết thúc
        window.onbeforeunload = null;
        document.getElementById("btn-close").hidden = false;
    }
};
