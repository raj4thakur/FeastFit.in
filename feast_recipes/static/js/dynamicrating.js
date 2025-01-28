
document.addEventListener("DOMContentLoaded", () => {
    // Get all rating containers
    const ratingContainers = document.querySelectorAll(".static-rating");

    ratingContainers.forEach(container => {
        const averageRating = parseFloat(container.getAttribute("data-average-rating"));
        const totalReviews = container.getAttribute("data-total-reviews");
        const starsContainer = container.querySelector(".stars");
        const reviewsCount = container.querySelector(".reviews-count");

        // Clear stars container
        starsContainer.innerHTML = "";

        // Generate filled stars
        for (let i = 0; i < Math.floor(averageRating); i++) {
            starsContainer.innerHTML += `<i class="fa fa-star rated"></i>`;
        }

        // Check for half-star
        if (averageRating % 1 !== 0) {
            starsContainer.innerHTML += `<i class="fa fa-star-half-alt rated"></i>`;
        }

        // Generate empty stars
        for (let i = Math.ceil(averageRating); i < 5; i++) {
            starsContainer.innerHTML += `<i class="fa fa-star"></i>`;
        }

        // Display total reviews
        reviewsCount.textContent = `${totalReviews} Reviews`;
    });
});
