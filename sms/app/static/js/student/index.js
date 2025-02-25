



// Temporay dataset
const data = {
    "profile": {
      "gpa": "3.8",
      "recentScore": "92%",
      "grade": "11th"
    },
    "behavior": {
      "comment": "John consistently demonstrates excellent behavior in class and is always willing to help his peers.",
      "status": "Excellent",
      "teacher": "Ms. Smith",
      "color": "green"
    },
    "attendance": {
      "rate": "95%",
      "present": 57,
      "absent": 2,
      "late": 1
    },
    "grades": [
      { "subject": "Math", "grade": "A+" },
      { "subject": "English", "grade": "B+" },
      { "subject": "Science", "grade": "F" }
    ],
    "assignments": [
      {
        "subject": "Mathematics",
        "details": "Quadratic Equations",
        "due": "May 15"
      },
      {
        "subject": "English Literature",
        "details": "Shakespeare Essay",
        "due": "May 20"
      }
    ],
    "events": [
      {
        "event": "Science Fair",
        "description": "Event",
        "date": "June 1, 2024"
      }
    ],
    "classSchedule": [
      {
        "day": "Mon",
        "8AM": "Math",
        "10AM": "Eng",
        "1PM": "Sci",
        "3PM": "His"
      },
      {
        "day": "Tue",
        "8AM": "Phy",
        "10AM": "Chem",
        "1PM": "Lit",
        "3PM": "P.E."
      }
    ],
    "examSchedule": [
      {
        "date": "May 20",
        "subject": "Mathematics",
        "time": "9-11 AM"
      },
      {
        "date": "May 22",
        "subject": "English Lit",
        "time": "1-3 PM"
      }
    ],
    "testSchedule": [
      {
        "date": "May 15",
        "subject": "Biology Quiz",
        "time": "10-10:30 AM"
      },
      {
        "date": "May 17",
        "subject": "Chemistry Quiz",
        "time": "2-2:30 PM"
      }
    ],
    "community": [
      {
        "author": "Ms. Johnson (Math)",
        "message": "Submit math project by Friday!",
        "sent": "May 1"
      },
      {
        "author": "Principal Adams",
        "message": "School picnic next month.",
        "sent": "Apr 28"
      }
    ],

    "financial": {
      "tuition": {
        "paid": 5000,
        "due": 2000,
      },
      "textbooks": {
        "bought": 8,
        "needed": 2,
      },
      "extraLessons": {
        "paid": 500,
        "due": 100,
      },
    }
  };

