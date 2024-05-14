function enableDragAndDrop(elementId) {
    var element = document.getElementById(elementId);
    var isDragging = false;
    var startX, startY, scrollLeft, scrollTop;
    var scrollSpeed = 3;

    element.addEventListener("mousedown", function (e) {
        isDragging = true;
        startX = e.pageX - element.offsetLeft;
        startY = e.pageY - element.offsetTop;
        scrollLeft = element.scrollLeft;
        scrollTop = element.scrollTop;
    });

    element.addEventListener("mouseleave", function () {
        isDragging = false;
    });

    element.addEventListener("mouseup", function () {
        isDragging = false;
    });

    element.addEventListener("mousemove", function (e) {
        if (!isDragging) return;
        e.preventDefault();
        var x = e.pageX - element.offsetLeft;
        var y = e.pageY - element.offsetTop;
        var walkX = (x - startX) * scrollSpeed;
        var walkY = (y - startY) * scrollSpeed;

        // Check if scrolled to the end
        if (element.scrollLeft + element.clientWidth >= element.scrollWidth) {
            element.scrollLeft = 0; // Scroll back to the beginning
        } else {
            element.scrollLeft = scrollLeft - walkX;
        }

        if (element.scrollTop + element.clientHeight >= element.scrollHeight) {
            element.scrollTop = 0; // Scroll back to the beginning
        } else {
            element.scrollTop = scrollTop - walkY;
        }

        // Check if scrolled to the beginning
        if (element.scrollLeft === 0 && walkX < 0) {
            element.scrollLeft = element.scrollWidth - element.clientWidth;
        }

        if (element.scrollTop === 0 && walkY < 0) {
            element.scrollTop = element.scrollHeight - element.clientHeight;
        }
    });
}
