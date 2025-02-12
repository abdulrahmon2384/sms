    // Chart instances
    let subjectsChart, progressChart, comparisonChart;
    
    // DOM Elements
    const domElements = {
        studentName: document.getElementById('studentName'),
        studentId: document.getElementById('studentId'),
        yearSelect: document.getElementById('yearSelect'),
        termSelect: document.getElementById('termSelect'),
        gpa: document.getElementById('gpa'),
        classRank: document.getElementById('classRank'),
        attendance: document.getElementById('p-attendance'),
        credits: document.getElementById('credits'),
        strengths: document.getElementById('strengths'),
        areasForImprovement: document.getElementById('areasForImprovement'),
        subjectDetails: document.getElementById('subjectDetails'),
        teacherComments: document.getElementById('teacherComments'),
        upcomingAssessments: document.getElementById('upcomingAssessments')
    };

    // Fetch student information
    async function fetchStudentInfo() {
        return new Promise(resolve => {
            setTimeout(() => resolve({
                name: "John Doe",
                id: "STU-2024-12345",
                years: ["2023-2024", "2022-2023", "2021-2022"],
                terms: ["Spring", "Fall", "Summer"],
                currentYear: "2023-2024",
                currentTerm: "Spring"
            }), 500);
        });
    }

    // Fetch performance data
    async function fetchPerformance(year, term) {
        return new Promise(resolve => {
            setTimeout(() => resolve({
                gpa: 3.89,
                classRank: "12/450",
                attendance: "98.6",
                credits: "128",
                subjects: [
                    { name: "Mathematics", grade: "A", teacher: "Dr. Smith", assessments: "Midterm: 95%", mark: 90},
                    { name: "Physics", grade: "A-", teacher: "Prof. Johnson", assessments: "Lab: 89%" , mark: 86}
                ],
                strengths: ["Analytical Skills", "Research Ability", "Technical Writing"],
                areasForImprovement: ["Time Management", "Public Speaking"],
                comments: [
                    { subject: "Mathematics", text: "Excellent problem-solving skills but needs to work on time management." }
                ],
                assessments: [
                    { subject: "Mathematics", date: "2024-03-15", type: "Final Exam", status: "On Track" }
                ],
                progress: [3.6, 3.7, 3.75, 3.8, 3.82, 3.85],
                comparison: {
                    labels: ["Math", "Science", "English", "History"],
                    student: [92, 88, 95, 85],
                    average: [84, 79, 88, 78]
                }
            }), 500);
        });
    }


    // Populate student information
    function populateStudentInfo(data) {
        domElements.studentName.textContent = data.name;
        domElements.studentId.textContent = `Student ID: ${data.id}`;
        
        // Populate year select
        domElements.yearSelect.innerHTML = data.years
            .map(year => `<option ${year === data.currentYear ? 'selected' : ''}>${year}</option>`);
        
        // Populate term select
        domElements.termSelect.innerHTML = data.terms
            .map(term => `<option ${term === data.currentTerm ? 'selected' : ''}>${term}</option>`);
    }

    // Update performance data
    function updatePerformanceData(data) {
        domElements.classRank.textContent = data.classRank;
        domElements.attendance.textContent = data.attendance;
        animateCounter("gpa", data.gpa);
        animateCounter("credits", data.credits);

        // Function to create styled badges
const createBadge = (text, type = "default") => {
    const colors = {
        default: "bg-teal-500 text-white",
        warning: "bg-yellow-500 text-white"
    };
    return `<span class="px-3 py-1 rounded-full text-sm font-medium ${colors[type]} shadow-md">${text}</span>`;
};

// Populate strengths
domElements.strengths.innerHTML = data.strengths
    .map(strength => createBadge(strength, "default"))
    .join('');

// Populate improvement areas
domElements.areasForImprovement.innerHTML = data.areasForImprovement
    .map(area => createBadge(area, "warning"))
    .join('');

// Function to generate table rows with styling
const createTableRow = (subject) => {
    return `
        <tr class="hover:bg-gray-100 dark:hover:bg-gray-700 transition">
            <td class="px-6 py-4 font-medium text-gray-800 dark:text-gray-200">${subject.name}</td>
            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">${subject.grade}</td>
            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">${subject.teacher}</td>
            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">${subject.assessments}</td>
        </tr>
    `;
};

// Populate subject details dynamically
domElements.subjectDetails.innerHTML = data.subjects.map(createTableRow).join('');


        // Function to create teacher comment cards
const createCommentCard = (comment) => {
    return `
        <div class="flex items-start gap-4 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md border-l-4 border-teal-500">
            <div class="flex-shrink-0">
                <span class="inline-block w-12 h-12 bg-teal-500 text-white font-bold flex items-center justify-center rounded-full">
                    ${comment.subject.charAt(0)}
                </span>
            </div>
            <div>
                <h4 class="text-lg font-semibold text-gray-800 dark:text-gray-200">${comment.subject}</h4>
                <p class="text-gray-600 dark:text-gray-400 italic">"${comment.text}"</p>
            </div>
        </div>
    `;
};

// Update teacher comments section
domElements.teacherComments.innerHTML = data.comments.map(createCommentCard).join('');

// Function to create upcoming evaluation rows with status badges
const createAssessmentRow = (assessment) => {
    const statusColors = {
        "Pending": "bg-yellow-500",
        "Completed": "bg-green-500",
        "Missed": "bg-red-500"
    };
    return `
        <tr class="hover:bg-gray-100 dark:hover:bg-gray-700 transition">
            <td class="px-6 py-4 font-medium text-gray-800 dark:text-gray-200">${assessment.subject}</td>
            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">${assessment.date}</td>
            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">${assessment.type}</td>
            <td class="px-6 py-4">
                <span class="px-3 py-1 rounded-full text-white text-xs font-bold ${statusColors[assessment.status] || 'bg-gray-500'}">
                    ${assessment.status}
                </span>
            </td>
        </tr>
    `;
};

// Update upcoming assessments table
domElements.upcomingAssessments.innerHTML = data.assessments.map(createAssessmentRow).join('');

        // Update charts
        updateCharts(data);
    }