// Update the dashboard with data
function updateDashboard(data) {
    // Helper function to set text content
    const setText = (id, text) => {
        const element = document.getElementById(id);
        if (element) element.textContent = text || "N/A";
    };

    // Helper function to hide a section
    const hideSection = (id) => {
        const section = document.getElementById(id);
        if (section) section.classList.add("hidden");
    };

    // Update Profile Info
    updatElementIdContent(
      {
        dashboardProfilePic: Data.IMG,
        teacher: Data.teacher,
        term: Data.currentTerm,
        gpa: data.profile.gpa,
        recent_score: data.profile.recentScore,
        grade: Data.grade,
        year: Data.currentYear
      }
    )
    const FullName = Data.firstname + " " + Data.lastname
    const profileElement = document.getElementById("profile")
    profileElement.innerHTML =  `
            <h2 id="name" class="text-lg font-semibold text-gray-900 dark:text-gray-100">${FullName || "Unknown Name"}</h2>
            <p id="username" class="text-sm text-gray-600 dark:text-gray-400">@${Data.userID || "Unknown Name"}</p>
                   
            `;



    const assignments = data.assignments
    if (assignments) {
      const assignmentDiv = document.getElementById("assignments");
      assignmentDiv.innerHTML = `
  <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
    <!-- Subheading with Icon -->
    <h3 class="text-xl font-semibold text-teal-600 dark:text-teal-400 flex items-center mb-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v8m4-4H8" />
      </svg>
      Assignments
    </h3>

    <!-- Assignment List -->
    <div class="space-y-4">
      ${assignments
        .map(
          (assignment) => `
            <div class="relative bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 shadow-sm hover:shadow-lg transition-all">
              <div class="absolute top-2 right-4 text-sm text-orange-500 font-bold">Due: ${assignment.due}</div>
              <div>
                <p class="font-medium text-gray-900 dark:text-gray-100">${assignment.subject}</p>
                <p class="text-gray-600 dark:text-gray-400">${assignment.details}</p>
              </div>
            </div>
          `
        )
        .join("")}
    </div>
  </div>
`;
    } else {
      hideSection("assig")
    }






    // Update Behavior Section Dynamically
    const behavior = data.behavior; // Assuming `data.behavior` contains the necessary information.
    if (behavior) {
    const behaviorElement = document.getElementById("behavior");

    if (behaviorElement) {
        // Clear existing content
        behaviorElement.innerHTML = "";

        const newContent = `
  <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
    <!-- Subheading with Icon -->
    <h3 class="text-xl font-semibold text-teal-600 dark:text-teal-400 flex items-center mb-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 9l2 2-2 2M10 9l-2 2 2 2m7 3H3m8 6h2a2 2 0 002-2v-6a2 2 0 00-2-2H7a2 2 0 00-2 2v6a2 2 0 002 2h2" />
      </svg>
      Behavior
    </h3>

    <!-- Behavior Content -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <p class="font-medium text-gray-900 dark:text-gray-100">Recent Comment:</p>
        <span class="px-3 py-1 text-xs bg-${behavior.color}-100 text-${behavior.color}-800 dark:bg-${behavior.color}-800 dark:text-${behavior.color}-100 rounded-full">
          ${behavior.status || "N/A"}
        </span>
      </div>

      <p class="text-gray-600 dark:text-gray-400">
        "${behavior.comment || "No comments available."}"
      </p>
      
      <p class="text-gray-500 dark:text-gray-400">
        - ${behavior.teacher || "Unknown Teacher"}
      </p>

      <!-- Additional Section for Positive Behavior (if applicable) -->
      <div class="mt-4 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 20l9-5-3-9-9 5-9-5-3 9 9 5z" />
        </svg>
        <p class="text-sm text-gray-600 dark:text-gray-400">Keep up the great work!</p>
      </div>
    </div>
  </div>
`;

        // Add the new content to the behavior element
        behaviorElement.innerHTML = newContent;
    }
    } else {
        hideSection("bh"); 
    }


    // Update Attendance Section Dynamically
    const attendance = data.attendance; 
    if (attendance) {
        const attendanceElement = document.getElementById("attendance");

        if (attendanceElement) {
            attendanceElement.innerHTML = "";
            attendanceElement.innerHTML = `
            
            <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
    <h3 class="text-lg font-semibold text-teal-600 dark:text-teal-400 mb-4 flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <path d="M15 9a3 3 0 0 1-6 0"></path>
      </svg>
      Attendance Overview
    </h3>
    <div class="flex justify-center mb-6">
      <div class="relative w-32 h-32">
        <svg class="w-full h-full transform -rotate-90">
          <circle cx="50%" cy="50%" r="48%" stroke="#e5e7eb" stroke-width="8" fill="none"></circle>
          <circle cx="50%" cy="50%" r="48%" stroke="teal" stroke-width="8" fill="none" stroke-dasharray="100" stroke-dashoffset="${100 - attendance.rate}" class="transition-all duration-500"></circle>
        </svg>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-lg font-semibold text-teal-600 dark:text-teal-400">${attendance.rate}%</span>
        </div>
      </div>
    </div>
    <div class="grid grid-cols-3 gap-4 text-sm text-center">
      <div>
        <p class="font-medium text-gray-900 dark:text-gray-100">Present</p>
        <p class="text-gray-600 dark:text-gray-400">${attendance.present}</p>
      </div>
      <div>
        <p class="font-medium text-gray-900 dark:text-gray-100">Absent</p>
        <p class="text-gray-600 dark:text-gray-400">${attendance.absent}</p>
      </div>
      <div>
        <p class="font-medium text-gray-900 dark:text-gray-100">Late</p>
        <p class="text-gray-600 dark:text-gray-400">${attendance.late}</p>
      </div>
    </div>
    <div class="mt-6">
      <p class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">Attendance Progress</p>
      <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
        <div class="h-3 rounded-full" style="width: ${attendance.rate}%; background-color: teal;"></div>
      </div>
    </div>
  </div>`;
        }
    } else {
        hideSection("attendance"); 
    }


    // Update Grades Section Dynamically
    const grades = data.grades; 
    if (grades) {
      const newContent = `
  <!-- GPA Donut Chart -->
  <div class="text-center mb-6">
    <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">GPA</p>
    <div class="relative w-32 h-32 mx-auto flex items-center justify-center">
      <svg class="w-full h-full transform">
        <!-- Outer Circle -->
        <circle
          cx="32"
          cy="32"
          r="28"
          fill="none"
          stroke="currentColor"
          stroke-width="4"
          class="text-gray-200 dark:text-gray-700"
        ></circle>

        <!-- Inner Circle with Stroke Dash Offset based on GPA -->
        <circle
          cx="32"
          cy="32"
          r="28"
          fill="none"
          stroke="currentColor"
          stroke-width="4"
          stroke-dasharray="176"
          stroke-dashoffset="0"
          class="text-teal-500"
          style="stroke-dashoffset: calc(176 - (176 * 3.8) / 4)"
        ></circle>

        <!-- GPA Text in the Center -->
        <text
          x="32"
          y="32"
          text-anchor="middle"
          dy="0.3em"
          font-size="1.5rem"
          font-weight="bold"
          fill="currentColor"
          class="text-teal-500"
        >
          3.8
        </text>
      </svg>
    </div>
  </div>

  <!-- Recent Score Progress Bar -->
  <div class="text-center mb-6">
    <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Recent Score</p>
    <div class="relative w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
      <div
        class="h-full bg-teal-500 rounded-full"
        style="width: ${data.profile.recentScore.replace('%', '')}%"
      ></div>
    </div>
    <div class="mt-2">
      <span id="recent_score" class="text-xl font-semibold text-teal-600 dark:text-teal-100">${data.profile.recentScore}</span>
    </div>
  </div>

  <!-- Subject Grades Section -->
  <div class="space-y-2">
    <p class="font-medium text-gray-900 dark:text-gray-100 text-lg mb-2">Subject Grades:</p>
    <div id="grades" class="flex flex-wrap gap-4">
      ${grades
        .map(
          (grade) => `
            <span class="px-4 py-2 bg-teal-100 dark:bg-teal-700 text-teal-700 dark:text-teal-200 rounded-full text-xs font-medium">
              ${grade.subject}: ${grade.grade}
            </span>
          `
        )
        .join("")}
    </div>
  </div>
`;

document.getElementById("performance").innerHTML = newContent;

document.getElementById("performance").innerHTML = newContent;

document.getElementById("performance").innerHTML = newContent;
    
    document.getElementById("performance").innerHTML = newContent;
    } else {
        hideSection("performance"); // Hide the section if no grades data is available
    }

    




    


    // Update Community
    const community = data.community;
    if (community && community.length > 0) {
      const communityDiv = document.getElementById("community");
      communityDiv.innerHTML = `
        <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <!-- Subheading with Icon -->
          <h3 class="text-xl font-semibold text-teal-600 dark:text-teal-400 flex items-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zM9 9h6M9 13h6M9 17h6" />
            </svg>
            Community
          </h3>
          <!-- Community Messages -->
          <ul class="space-y-4">
            ${community
              .map(
                (msg) => `
                  <li class="p-4 border rounded-lg shadow-sm bg-white dark:bg-gray-800">
                    <div class="flex items-center space-x-3">
                      <div class="flex-shrink-0">
                        <div class="w-10 h-10 rounded-full bg-gray-300 dark:bg-gray-700 flex items-center justify-center">
                          <svg class="w-6 h-6 text-gray-500 dark:text-gray-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A12.053 12.053 0 0112 15a12.053 12.053 0 016.879 2.804M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          </svg>
                        </div>
                      </div>
                      <div>
                        <p class="font-medium text-gray-900 dark:text-gray-100">${msg.author}</p>
                        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">"${msg.message}"</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">Sent: ${msg.sent}</p>
                      </div>
                    </div>
                  </li>
                `
              )
              .join("")}
          </ul>
        </div>
      `;
    } else {
        hideSection("comm");
    }


    // Update Financial Overview
    const financial = data.financial;
if (financial ) {
  // Select the container
  const financialContainer = document.getElementById("financial");

  if (financialContainer) {
    // Generate HTML dynamically
    financialContainer.innerHTML = `
      <div class="p-6 bg-white dark:bg-gray-800  rounded-lg shadow-sm">
        <h3 class="text-lg flex items-center font-semibold text-teal-600 dark:text-teal-400 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" x2="12" y1="2" y2="22"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
          </svg>
          Financial Overview
        </h3>
        <ul class="space-y-4">
          ${Object.entries(financial)
            .map(([key, value]) => {
              const details =
                key === "textbooks"
                  ? `Bought: ${value.bought} | Needed: ${value.needed}`
                  : `Paid: $${value.paid} | Due: $${value.due}`;
              return `
                <li class="flex items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg shadow-sm">
                  <div class="flex-shrink-0 w-10 h-10 rounded-full bg-teal-100 dark:bg-teal-700 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-teal-500 dark:text-teal-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path d="M12 2L12 22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                    </svg>
                  </div>
                  <div class="ml-4">
                    <p class="font-medium text-gray-900 dark:text-gray-100">${key.charAt(0).toUpperCase() + key.slice(1)}</p>
                    <p class="text-sm text-gray-600 dark:text-gray-400">${details}</p>
                  </div>
                </li>
              `;
            })
            .join("")}
        </ul>
      </div>
    `
  } else {
    console.error("Error: 'financialContainer' element not found in the DOM.");
  }
} else {
  console.error("Error: 'financial.financial' is undefined or not properly structured.");
}
}

