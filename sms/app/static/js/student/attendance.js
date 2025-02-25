


function fetchStudentAttendanceDataset(term){
  return {
    currentTerm: "Second Term",
    currentDate: new Date(),
    currentTermProgress: 95,
    currentMonthProgress: 60,
    overallAttendance: "90%",
    daysStreak: 15,
    weeklyLog: [
        {day: "Monday", status: "Present"},
        {day: "Tuesday", status: "Absent"},
        {day: "Wednesday", status: "Present (Late)"},
        {day: "Thursday", status: "Present"},
        {day: "Friday", status: "Absent"}
    ],
    status: [
        {
            status: "Present",
            count: 18,
            thisWeek: "+3"
        },
        {
            status: "Absent",
            count: 2,
            thisWeek: "+1"
        },
        {
            status: "Late",
            count: 1,
            thisWeek: "None"
        },
        {
            status: "Event",
            count: 3,
            upcoming: 2
        }
    ],
    Event: [
        "Spring Break (March 15-22)",
        "midterm Break (April 20-21)"
    ],
    topPuntualityStudents: [
        { name: "John Smith", attendance: "98%", streak: "15 days" , image: "https://ui-avatars.com/api/?name=John+Smith&background=random",},
        { name: "Emma Davis", attendance: "95%", streak: "12 days" , image: "https://ui-avatars.com/api/?name=Emma+Davis&background=random"},
        { name: "Michael Chen", attendance: "93%", streak: "10 days" , image: "https://ui-avatars.com/api/?name=Michael+Chen&background=random"},
        { name: "Sarah Wilson", attendance: "92%", streak: "8 days" , image: "https://ui-avatars.com/api/?name=Sarah+Wilson&background=random"}
    ],
    attendanceDataset: {
        "2024-12": {
          "2024-12-01": { "status": "Present", "timeIn": "08:40", "timeOut": "15:30" },
          "2024-12-02": { "status": "Late", "timeIn": "09:05", "timeOut": "15:30" },
          "2024-12-03": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2024-12-04": { "status": "Present", "timeIn": "08:35", "timeOut": "15:30" },
          "2024-12-05": { "status": "Present", "timeIn": "08:45", "timeOut": "15:30" },
          "2024-12-06": { "status": "Late", "timeIn": "09:10", "timeOut": "15:30" },
          "2024-12-07": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2024-12-08": { "status": "Present", "timeIn": "08:37", "timeOut": "15:30" },
          "2024-12-09": { "status": "Present", "timeIn": "08:33", "timeOut": "15:30" },
          "2024-12-10": { "status": "Late", "timeIn": "09:02", "timeOut": "15:30" },
          "2024-12-11": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2024-12-12": { "status": "Present", "timeIn": "08:42", "timeOut": "15:30" },
          "2024-12-13": { "status": "Present", "timeIn": "08:39", "timeOut": "15:30" },
          "2024-12-14": { "status": "Late", "timeIn": "09:11", "timeOut": "15:30" },
          "2024-12-15": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2024-12-16": { "status": "Present", "timeIn": "08:48", "timeOut": "15:30" },
          "2024-12-17": { "status": "Late", "timeIn": "09:06", "timeOut": "15:30" },
          "2024-12-18": { "status": "Present", "timeIn": "08:38", "timeOut": "15:30" },
          "2024-12-19": { "status": "Present", "timeIn": "08:44", "timeOut": "15:30" },
          "2024-12-20": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2024-12-21": { "status": "Late", "timeIn": "09:04", "timeOut": "15:30" },
          "2024-12-22": { "status": "Present", "timeIn": "08:32", "timeOut": "15:30" },
          "2024-12-23": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2024-12-24": { "status": "Present", "timeIn": "08:41", "timeOut": "15:30" },
          "2024-12-25": { "status": "Present", "timeIn": "08:40", "timeOut": "15:30" },
          "2024-12-26": { "status": "Late", "timeIn": "09:09", "timeOut": "15:30" },
          "2024-12-27": { "status": "Present", "timeIn": "08:37", "timeOut": "15:30" },
          "2024-12-28": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2024-12-29": { "status": "Present", "timeIn": "08:43", "timeOut": "15:30" },
          "2024-12-30": { "status": "Late", "timeIn": "09:13", "timeOut": "15:30" },
          "2024-12-31": { "status": "Present", "timeIn": "08:35", "timeOut": "15:30" }
        },
        "2025-01": {
          "2025-01-01": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-01-02": { "status": "Present", "timeIn": "08:45", "timeOut": "15:30" },
          "2025-01-03": { "status": "Late", "timeIn": "09:07", "timeOut": "15:30" },
          "2025-01-04": { "status": "Present", "timeIn": "08:38", "timeOut": "15:30" },
          "2025-01-05": { "status": "Present", "timeIn": "08:42", "timeOut": "15:30" },
          "2025-01-06": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-01-07": { "status": "Late", "timeIn": "09:10", "timeOut": "15:30" },
          "2025-01-08": { "status": "Present", "timeIn": "08:34", "timeOut": "15:30" },
          "2025-01-09": { "status": "Present", "timeIn": "08:33", "timeOut": "15:30" },
          "2025-01-10": { "status": "Late", "timeIn": "09:03", "timeOut": "15:30" },
          "2025-01-11": { "status": "Present", "timeIn": "08:37", "timeOut": "15:30" },
          "2025-01-12": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-01-13": { "status": "Present", "timeIn": "08:39", "timeOut": "15:30" },
          "2025-01-14": { "status": "Late", "timeIn": "09:14", "timeOut": "15:30" },
          "2025-01-15": { "status": "Present", "timeIn": "08:45", "timeOut": "15:30" },
          "2025-01-16": { "status": "Present", "timeIn": "08:46", "timeOut": "15:30" },
          "2025-01-17": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-01-18": { "status": "Late", "timeIn": "09:05", "timeOut": "15:30" },
          "2025-01-19": { "status": "Present", "timeIn": "08:32", "timeOut": "15:30" },
          "2025-01-20": { "status": "Present", "timeIn": "08:38", "timeOut": "15:30" },
          "2025-01-21": { "status": "Late", "timeIn": "09:02", "timeOut": "15:30" },
          "2025-01-22": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-01-23": { "status": "Present", "timeIn": "08:37", "timeOut": "15:30" },
          "2025-01-24": { "status": "Present", "timeIn": "08:43", "timeOut": "15:30" },
          "2025-01-25": { "status": "Late", "timeIn": "09:09", "timeOut": "15:30" },
          "2025-01-26": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-01-27": { "status": "Present", "timeIn": "08:41", "timeOut": "15:30" },
          "2025-01-28": { "status": "Present", "timeIn": "08:35", "timeOut": "15:30" },
          "2025-01-29": { "status": "Late", "timeIn": "09:07", "timeOut": "15:30" },
          "2025-01-30": { "status": "Present", "timeIn": "08:44", "timeOut": "15:30" },
          "2025-01-31": { "status": "Absent", "timeIn": null, "timeOut": null }
        },
        "2025-02": {
          "2025-02-01": { "status": "Late", "timeIn": "09:12", "timeOut": "15:30" },
          "2025-02-02": { "status": "Present", "timeIn": "08:41", "timeOut": "15:30" },
          "2025-02-03": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-02-04": { "status": "Present", "timeIn": "08:40", "timeOut": "15:30" },
          "2025-02-05": { "status": "Late", "timeIn": "09:06", "timeOut": "15:30" },
          "2025-02-06": { "status": "Present", "timeIn": "08:38", "timeOut": "15:30" },
          "2025-02-07": { "status": "Present", "timeIn": "08:45", "timeOut": "15:30" },
          "2025-02-08": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-02-09": { "status": "Present", "timeIn": "08:34", "timeOut": "15:30" },
          "2025-02-10": { "status": "Late", "timeIn": "09:08", "timeOut": "15:30" },
          "2025-02-11": { "status": "Present", "timeIn": "08:32", "timeOut": "15:30" },
          "2025-02-12": { "status": "Present", "timeIn": "08:39", "timeOut": "15:30" },
          "2025-02-13": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-02-14": { "status": "Late", "timeIn": "09:11", "timeOut": "15:30" },
          "2025-02-15": { "status": "Present", "timeIn": "08:43", "timeOut": "15:30" },
          "2025-02-16": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-02-17": { "status": "Present", "timeIn": "08:41", "timeOut": "15:30" },
          "2025-02-18": { "status": "Late", "timeIn": "09:07", "timeOut": "15:30" },
          "2025-02-19": { "status": "Present", "timeIn": "08:35", "timeOut": "15:30" },
          "2025-02-20": { "status": "Present", "timeIn": "08:44", "timeOut": "15:30" },
          "2025-02-21": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-02-22": { "status": "Late", "timeIn": "09:09", "timeOut": "15:30" },
          "2025-02-23": { "status": "Present", "timeIn": "08:37", "timeOut": "15:30" },
          "2025-02-24": { "status": "Present", "timeIn": "08:39", "timeOut": "15:30" },
          "2025-02-25": { "status": "Absent", "timeIn": null, "timeOut": null },
          "2025-02-26": { "status": "Late", "timeIn": "09:13", "timeOut": "15:30" },
          "2025-02-27": { "status": "Present", "timeIn": "08:38", "timeOut": "15:30" },
          "2025-02-28": { "status": "Present", "timeIn": "08:41", "timeOut": "15:30" }
        }
      }};
    }




