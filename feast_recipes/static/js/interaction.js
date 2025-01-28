document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const recipeId = this.dataset.recipeId;
            const url = this.dataset.url;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const likeIcon = this.querySelector('.like-icon');
                    const likeCount = this.querySelector('.like-count');

                    if (data.liked) {
                        likeIcon.textContent = '❤️';
                    } else {
                        likeIcon.textContent = '🤍';
                    }

                    likeCount.textContent = data.likes_count;
                } else {
                    alert(data.message || 'An error occurred');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});