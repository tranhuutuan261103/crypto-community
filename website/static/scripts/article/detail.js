const up_view = async (article_id) => {
    const params = {
        article_id: article_id,
    };
    try {
        const response = await fetch("http://127.0.0.1:5000/articles/view", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(params),
        });
        if (!response.ok) {
            throw new Error("Server responded with an error!");
        }
        console.log(response.data);
    } catch (error) {
        console.error("Error:", error);
    }
};
