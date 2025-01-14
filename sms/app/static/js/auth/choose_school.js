



document.addEventListener("DOMContentLoaded", function () {
    const nextButton = document.getElementById("nextButton");
    const schoolIdInput = document.getElementById("schoolIdInput");
    const schoolDetails = document.getElementById("schoolDetails");
    const schoolName = document.getElementById("schoolName");
    const locationText = document.getElementById("locationText");
    const schoolInfo = document.getElementById("schoolInfo");
    const schoolLogo = document.getElementById("schoolLogo");
    const errorMessage = document.getElementById("errorMessage");
    const accordionHeaders = document.querySelectorAll(".accordion-header");
  
    schoolDetails.classList.add("hidden");
    
    // Accordion toggle functionality
    accordionHeaders.forEach((header) => {
      header.addEventListener("click", function () {
        const content = this.nextElementSibling;
        const icon = this.querySelector("svg");
  
        if (content.style.display === "block") {
          content.style.display = "none";
          icon.classList.remove("rotate-180");
        } else {
          document.querySelectorAll(".accordion-content").forEach((c) => (c.style.display = "none"));
          document.querySelectorAll(".accordion-header svg").forEach((i) => i.classList.remove("rotate-180"));
  
          content.style.display = "block";
          icon.classList.add("rotate-180");
        }
      });
    });
  
    // Next button functionality
    nextButton.addEventListener("click", function () {
      performSearch();
    });
  
    function performSearch() {
      const schoolId = schoolIdInput.value.trim();
  
      // Validate input
      if (!schoolId) {
        showError("Invalid School ID. Please try again.");
        return;
      }
  
      // API call to fetch school details
      fetch(`/api/schools?schoolID=${schoolId}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("School not found");
          }
          return response.json();
        })
        .then((data) => {
          // Display school details on successful response
          errorMessage.classList.add("hidden");
          schoolDetails.classList.remove("hidden");
  
          // Update school details
          schoolName.textContent = data.name; // Update school name
          locationText.textContent = data.location; // Update location
          schoolLogo.src = data.logo; // Update logo
          schoolLogo.alt = `Logo of ${data.name}`; // Accessible alt text
  
          // Update school information icons
          schoolInfo.innerHTML = `
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
              Type: ${data.type}
            </span>
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-1 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
              Grades: ${data.grades}
            </span>
            <span class="flex items-center">
              <svg class="w-5 h-5 mr-1 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
              Students: ${data.students}
            </span>
          `;
        })
        .catch(() => {
          // Handle errors
          showError("School not found. Please check the School ID and try again.");
          schoolDetails.classList.add("hidden");
        });
    }
  
    function showError(message) {
      errorMessage.textContent = message;
      errorMessage.classList.remove("hidden");
  
      setTimeout(() => {
        errorMessage.classList.add("hidden");
      }, 3000); // Hide the error after 3 seconds
    }
  });
