// Chart instances
let subjectsChart, progressChart, comparisonChart, performanceTimeTravelchart;
    

// Fetch performance data
function fetchPerformance(year, term) {
        return {
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
            }
    };

// Populate student information
function populateStudentInfo() {
        updatElementIdContent(
            {  
                performanceStudentName: Data.firstname + " " + Data.lastname,
                performanceProfilePic: Data.IMG,
                performanceStudentId: Data.userID,
                performanceStudentGrade: Data.grade
            }
        )
        
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
    updateCharts(data);

    }


// Function to create an advanced Subjects Chart
function createSubjectsChart(data) {
    // Get the canvas element
    const canvas = document.getElementById('subjectsChart');
    const ctx = canvas.getContext('2d');

    // Destroy existing chart instance if it exists
    if (window.subjectsChart instanceof Chart) {
        window.subjectsChart.destroy();
    }

    // Define gradient for bars
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(20, 184, 166, 0.9)');  // Teal
    gradient.addColorStop(1, 'rgba(20, 184, 166, 0.3)');  // Lighter Teal

    // Create new chart instance
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




const performanceTabContents = {
            overview: document.getElementById("overviewTab"),
            subjects: document.getElementById("subjectsTab"),
            progress: document.getElementById("progressTab"),
            p_timetravel: document.getElementById("performanceTimetravelTab"),
            feedback: document.getElementById("feedbackTab"),
        };
handleTabButtons("studentPerformance", performanceTabContents, ".p-tab-button")


const domElements = {
    pTimeTravelTerm: document.getElementById("performanceTimetravelTerm"),
    pTimeTravelYear: document.getElementById("performanceTimetravelYear"),
    yearSelect: document.getElementById('performanceYearSelect'),
    termSelect: document.getElementById('PerformanceTermSelect'),
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





performanceSelectMappings = {
        schoolTerms: ["PerformanceTermSelect", "performanceTimetravelTerm"],
        currentYear: "performanceYearSelect",
        userYears: "performanceTimetravelYear"
    }

populateSelectElements(Data, performanceSelectMappings)
domElements.pTimeTravelTerm.innerHTML += "<option value='All'>all</option>";
domElements.pTimeTravelYear.addEventListener('change', updateData);
domElements.pTimeTravelTerm.addEventListener('change', updateData);
domElements.termSelect.addEventListener('change', intializePerformanceDashboard);






// Filter handlers
async function intializePerformanceDashboard() {
        const performanceData = fetchPerformance(
            domElements.yearSelect.value,
            domElements.termSelect.value
        );
        
        updatePerformanceData(performanceData);
    }


  


populateStudentInfo();
intializePerformanceDashboard();





// Mock Data Generator
function fetchPerformanceTimeTravelData() {
    return {
        "2023-2024": {
            gpa: 3.8,
            rank: 5,
            credits: 18,
            subjects: [
                { subject: 'Mathematics', grade: 'A', instructor: 'Dr. Smith' },
                { subject: 'Physics', grade: 'B+', instructor: 'Prof. Johnson' },
                { subject: 'Literature', grade: 'A-', instructor: 'Dr. Williams' }
            ],
            terms: {
                "First Term": { gpa: 3.7, credits: 9 },
                "Second Term": { gpa: 3.9, credits: 9 },
                "Third Term": {gpa:3.6, credits: 9}
            },
            timeline: [
                { term: 'First Term', date: '2023-03-15', event: 'Mathematics Excellence Award' },
                { term: 'Second Term', date: '2023-09-20', event: 'Physics Research Project Completion' },
                { term: "Third Term", date: "2023-11-01", event: "developer days"}
            ]
        },
        "2022-2023": {
            gpa: 3.6,
            rank: 8,
            credits: 15,
            subjects: [
                { subject: 'Chemistry', grade: 'B', instructor: 'Prof. Davis' },
                { subject: 'Biology', grade: 'A-', instructor: 'Dr. Wilson' }
            ],
            terms: {
                "First Term": { gpa: 3.5, credits: 6 },
                "Second Term": { gpa: 3.7, credits: 9 },
                "Third Term": { gpa: 3.9, credits: 8}
            },
            timeline: [
                { term: 'First Term', date: '2022-04-10', event: 'Chemistry Lab Certification' },
                { term: 'Second Term', date: '2022-11-05', event: 'Biology Field Research' },
                {term: "Third Term", date: "2023-01-24", event: "House party"}
            ]
        }
    };
}


function initiatePerformanceCharts(subjects) {
    const ctx = document.getElementById('PT-subjectChart').getContext('2d');
    if (performanceTimeTravelchart) performanceTimeTravelchart.destroy();
    
    performanceTimeTravelchart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: subjects.map(s => s.subject),
            datasets: [{
                label: 'Grades',
                data: subjects.map(s => {
                    const grades = { 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3 };
                    return grades[s.grade] || 0;
                }),
                backgroundColor: '#0d9488',
                borderColor: '#115e59',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 4,
                    grid: { color: '#e5e7eb' },
                    ticks: { color: '#6b7280' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#6b7280' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// Populate Data
function updatePTtDisplay(year, term) {
    const data = fetchPerformanceTimeTravelData()[year];
    const termData = term === 'All' ? data : data.terms[term];
    
    // Update Metrics
    document.getElementById('PT-gpaDisplay').textContent = termData.gpa.toFixed(1);
    document.getElementById('PT-rankDisplay').textContent = data.rank;
    document.getElementById('PT-creditsDisplay').textContent = termData.credits;
    
    // Update Chart
    initiatePerformanceCharts(data.subjects);
    
    // Update Table
    const tableBody = document.getElementById('PT-SubjectTable');
    tableBody.innerHTML = data.subjects.map(subject => `
        <tr class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="p-2 dark:text-white">${subject.subject}</td>
            <td class="p-2 dark:text-white">${subject.grade}</td>
            <td class="p-2 dark:text-white">${subject.instructor}</td>
        </tr>
    `).join('');
    
    // Update Timeline
    const timeline = document.getElementById('PT-timeline');
    timeline.innerHTML = data.timeline.map(event => `
        <div class="relative pl-8 border-l-2 border-teal-200 dark:border-teal-800">
            <div class="absolute w-4 h-4 bg-teal-500 rounded-full -left-[9px] top-0"></div>
            <h4 class="text-teal-600 dark:text-teal-400 font-semibold">${event.term}</h4>
            <p class="text-gray-600 dark:text-gray-300">${event.event}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">${new Date(event.date).toLocaleDateString()}</p>
        </div>
    `).join('');
}


function updateData() {
    const year = document.getElementById('performanceTimetravelYear').value;
    const term = document.getElementById('performanceTimetravelTerm').value;
    updatePTtDisplay(year, term);
}