function renderCalendar() {
        let yearSelect = document.getElementById("attendanceTimetravelYear").value;
        let termSelect = document.getElementById("attendanceTimetravelTerm");
        let calendarBasic = document.getElementById("calendar_basic");
        let presentCount = document.getElementById("presentCount");
        let absentCount = document.getElementById("absentCount");
        let lateCount = document.getElementById("lateCount");
    
        const year = parseInt(yearSelect.split('-')[0], 10);
        const term = termSelect.value;
        const attendanceData = fetchAttendanceTimeTravel(year, term);
    
        // Clear previous calendar and set grid layout
        calendarBasic.innerHTML = "";
        calendarBasic.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-4";
    
        if (!attendanceData.length) {
            calendarBasic.innerHTML = "<p class='text-center text-gray-500 dark:text-gray-400 col-span-full'>No attendance data available for this period.</p>";
            return;
        }
    
        // Organize attendance by month
        const dataByMonth = {};
        attendanceData.forEach((day) => {
            const date = new Date(day.date);
            const key = `${date.getFullYear()}-${date.getMonth()}`;
            if (!dataByMonth[key]) {
                dataByMonth[key] = [];
            }
            dataByMonth[key].push(day);
        });
    
        // Sort months in order
        const sortedMonths = Object.keys(dataByMonth).sort();
    
        // Generate calendar for each month
        sortedMonths.forEach((key) => {
            const [monthYear, monthIndex] = key.split("-").map(Number);
            const firstDay = new Date(monthYear, monthIndex, 1);
            const lastDay = new Date(monthYear, monthIndex + 1, 0);
            const daysInMonth = lastDay.getDate();
    
            // Create month container (card styling)
            const monthCard = document.createElement("div");
            monthCard.className = "bg-white dark:bg-gray-800 shadow-lg rounded-xl p-6 transition-transform duration-200 hover:scale-[1.02] hover:shadow-xl";
    
            // Month title
            const monthTitle = document.createElement("h4");
            monthTitle.className = "text-lg font-bold text-primary-600 dark:text-primary-400 mb-4 text-center";
            monthTitle.textContent = `${firstDay.toLocaleString("default", { month: "long" })} ${monthYear}`;
            monthCard.appendChild(monthTitle);
    
            // Create table for the month
            const table = document.createElement("table");
            table.className = "w-full border-collapse";
    
            // Table header (Mon-Fri)
            const tableHeader = document.createElement("thead");
            const headerRow = document.createElement("tr");
            ["Mon", "Tue", "Wed", "Thu", "Fri"].forEach((day) => {
                const th = document.createElement("th");
                th.className = "p-2 text-center text-xs font-semibold text-gray-600 dark:text-gray-300";
                th.textContent = day;
                headerRow.appendChild(th);
            });
            tableHeader.appendChild(headerRow);
            table.appendChild(tableHeader);
    
            // Table body
            const tableBody = document.createElement("tbody");
    
            // Collect all weekdays with attendance data
            const weekdaysData = [];
            for (let day = 1; day <= daysInMonth; day++) {
                const date = new Date(monthYear, monthIndex, day);
                if (date.getDay() >= 1 && date.getDay() <= 5) { // Mon-Fri
                    const attendanceDay = dataByMonth[key].find(d => 
                        new Date(d.date).getDate() === day
                    );
                    weekdaysData.push({ day, attendanceDay, date });
                }
            }
    
            // Create rows with 5 days each
            for (let i = 0; i < weekdaysData.length; i += 5) {
                const rowDays = weekdaysData.slice(i, i + 5);
                const row = document.createElement("tr");
                
                for (let j = 0; j < 5; j++) {
                    const td = document.createElement("td");
                    td.className = "p-2 text-center transition-colors duration-200";
                    
                    if (rowDays[j]) {
                        const { day, attendanceDay, date } = rowDays[j];
                        const status = attendanceDay?.status;
                        
                        td.className += ` rounded-md cursor-default ${
                            status === 1 
                                ? "bg-green-200 dark:bg-green-800 text-green-700 dark:text-green-300"
                                : status === 0.5 
                                ? "bg-yellow-200 dark:bg-yellow-800 text-yellow-700 dark:text-yellow-300"
                                : status === 0 
                                ? "bg-red-200 dark:bg-red-800 text-red-700 dark:text-red-300"
                                : "bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
                        } hover:opacity-75`;
                        
                        td.textContent = day;
                    } else {
                        td.className += " bg-transparent";
                    }
                    
                    row.appendChild(td);
                }
                tableBody.appendChild(row);
            }
    
            table.appendChild(tableBody);
            monthCard.appendChild(table);
            calendarBasic.appendChild(monthCard);
        });
    
        // Update attendance statistics
        const presentDays = attendanceData.filter((day) => day.status === 1).length;
        const lateDays = attendanceData.filter((day) => day.status === 0.5).length;
        const absentDays = attendanceData.filter((day) => day.status === 0).length;
    
        presentCount.textContent = presentDays;
        lateCount.textContent = lateDays;
        absentCount.textContent = absentDays;
    }


