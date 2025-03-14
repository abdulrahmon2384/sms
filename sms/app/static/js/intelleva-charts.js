// Intelleva Chart.js Configuration and Utilities

// Common chart options for consistent styling
const commonChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        usePointStyle: true,
        boxWidth: 6,
        font: {
          family: "'Inter', sans-serif",
          size: 12
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(31, 41, 55, 0.9)',
      titleFont: {
        family: "'Inter', sans-serif",
        size: 13
      },
      bodyFont: {
        family: "'Inter', sans-serif",
        size: 12
      },
      padding: 10,
      cornerRadius: 4,
      displayColors: true
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          family: "'Inter', sans-serif",
          size: 11
        }
      }
    },
    y: {
      grid: {
        borderDash: [2, 2],
        drawBorder: false
      },
      ticks: {
        font: {
          family: "'Inter', sans-serif",
          size: 11
        }
      }
    }
  }
};

// Color palettes for charts
const chartColors = {
  primary: '#14b8a6', // teal-500
  primaryLight: '#5eead4', // teal-300
  primaryDark: '#0f766e', // teal-700
  secondary: '#4b5563', // gray-600
  secondaryLight: '#9ca3af', // gray-400
  secondaryDark: '#1f2937', // gray-800
  accent: '#f97316', // orange-500
  success: '#10b981', // emerald-500
  warning: '#f59e0b', // amber-500
  danger: '#ef4444', // red-500
  info: '#3b82f6', // blue-500
  // Gradient backgrounds
  gradients: {
    primary: ['rgba(20, 184, 166, 0.2)', 'rgba(20, 184, 166, 0)'],
    success: ['rgba(16, 185, 129, 0.2)', 'rgba(16, 185, 129, 0)'],
    warning: ['rgba(245, 158, 11, 0.2)', 'rgba(245, 158, 11, 0)'],
    danger: ['rgba(239, 68, 68, 0.2)', 'rgba(239, 68, 68, 0)'],
    info: ['rgba(59, 130, 246, 0.2)', 'rgba(59, 130, 246, 0)']
  }
};

// Create gradient for line charts
function createGradient(ctx, colors) {
  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, colors[0]);
  gradient.addColorStop(1, colors[1]);
  return gradient;
}

// Chart initialization functions
function initAttendanceChart(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Present',
        data: data.present,
        borderColor: chartColors.primary,
        backgroundColor: createGradient(ctx, chartColors.gradients.primary),
        borderWidth: 2,
        tension: 0.3,
        fill: true,
        pointBackgroundColor: chartColors.primary,
        pointRadius: 3,
        pointHoverRadius: 5
      }, {
        label: 'Absent',
        data: data.absent,
        borderColor: chartColors.danger,
        backgroundColor: 'transparent',
        borderWidth: 2,
        tension: 0.3,
        fill: false,
        pointBackgroundColor: chartColors.danger,
        pointRadius: 3,
        pointHoverRadius: 5
      }]
    },
    options: {
      ...commonChartOptions,
      plugins: {
        ...commonChartOptions.plugins,
        title: {
          display: true,
          text: 'Attendance Overview',
          font: {
            family: "'Inter', sans-serif",
            size: 16,
            weight: 'bold'
          }
        }
      }
    }
  });
}

function initPerformanceChart(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Current Term',
        data: data.current,
        backgroundColor: chartColors.primary,
        borderRadius: 4,
        barThickness: 12,
        maxBarThickness: 18
      }, {
        label: 'Previous Term',
        data: data.previous,
        backgroundColor: chartColors.secondaryLight,
        borderRadius: 4,
        barThickness: 12,
        maxBarThickness: 18
      }]
    },
    options: {
      ...commonChartOptions,
      plugins: {
        ...commonChartOptions.plugins,
        title: {
          display: true,
          text: 'Academic Performance',
          font: {
            family: "'Inter', sans-serif",
            size: 16,
            weight: 'bold'
          }
        }
      },
      scales: {
        ...commonChartOptions.scales,
        y: {
          ...commonChartOptions.scales.y,
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: function(value) {
              return value + '%';
            }
          }
        }
      }
    }
  });
}

function initFinanceChart(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Income',
        data: data.income,
        borderColor: chartColors.success,
        backgroundColor: createGradient(ctx, chartColors.gradients.success),
        borderWidth: 2,
        tension: 0.4,
        fill: true,
        pointBackgroundColor: chartColors.success,
        pointRadius: 3,
        pointHoverRadius: 5
      }, {
        label: 'Expenses',
        data: data.expenses,
        borderColor: chartColors.danger,
        backgroundColor: createGradient(ctx, chartColors.gradients.danger),
        borderWidth: 2,
        tension: 0.4,
        fill: true,
        pointBackgroundColor: chartColors.danger,
        pointRadius: 3,
        pointHoverRadius: 5
      }]
    },
    options: {
      ...commonChartOptions,
      plugins: {
        ...commonChartOptions.plugins,
        title: {
          display: true,
          text: 'Financial Overview',
          font: {
            family: "'Inter', sans-serif",
            size: 16,
            weight: 'bold'
          }
        }
      },
      scales: {
        ...commonChartOptions.scales,
        y: {
          ...commonChartOptions.scales.y,
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return '$' + value.toLocaleString();
            }
          }
        }
      }
    }
  });
}

