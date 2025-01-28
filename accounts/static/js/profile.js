document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.nav-link');
    const contentSections = document.querySelectorAll('.content-section');

    // Show General Information section by default
    const defaultSectionId = 'general-info';
    showSection(defaultSectionId);
    setActiveLink(document.querySelector(`.nav-link[href="#${defaultSectionId}"]`));

    navLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const sectionId = this.getAttribute('href').substring(1);
            showSection(sectionId);
            setActiveLink(this); // Set active link
        });
    });

    function showSection(sectionId) {
        // Hide all content sections
        contentSections.forEach(section => {
            section.style.display = 'none';
        });

        // Show the selected section
        const selectedSection = document.getElementById(sectionId);
        if (selectedSection) {
            selectedSection.style.display = 'block';
        }
    }

    function setActiveLink(activeLink) {
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        activeLink.classList.add('active');
    }

    const formGeneralInfo = document.getElementById('form-general-info');
    formGeneralInfo.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(formGeneralInfo);
        // AJAX form submission for General Information form data
        submitFormData(formData, 'profile.php', 'general-info');
        // Optional: Set active link
        setActiveLink(document.querySelector('.nav-link[href="#general-info"]'));
    });

    const formDietaryPrefs = document.getElementById('form-dietary-prefs');
    formDietaryPrefs.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(formDietaryPrefs);
        // AJAX form submission for Dietary Preferences form data
        submitFormData(formData, 'diet_preference.php', 'dietary-prefs');
        // Optional: Set active link
        setActiveLink(document.querySelector('.nav-link[href="#dietary-prefs"]'));
    });

    // Function to submit form data asynchronously using AJAX
    function submitFormData(formData, url, sectionId) {
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            console.log(data); // Log the response data
            showSection(sectionId); // Show the corresponding section after form submission
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
    }
});