function fetchAttendanceTimeTravel(year, term) {
            const termDates = {
                "First Term": { start: `${year}-01-10`, end: `${year}-04-10` }, // Term 1: Jan 10 - Apr 10
                "Second Term": { start: `${year}-05-05`, end: `${year}-08-05` }, // Term 2: May 5 - Aug 5
                "Third Term": { start: `${year}-09-01`, end: `${year}-12-01` }, // Term 3: Sep 1 - Dec 1
            };
    
            if (!termDates[term]) {
                throw new Error("Invalid term. Choose 1, 2, or 3.");
            }
    
            const { start, end } = termDates[term];
            const data = [];
            let currentDate = new Date(start);
    
            while (currentDate <= new Date(end)) {
                if (currentDate.getDay() !== 0 && currentDate.getDay() !== 6) {
                    // Exclude weekends
                    const status = Math.random();
                    data.push({
                        date: currentDate.toISOString().split("T")[0],
                        status: status < 0.9 ? 1 : status < 0.95 ? 0.5 : 0, // 90% Present, 5% Late, 5% Absent
                    });
                }
                currentDate.setDate(currentDate.getDate() + 1);
            }
    
            return data;
        }


function populateWeeklyLog(data) {
        // Get the tbody element of the weekly log table
        const tbody = document.querySelector("#attendanceSectionWeekly tbody");
    
        // Clear any existing rows in the tbody
        tbody.innerHTML = "";
    
        // Loop through the weeklyLog data and create table rows
        data.weeklyLog.forEach(entry => {
            // Create a new table row
            const row = document.createElement("tr");
    
            // Create and append the day cell
            const dayCell = document.createElement("td");
            dayCell.className = "py-2";
            dayCell.textContent = entry.day;
            row.appendChild(dayCell);
    
            // Create and append the status cell
            const statusCell = document.createElement("td");
    
            // Determine the status badge color based on the status
            let badgeClass;
            if (entry.status.includes("Present")) {
                badgeClass = "bg-green-500";
            } else if (entry.status.includes("Absent")) {
                badgeClass = "bg-red-500";
            } else if (entry.status.includes("Late")) {
                badgeClass = "bg-yellow-500";
            }
    
            // Create the status badge
            const statusBadge = document.createElement("span");
            statusBadge.className = `${badgeClass} text-white px-2 py-1 rounded-full text-xs`;
            statusBadge.textContent = entry.status;
    
            // Append the badge to the status cell
            statusCell.appendChild(statusBadge);
            row.appendChild(statusCell);
    
            // Append the row to the tbody
            tbody.appendChild(row);
        });
    }
    