function initDoughnutChart(canvasId, data, title) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.labels,
      datasets: [{
        data: data.values,
        backgroundColor: [
          chartColors.primary,
          chartColors.success,
          chartColors.warning,
          chartColors.danger,
          chartColors.info,
          chartColors.secondary
        ],
        borderWidth: 0,
        hoverOffset: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            usePointStyle: true,
            padding: 15,
            font: {
              family: "'Inter', sans-serif",
              size: 12
            }
          }
        },
        title: {
          display: !!title,
          text: title || '',
          font: {
            family: "'Inter', sans-serif",
            size: 16,
            weight: 'bold'
          }
        },
        tooltip: {
          backgroundColor: 'rgba(31, 41, 55, 0.9)',
          titleFont: {
            family: "'Inter', sans-serif",
            size: 13
          },
          bodyFont: {
            family: "'Inter', sans-serif",
            size: 12
          },
          padding: 10,
          cornerRadius: 4,
          displayColors: true
        }
      }
    }
  });
}

// Initialize all charts on page load
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
  
  // Initialize dark mode toggle
  const darkModeToggle = document.getElementById('darkModeToggle');
  if (darkModeToggle) {
    // Check for saved theme preference or respect OS preference
    if (localStorage.getItem('darkMode') === 'true' || 
        (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
      darkModeToggle.checked = true;
    }
    
    // Toggle dark mode
    darkModeToggle.addEventListener('change', function() {
      if (this.checked) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('darkMode', 'true');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('darkMode', 'false');
      }
    });
  }
  
  // Initialize sidebar toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
  const sidebar = document.getElementById('sidebar');
  
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('sidebar-collapsed');
      document.querySelectorAll('.sidebar-text').forEach(el => {
        el.classList.toggle('hidden');
      });
    });
  }
  
  if (mobileSidebarToggle && sidebar) {
    mobileSidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('-translate-x-full');
    });
  }
  
  // Initialize dropdown toggles
  const userDropdownButton = document.getElementById('userDropdownButton');
  const userDropdown = document.getElementById('userDropdown');
  const notificationButton = document.getElementById('notificationButton');
  const notificationDropdown = document.getElementById('notificationDropdown');
  
  if (userDropdownButton && userDropdown) {
    userDropdownButton.addEventListener('click', function() {
      userDropdown.classList.toggle('hidden');
      if (notificationDropdown) {
        notificationDropdown.classList.add('hidden');
      }
    });
  }
  
  if (notificationButton && notificationDropdown) {
    notificationButton.addEventListener('click', function() {
      notificationDropdown.classList.toggle('hidden');
      if (userDropdown) {
        userDropdown.classList.add('hidden');
      }
    });
  }
  
  // Close dropdowns when clicking outside
  document.addEventListener('click', function(event) {
    if (userDropdown && !userDropdown.classList.contains('hidden') && 
        !userDropdown.contains(event.target) && 
        !userDropdownButton.contains(event.target)) {
      userDropdown.classList.add('hidden');
    }
    
    if (notificationDropdown && !notificationDropdown.classList.contains('hidden') && 
        !notificationDropdown.contains(event.target) && 
        !notificationButton.contains(event.target)) {
      notificationDropdown.classList.add('hidden');
    }
  });
});

// Tab switching function
function switchTab(tabGroupId, tabIndex) {
  // Hide all tab contents
  document.querySelectorAll(`[id^="${tabGroupId}-content-"]`).forEach(tab => {
    tab.classList.add('hidden');
  });
  
  // Show the selected tab content
  document.getElementById(`${tabGroupId}-content-${tabIndex}`).classList.remove('hidden');
  
  // Update tab buttons
  document.querySelectorAll(`[id^="${tabGroupId}-tab-"]`).forEach(button => {
    button.classList.remove('border-teal-500', 'text-teal-600', 'dark:text-teal-400');
    button.classList.add('border-transparent', 'text-gray-500', 'hover:text-gray-700', 'hover:border-gray-300', 'dark:text-gray-400', 'dark:hover:text-gray-300', 'dark:hover:border-gray-600');
  });
  
  // Highlight the active tab button
  const activeButton = document.getElementById(`${tabGroupId}-tab-${tabIndex}`);
  activeButton.classList.remove('border-transparent', 'text-gray-500', 'hover:text-gray-700', 'hover:border-gray-300', 'dark:text-gray-400', 'dark:hover:text-gray-300', 'dark:hover:border-gray-600');
  activeButton.classList.add('border-teal-500', 'text-teal-600', 'dark:text-teal-400');
}
