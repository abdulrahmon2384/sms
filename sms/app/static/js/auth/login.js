

document.addEventListener('DOMContentLoaded', function() {
    loadSchoolInfo();
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const icon = this.querySelector('svg');

            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                icon.classList.remove('rotate-180');
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                icon.classList.add('rotate-180');
            }
        });
    });
});



document.getElementById("loginButton").addEventListener("click", async function (event) {
    event.preventDefault(); 

    // Get the values from the form
    const role = document.getElementById("role").value;
    const userId = document.getElementById("userId").value;
    const password = document.getElementById("password").value;

    // Create the request payload
    const payload = {
        role: role,
        userId: userId,
        password: password
    };


    try {
        // Make an API call to the login endpoint
        const response = await fetch("/api/submit-login-credentials", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        // Parse the response from the API
        const data = await response.json();

        console.log(data)
        // Check if login was successful
        if (response.ok && data.success) {
            // Redirect 
            window.location.href = "/intelleva";
            
        } else {
            // Show an error message if login fails
            showError("errorMessage", data.message)
            // alert(data.message || "Login failed. Please check your credentials.");
        }
    } catch (error) {
        showError("errorMessage", "Internet comnection error")
        console.error("Error during login:", error);
        // alert("An error occurred. Please try again later.");
    }
});


function showError(errorId, outputText) {
    // Get the button and error message element dynamically
    const errorMessage = document.getElementById(errorId);
  
    if (!errorMessage) {
      console.error("Button or error message element not found");
      return;
    }

    errorMessage.textContent = outputText;
    errorMessage.classList.remove("hidden");
    
    setTimeout(() => {
        errorMessage.classList.add("hidden");
    }, 3000); // Hide the error after 3 seconds
}


function loadSchoolInfo() {
    // Fetch data from the API
    fetch("/api/schools?insession=true")
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    console.error("School not found");
                    window.location.href = '/choose-school';
                } else {
                    console.error(`HTTP error: Status ${response.status}`);
                }
                return Promise.reject(`HTTP error: Status ${response.status}`);
            }
            return response.json();
        })
        .then(schoolData => {
            // Populate school details
            const schoolLogo = document.getElementById('schoolLogo');
            schoolLogo.src = schoolData.logo;
            schoolLogo.alt = `${schoolData.name} Logo`;

            const schoolName = document.getElementById('schoolName');
            schoolName.textContent = schoolData.name;

            const schoolLocation = document.getElementById('schoolLocation');
            schoolLocation.textContent = schoolData.location;

            // Additional school info
            const schoolInfoDiv = document.querySelector('.absolute.bottom-0.left-0.right-0');
            const additionalInfo = document.createElement('p');
            additionalInfo.textContent = `${schoolData.type} | ${schoolData.grades[0]} | ${schoolData.students} Students`;
            schoolInfoDiv.appendChild(additionalInfo);
        })
        .catch(error => {
            console.error('Error occurred:', error);
        });
}