// Function to create an advanced Subjects Chart
function createSubjectsChart(data) {
    // Get the canvas element
    const ctx = document.getElementById('subjectsChart').getContext('2d');

    // Define gradient for bars
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(20, 184, 166, 0.9)');  // Teal
    gradient.addColorStop(1, 'rgba(20, 184, 166, 0.3)');  // Lighter Teal

    // Create new chart
    window.subjectsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.subjects.map(s => s.name),
            datasets: [{
                label: 'Grades',
                data: data.subjects.map(s => parseFloat(s.mark)),
                backgroundColor: gradient,
                borderColor: '#14b8a6',
                borderWidth: 2,
                borderRadius: 10, // Rounded bars
                hoverBackgroundColor: '#0d9488' // Darker teal on hover
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: '#4b5563', // Dark gray text for light mode
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(75, 85, 99, 0.2)' // Light grid lines
                    }
                },
                x: {
                    ticks: {
                        color: '#4b5563' // Dark gray text for light mode
                    },
                    grid: {
                        display: false // Hide vertical grid lines
                    }
                }
            },
            plugins: {
                legend: {
                    display: false // Hides legend for a cleaner look
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Grade: ${context.raw}%`;
                        }
                    },
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderWidth: 1,
                    borderColor: '#14b8a6'
                }
            }
        }
    });
}


function updateCharts(data) {
    // Destroy existing charts before reloading new ones
    [subjectsChart, progressChart, comparisonChart].forEach(chart => {
        if (chart) chart.destroy();
    });

    createSubjectsChart(data);

    // Progress chart (Line Chart)
    progressChart = new Chart(document.getElementById('progressChart'), {
        type: 'line',
        data: {
            labels: ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
            datasets: [{
                label: 'GPA Trend',
                data: data.progress,
                borderColor: '#14b8a6',
                backgroundColor: 'rgba(20, 184, 166, 0.2)',
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: '#14b8a6',
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#14b8a6' } }
            },
            scales: {
                x: { ticks: { color: '#6b7280' }, grid: { display: false } },
                y: { ticks: { color: '#6b7280' }, grid: { color: 'rgba(156, 163, 175, 0.2)' } }
            }
        }
    });

    // Comparison chart (Radar Chart)
    comparisonChart = new Chart(document.getElementById('comparisonChart'), {
        type: 'radar',
        data: {
            labels: data.comparison.labels,
            datasets: [{
                label: 'Student',
                data: data.comparison.student,
                backgroundColor: 'rgba(20, 184, 166, 0.2)',
                borderColor: '#14b8a6',
                pointBackgroundColor: '#14b8a6'
            }, {
                label: 'Class Average',
                data: data.comparison.average,
                backgroundColor: 'rgba(156, 163, 175, 0.2)',
                borderColor: '#9ca3af',
                pointBackgroundColor: '#9ca3af'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#14b8a6' } }
            },
            scales: {
                r: {
                    angleLines: { color: 'rgba(156, 163, 175, 0.3)' },
                    grid: { color: 'rgba(156, 163, 175, 0.2)' },
                    ticks: { color: '#6b7280' }
                }
            }
        }
    });
}


    // Get all tab buttons and tab content divs
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = {
            overview: document.getElementById("overviewTab"),
            subjects: document.getElementById("subjectsTab"),
            progress: document.getElementById("progressTab"),
            feedback: document.getElementById("feedbackTab"),
        };
    
    // Function to handle tab switching
    function switchTab(event) {
            const selectedTab = event.target.getAttribute("data-tab");
    
            // Remove active styles from all buttons
            tabButtons.forEach(button => {
                button.classList.remove("text-teal-600", "dark:text-teal-400", "border-teal-500");
                button.classList.add("text-gray-600", "dark:text-gray-400", "hover:text-teal-600", "dark:hover:text-teal-300");
                button.classList.remove("border-b-2");
            });
    
            // Hide all tab contents
            Object.values(tabContents).forEach(content => {
                content.classList.add("hidden");
            });
    
            // Show the selected tab content and highlight the active button
            if (tabContents[selectedTab]) {
                tabContents[selectedTab].classList.remove("hidden");
            }
    
            // Add active styles to the clicked button
            event.target.classList.add("text-teal-600", "dark:text-teal-400", "border-teal-500", "border-b-2");
            event.target.classList.remove("text-gray-600", "dark:text-gray-400", "hover:text-teal-600", "dark:hover:text-teal-300");
        }
    
        // Add click event listeners to each tab button
        tabButtons.forEach(button => {
            button.addEventListener("click", switchTab);
        });


    
    // Filter handlers
    async function handleFilterChange() {
        const performanceData = await fetchPerformance(
            domElements.yearSelect.value,
            domElements.termSelect.value
        );
        updatePerformanceData(performanceData);
    }

    // Initialization
    async function initializeDashboard() {
        const studentInfo = await fetchStudentInfo();
        populateStudentInfo(studentInfo);
        
        const performanceData = await fetchPerformance(
            studentInfo.currentYear,
            studentInfo.currentTerm
        );
        
        updatePerformanceData(performanceData);
        
        // Event listeners
        domElements.yearSelect.addEventListener('change', handleFilterChange);
        domElements.termSelect.addEventListener('change', handleFilterChange);
        
        
    }

    // Function to animate counters
function animateCounter(id, target) {
    let element = document.getElementById(id);
    let count = 0;
    let speed = Math.max(20, 2000 / target); // Adjust speed based on number size

    function updateCounter() {
        if (count < target) {
            count += Math.ceil(target / 100);
            element.textContent = count;
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }

    updateCounter();
}



    // Start the dashboard
    initializeDashboard();