// Rrload the dashboard data while reload
function loadDashboardData(data) {


// Update the schedule Section
const renderSchedule = (schedule, containerId) => {
  const container = document.getElementById(containerId);
  if (!schedule || schedule.length === 0) {
    container.innerHTML = "<p class='text-gray-500 dark:text-gray-400'>No data available</p>";
    return;
  }

  // Extract table headers dynamically from the keys of the first object
  const headers = Object.keys(schedule[0]);

  let tableContent = `
      <div class="overflow-x-auto shadow-md rounded-lg">
          <table class="table-auto w-full text-left border-collapse">
              <thead class="bg-gray-100 dark:bg-gray-800">
                  <tr>
                      ${headers.map(header => `
                          <th class="px-4 py-2 border-b text-gray-700 dark:text-gray-300 font-semibold uppercase">
                              ${header.charAt(0).toUpperCase() + header.slice(1)}
                          </th>`).join('')}
                  </tr>
              </thead>
              <tbody>
  `;

  schedule.forEach(item => {
    tableContent += `
          <tr class="odd:bg-gray-50 even:bg-white dark:odd:bg-gray-700 dark:even:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-600">
              ${headers.map(header => `
                  <td class="border px-4 py-2 text-gray-600 dark:text-gray-300">
                      ${item[header] || '-'}
                  </td>`).join('')}
          </tr>
      `;
  });

  tableContent += `
              </tbody>
          </table>
      </div>`;
  container.innerHTML = tableContent;
};

// Render schedules
renderSchedule(data.classSchedule, "class-schedule");
renderSchedule(data.examSchedule, "exam-schedule");
renderSchedule(data.testSchedule, "test-schedule");


// Tab switching functionality
const tabs = document.querySelectorAll('[data-tab]');
tabs.forEach(tab => {
  tab.addEventListener("click", () => {
      document.querySelectorAll('[id$="-schedule"]').forEach(section => section.classList.add("hidden"));
      document.getElementById(`${tab.dataset.tab}-schedule`).classList.remove("hidden");

      tabs.forEach(tab => tab.classList.remove("border-b-2", "border-teal-600", "dark:border-teal-400"));
      tab.classList.add("border-b-2", "border-teal-600", "dark:border-teal-400");
  });
});

}

// Calling witg the Fake dataset
loadDashboardData(data)
updateDashboard(data)