function AttendanceTermProgressCharts(data) {
        // Extract values from data
        const termProgress = data.currentTermProgress;
        const attendancePercentage = parseInt(data.overallAttendance);
    
        // Get the canvas element
        const ctx = document.getElementById('termProgressChart').getContext('2d');
    
        // Destroy existing chart if it exists
        if (window.termChart) window.termChart.destroy();
    
        // Create the stacked donut chart
        window.termChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Term Progress', 'Attendance'],
                datasets: [
                    {
                        label: 'Term Progress',
                        data: [termProgress, 100 - termProgress],
                        backgroundColor: [
                            'rgba(20, 184, 166, 0.8)', // Teal for term progress
                            'rgba(229, 231, 235, 0.2)' // Light gray for remaining term
                        ],
                        borderColor: [
                            'rgba(20, 184, 166, 1)',
                            'rgba(209, 213, 219, 0.2)'
                        ],
                        borderWidth: 2,
                        weight: 1 // Outer ring (term progress)
                    },
                    {
                        label: 'Attendance',
                        data: [attendancePercentage, 100 - attendancePercentage],
                        backgroundColor: [
                            'rgba(59, 130, 246, 0.8)', // Blue for attendance
                            'rgba(229, 231, 235, 0.2)' // Light gray for remaining attendance
                        ],
                        borderColor: [
                            'rgba(59, 130, 246, 1)',
                            'rgba(209, 213, 219, 0.2)'
                        ],
                        borderWidth: 2,
                        weight: 2 // Inner ring (attendance)
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%', // Adjust the size of the hole in the donut
                plugins: {
                    legend: {
                        display: false // Hide the legend box
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const label = context.dataset.label || '';
                                const value = context.parsed || 0;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    
        // Update text descriptions
        document.getElementById('termProgressText').textContent = `${termProgress}%`;
        document.getElementById('attendanceProgressText').textContent = `${attendancePercentage}%`;
    }
    

function populateCurrentTermAttendanceDetails(data, currentYear) {
        // Update Current Term & Month Info
        document.querySelector('.text-lg.sm\\:text-xl.font-semibold').textContent = `${data.currentTerm} ${currentYear}`;
        document.querySelector('.text-sm.text-gray-600.dark\\:text-gray-400').textContent = data.currentDate.toLocaleString('default', { month: 'long' });
        document.getElementById('monthCompletion').textContent = `${data.currentMonthProgress}% of Month completed`;
    
        // Update Term Progress Bar
        const termProgressBar = document.querySelector('.bg-gradient-to-r.from-teal-500.to-blue-500.dark\\:from-teal-400.dark\\:to-blue-400');
        termProgressBar.style.width = `${data.currentMonthProgress}%`;
        document.querySelector('.absolute.right-2.top-0.text-xs.sm\\:text-sm').textContent = `${data.currentMonthProgress}%`;
    
        
        // Update Attendance Breakdown
        const presentPercentage = (data.status[0].count / (data.status[0].count + data.status[1].count + data.status[2].count)) * 100;
        const absentPercentage = (data.status[1].count / (data.status[0].count + data.status[1].count + data.status[2].count)) * 100;
        const latePercentage = (data.status[2].count / (data.status[0].count + data.status[1].count + data.status[2].count)) * 100;
    
        document.querySelector('.text-green-500.dark\\:text-green-400').textContent = `${presentPercentage.toFixed(0)}%`;
        document.querySelector('.bg-green-500.dark\\:bg-green-400').style.width = `${presentPercentage.toFixed(0)}%`;
    
        document.querySelector('.text-red-500.dark\\:text-red-400').textContent = `${absentPercentage.toFixed(0)}%`;
        document.querySelector('.bg-red-500.dark\\:bg-red-400').style.width = `${absentPercentage.toFixed(0)}%`;
    
        document.querySelector('.text-yellow-500.dark\\:text-yellow-400').textContent = `${latePercentage.toFixed(0)}%`;
        document.querySelector('.bg-yellow-500.dark\\:bg-yellow-400').style.width = `${latePercentage.toFixed(0)}%`;
    
        // Update Days Streak
        document.getElementById('currentStreak').textContent = data.daysStreak;
    
        // Update Attendance Summary
        document.querySelector('.bg-teal-100.dark\\:bg-teal-900 .text-3xl').textContent = data.status[0].count;
        document.querySelector('.bg-teal-100.dark\\:bg-teal-900 .text-xs').textContent = `${data.status[0].thisWeek} this week`;
    
        document.querySelector('.bg-red-100.dark\\:bg-red-900 .text-3xl').textContent = data.status[1].count;
        document.querySelector('.bg-red-100.dark\\:bg-red-900 .text-xs').textContent = `${data.status[1].thisWeek} this week`;
    
        document.querySelector('.bg-yellow-100.dark\\:bg-yellow-900 .text-3xl').textContent = data.status[2].count;
        document.querySelector('.bg-yellow-100.dark\\:bg-yellow-900 .text-xs').textContent = data.status[2].thisWeek;
    
        document.querySelector('.bg-blue-100.dark\\:bg-blue-900 .text-3xl').textContent = data.status[3].count;
        document.querySelector('.bg-blue-100.dark\\:bg-blue-900 .text-xs').textContent = `${data.status[3].upcoming} upcoming`;
    
        // Update Upcoming Events
        document.querySelector('#attendanceEvent span').textContent = data.Event[0];
    
        AttendanceTermProgressCharts(data)
    }
    


function top5Puntuality(topPuntualityStudents){

        // Update top students section
        const topStudentsDiv = document.getElementById('topStudents');
        let topPuntuality = "";

        topPuntualityStudents.forEach(student => {
            topPuntuality += `
            <div class="flex items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:shadow-md transition-shadow">
                <img src="${student.image}" alt="${student.name}" class="w-12 h-12 rounded-full mr-4">
                <div class="flex-grow">
                    <div class="font-semibold text-lg">${student.name}</div>
                    <div class="flex space-x-4 text-sm">
                        <span class="flex items-center text-green-500">
                            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"/>
                            </svg>
                            ${student.attendance}
                        </span>
                        <span class="flex items-center text-blue-500">
                            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5z"/>
                            </svg>
                            ${student.streak}
                        </span>
                    </div>
                </div>
            </div>
        `});

        topStudentsDiv.innerHTML = topPuntuality;

}
    

// Popup functions
function showAttendanceDetails(date, attendanceDataset) {
    if (!date) return;

    const [year, month, day] = date.split('-');
    const monthKey = `${year}-${month}`;
    
    const attendance = attendanceDataset[monthKey]?.[date] || { status: "Unknown", timeIn: "N/A", timeOut: "N/A" };
    const popup = document.getElementById('attendancePopup');
    const overlay = document.getElementById('popupOverlay');

    document.getElementById('popupDate').textContent = new Date(date).toDateString();
    document.getElementById('popupStatus').textContent = `Status: ${attendance.status}`;
    document.getElementById('popupTimeIn').textContent = `Time In: ${attendance.timeIn || 'N/A'}`;
    document.getElementById('popupTimeOut').textContent = `Time Out: ${attendance.timeOut || 'N/A'}`;

    popup.style.display = 'block';
    overlay.style.display = 'block';
};


function closePopup() {
    document.getElementById('attendancePopup').style.display = 'none';
    document.getElementById('popupOverlay').style.display = 'none';
}
   

// Function to create calendar grid structure (only runs once)
function createCalendarStructure() {
    const calendar = document.getElementById('calendar');
    calendar.innerHTML = '';

    // Add day headers
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    dayNames.forEach(day => {
        calendar.innerHTML += `<div class="text-center font-semibold">${day}</div>`;
    });

    // Add 42 calendar cells (6 weeks x 7 days)
    for (let i = 0; i < 42; i++) {
        calendar.innerHTML += `<div class="calendar-day text-center p-2 rounded-md"></div>`;
    }
}


function updateCalendarDays(year, month, attendanceData) {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const calendar = document.getElementById('calendar');
    const dayCells = calendar.querySelectorAll('.calendar-day');
    
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = new Date(year, month, 1).getDay();

    // Update month title
    document.getElementById('currentMonthYear').textContent = `${monthNames[month]} ${year}`;

    const today = new Date();
    const monthKey = `${year}-${(month + 1).toString().padStart(2, '0')}`;

    // Clear all cells before updating
    dayCells.forEach(cell => {
        cell.textContent = '';
        cell.className = 'calendar-day text-center p-2 rounded-md';
    });

    // Add days and attendance status
    for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(year, month, i);
        const dateString = `${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`;
        const attendance = attendanceData[monthKey]?.[dateString] || { status: "Unknown" };

        let statusColor = "bg-gray-100 dark:bg-gray-600";
        if (date <= today) {
            statusColor = attendance.status === "Present" ? "bg-green-100 dark:bg-green-800" :
                        attendance.status === "Late" ? "bg-yellow-100 dark:bg-yellow-800" :
                        attendance.status === "Absent" ? "bg-red-100 dark:bg-red-800" :
                        "bg-gray-100 dark:bg-gray-600";
        }

        const isToday = date.toDateString() === today.toDateString();
        const todayClass = isToday ? "ring-2 ring-blue-500" : "";

        // Find the correct cell based on day offset
        const cellIndex = firstDay + i - 1;
        const cell = dayCells[cellIndex];
        if (cell) {
            cell.textContent = i;
            cell.className = `calendar-day text-center p-2 rounded-md cursor-pointer ${statusColor} ${todayClass}`;
            cell.onclick = () => showAttendanceDetails(dateString, attendanceData);
        }
    }
};



function createCharts(data, ctx1, ctx2) {
if (studentAttendanceChart) studentAttendanceChart.destroy();
if (studentPunctualityChart) studentPunctualityChart.destroy();

studentAttendanceChart = new Chart(ctx1, {
type: 'bar',
data: {
labels: data.map(item => item.label),
datasets: [
{
    label: 'Present',
    data: data.map(item => item.present),
    backgroundColor: 'rgba(75, 192, 192, 0.7)',
    borderColor: 'rgba(75, 192, 192, 1)',
    borderWidth: 1
},
{
    label: 'Late',
    data: data.map(item => item.late),
    backgroundColor: 'rgba(255, 206, 86, 0.7)',
    borderColor: 'rgba(255, 206, 86, 1)',
    borderWidth: 1
},
{
    label: 'Absent',
    data: data.map(item => item.absent),
    backgroundColor: 'rgba(255, 99, 132, 0.7)',
    borderColor: 'rgba(255, 99, 132, 1)',
    borderWidth: 1
}
]
},
options: {
responsive: true,
maintainAspectRatio: false,
scales: {
x: {
    stacked: true,
    ticks: { color: 'rgb(156, 163, 175)' }
},
y: {
    stacked: true,
    beginAtZero: true,
    ticks: { color: 'rgb(156, 163, 175)' }
}
},
plugins: {
legend: { labels: { color: 'rgb(156, 163, 175)' } },
title: { display: true, text: 'Attendance', color: 'rgb(156, 163, 175)' }
}
}
});

studentPunctualityChart = new Chart(ctx2, {
type: 'line',
data: {
labels: data.map(item => item.label),
datasets: [{
label: 'Punctuality Rate',
data: data.map(item => item.punctuality),
fill: false,
borderColor: 'rgb(75, 192, 192)',
tension: 0.2
}]
},
options: {
responsive: true,
maintainAspectRatio: false,
scales: {
x: { ticks: { color: 'rgb(156, 163, 175)' } },
y: {
    beginAtZero: true,
    max: 100,
    ticks: {
        color: 'rgb(156, 163, 175)',
        callback: (value) => value + '%'
    }
}
},
plugins: {
legend: { labels: { color: 'rgb(156, 163, 175)' } },
title: { display: true, text: 'Punctuality Rate', color: 'rgb(156, 163, 175)' }
}
}
});
}



function processAndFilterData(data, timeframe) {
const processedData = [];
const months = Object.keys(data);

if (timeframe === 'monthly') {
months.forEach(month => {
const days = Object.values(data[month]);
processedData.push({
label: month,
present: days.filter(day => day.status === "Present").length,
late: days.filter(day => day.status === "Late").length,
absent: days.filter(day => day.status === "Absent").length,
punctuality: (days.filter(day => day.status === "Present" && day.timeIn <= "08:45").length / days.length) * 100
});
});
} else { // weekly
months.forEach(month => {
const days = Object.entries(data[month]);
let weekCounter = 1;
let weekData = { present: 0, late: 0, absent: 0, onTime: 0, total: 0 };

days.forEach(([date, day], index) => {
weekData.total++;
if (day.status === "Present") weekData.present++;
if (day.status === "Late") weekData.late++;
if (day.status === "Absent") weekData.absent++;
if (day.status === "Present" && day.timeIn <= "08:45") weekData.onTime++;

if ((index + 1) % 7 === 0 || index === days.length - 1) {
processedData.push({
    label: `${month} Week ${weekCounter}`,
    present: weekData.present,
    late: weekData.late,
    absent: weekData.absent,
    punctuality: (weekData.onTime / weekData.total) * 100
});
weekCounter++;
weekData = { present: 0, late: 0, absent: 0, onTime: 0, total: 0 };
}
});
});
}
return processedData;
}


const attendanceTabContents = {
    overview: document.getElementById("attendanceSectionOverview"),
    subjects: document.getElementById("attendanceSectionWeekly"),
    progress: document.getElementById("attendanceSectiontimetravel"),
    feedback: document.getElementById("attendanceSectionAnalysis"),
};


handleTabButtons("studentAttendance", attendanceTabContents, ".a-tab-button")




attendanceSelectMappings = {
    schoolTerms: ["attendanceTermSelect", "attendanceTimetravelTerm"],
    currentYear: "attendanceYearSelect",
    userYears: "attendanceTimetravelYear"
}

populateSelectElements(Data, attendanceSelectMappings)
document.getElementById("attendanceTermSelect").addEventListener('change', InitializeAttendanceApp);
document.getElementById("attendanceTimetravelTerm").addEventListener('change', renderCalendar);
document.getElementById("attendanceTimetravelYear").addEventListener('change', renderCalendar);


updatElementIdContent(
    {  
        attendanceStudentName: Data.firstname + " " + Data.lastname,
        attendanceProfilePic: Data.IMG,
        attendanceStudentId: Data.userID,
        attendanceStudentGrade: Data.grade
    }
)

function InitializeAttendanceApp(){
    term = document.getElementById("attendanceTermSelect").value;
    const data = fetchStudentAttendanceDataset(term);
    let currentDate = data.currentDate
    let currentYear = currentDate.getFullYear();
    let currentMonth = currentDate.getMonth();
    

    const ctx1 = document.getElementById('weeklyattendanceChart').getContext('2d');
    const ctx2 = document.getElementById('weeklypunctualityChart').getContext('2d');
    const timeframeSelect = document.getElementById('timeframe');
    let currentTimeframe = timeframeSelect.value;

    createCalendarStructure();
    populateCurrentTermAttendanceDetails(data, currentYear);
    updateCalendarDays(currentYear, currentMonth, data.attendanceDataset);
    top5Puntuality(data.topPuntualityStudents)
    populateWeeklyLog(data);
    
    let processedData = processAndFilterData(data.attendanceDataset, currentTimeframe);
    createCharts(processedData, ctx1, ctx2);


    
 
    addEventListenerOnce('prevMonth', 'click', () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        updateCalendarDays(currentYear, currentMonth, data.attendanceDataset);
    });
    
    addEventListenerOnce('nextMonth', 'click', () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        updateCalendarDays(currentYear, currentMonth, data.attendanceDataset);
    });
    
    addEventListenerOnce('timeframe', 'change', (event) => {
        currentTimeframe = event.target.value;
        processedData = processAndFilterData(data.attendanceDataset, currentTimeframe);
        createCharts(processedData, ctx1, ctx2);
        console.log("im here ")
    });
}


//Initialize
InitializeAttendanceApp()



