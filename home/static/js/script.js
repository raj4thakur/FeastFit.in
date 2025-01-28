document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed!");

    // Debug: Check if like buttons exist
    const likeButtons = document.querySelectorAll('.like-button');
    if (likeButtons.length === 0) {
        console.error("No like buttons found in the DOM!");
    } else {
        console.log(`Found ${likeButtons.length} like button(s)`);
    }

    // Like button functionality
    likeButtons.forEach(button => {
        console.log("Attaching click event listener to button:", button);

        button.addEventListener('click', function (event) {
            console.log("Like button clicked!");
            event.preventDefault(); // Prevent default form submission

            // Debugging the button attributes
            const recipeId = this.getAttribute('data-recipe-id');
            const url = this.getAttribute('data-url');
            const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

            console.log("Button attributes:");
            console.log(`Recipe ID: ${recipeId}`);
            console.log(`URL: ${url}`);
            console.log(`CSRF Token: ${csrfToken}`);

            // Toggle the liked state
            const isLiked = this.classList.toggle('liked');
            console.log(`Liked state toggled to: ${isLiked}`);

            // Send AJAX POST request
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ isLiked })
            })
                .then(response => {
                    console.log("Response received from the server:", response);
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Server response data:", data);
                    if (data.success) {
                        const likeCountElement = this.closest('.recipe-card').querySelector('.like-count');
                        likeCountElement.textContent = `${data.like_count} Likes`;
                        console.log("Like count updated to:", data.like_count);
                    } else {
                        console.error("Server error:", data.error || "Unknown error");
                    }
                })
                .catch(error => {
                    console.error("AJAX request failed with error:", error);
                });
        });
    });

    // Blog Slider Functionality
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    const slider = document.querySelector('.blog-slider');
    const slides = document.querySelectorAll('.blog-slide');
    let currentIndex = 0;
    const totalSlides = slides.length;

    console.log("Initializing blog slider functionality");
    console.log(`Total slides found: ${totalSlides}`);

    if (!leftArrow || !rightArrow || !slider) {
        console.error("Slider elements not found in the DOM!");
        return;
    }

    // Update the slider position
    function updateSliderPosition() {
        const offset = -(currentIndex * 33.33); // Adjust slider movement percentage as per layout
        slider.style.transform = `translateX(${offset}%)`;
        console.log(`Slider position updated to index: ${currentIndex}`);
    }

    // Handle left arrow click
    leftArrow.addEventListener('click', () => {
        console.log("Left arrow clicked");
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = totalSlides - 1; // Loop to the last slide
        }
        updateSliderPosition();
    });

    // Handle right arrow click
    rightArrow.addEventListener('click', () => {
        console.log("Right arrow clicked");
        if (currentIndex < totalSlides - 1) {
            currentIndex++;
        } else {
            currentIndex = 0; // Loop to the first slide
        }
        updateSliderPosition();
    });
});
