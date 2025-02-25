// Global variables
const chartInstances = new Map();
let AttendanceTabButtons = false;
let PerformanceTabButtons = false;
let tabButtons = null;
let Data = {};
let studentAttendanceChart, studentPunctualityChart;







// Reuseable functions 
function switchTab(event, tabContents) {
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
};



function populateSelectElements(data, mappings) {
  Object.entries(mappings).forEach(([key, selectIds]) => {
      // Ensure selectIds is always treated as an array
      const ids = Array.isArray(selectIds) ? selectIds : [selectIds];

      ids.forEach(selectId => {
          const selectElement = document.getElementById(selectId);
          if (!selectElement) return; // Skip if the element doesn't exist

          if (key === "currentYear") {
              // Populate the currentYear dropdown with only the current year
              selectElement.innerHTML = `<option value="${data.currentYear}" selected>${data.currentYear}</option>`;
          } else if (key === "schoolTerms") {
            if (selectId.includes("Timetravel")) {
              // For timetravel selects: add a default "Select" option and no term is pre-selected
              selectElement.innerHTML = `<option value="" selected>Select</option>` +
                data.schoolTerms
                  .map(term => `<option value="${term.name}">${term.name}</option>`)
                  .join("");
            } else {
              // For other selects: mark the current term as selected
              selectElement.innerHTML = data.schoolTerms
                .map(term => `<option value="${term.name}" ${term.name === data.currentTerm ? 'selected' : ''}>${term.name}</option>`)
                .join("");
            }

          } else if (key === "userYears") {
              // Populate all userYears dropdowns but exclude currentYear
              selectElement.innerHTML = data.userYears
                  .filter(year => year !== data.currentYear)
                  .map(year => `<option value="${year}">${year}</option>`)
                  .join("");
          }
      });
  });
}

function handleTabButtons(pagename, tabContents, tabButtonId) {
  // If the handler is already initialized, exit the function
  if (PerformanceTabButtons && AttendanceTabButtons) {
      console.log("Handler is already initialized.");
      return;
  }

  tabButtons = document.querySelectorAll(tabButtonId);

  if (!tabButtons || tabButtons.length === 0) {
      console.error("No tab buttons found!"); // Show an error
      return;
  }

  tabButtons.forEach(button => {
    button.addEventListener("click", (event) => switchTab(event, tabContents));
    });;

  if (pagename === "studentAttendance"){
    AttendanceTabButtons = true;
  } else if (pagename === "studentPerformance"){
    PerformanceTabButtons = true;
  }
}

function addEventListenerOnce(elementId, eventType, callback) {
  const element = document.getElementById(elementId);
  if (!element) return;

  if (!element.dataset.listenerAdded) {  // Check if listener is already added
      element.addEventListener(eventType, callback);
      element.dataset.listenerAdded = "true"; // Mark as added
  }
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
// end of Reuseable functions





function updatElementIdContent(data) {
  Object.entries(data).forEach(([id, value]) => {
      let element = document.getElementById(id);
      if (element && value !== null && value !== undefined) {
          // Check if the element is an image (or any element that requires src update)
          if (element.tagName === "IMG") {
              element.src = value;
          } else {
              element.textContent = value;
          }
      }
  });
}


// Profile dropdown initialization
function initializeProfileDropdown() {
  const profileButton = document.getElementById('profileDropdown');
  const dropdownMenu = document.getElementById('dropdownMenu');
  
  
  updatElementIdContent(
    {
      firstname: Data.firstname,
      IMG: Data.IMG
    }
  )


  const clickHandler = (event) => {
    dropdownMenu.classList.toggle('hidden');
    event.stopPropagation();
  };

  profileButton.addEventListener('click', clickHandler);
  document.addEventListener('click', () => dropdownMenu.classList.add('hidden'));

  // Cleanup reference
  return () => {
    profileButton.removeEventListener('click', clickHandler);
  };
}

// Navigation setup
function setupNavigation({ userRole, mainContent, stateCache, loadedScripts, contentCache }) {
  const navButtons = document.querySelectorAll('nav button');
  let currentPage = 'dashboard';

  // Set initial active state
  document.querySelector(`[data-page="dashboard"]`).classList.add('text-teal-600', 'dark:text-teal-400');

  const clickHandlers = new Map();

  navButtons.forEach(button => {
    const handler = () => {
      const page = button.dataset.page;
      if (currentPage === page) return;

      // Cleanup previous page resources
      // cleanupPageResources(currentPage);

      // Update button states
      navButtons.forEach(btn => {
        btn.classList.remove('text-teal-600', 'dark:text-teal-400', 'bg-teal-100', 'dark:bg-teal-900');
      });

      button.classList.add('text-teal-600', 'dark:text-teal-400', 'bg-teal-100', 'dark:bg-teal-900');

      loadContent({
        page,
        userRole,
        mainContent,
        stateCache,
        loadedScripts,
        contentCache
      });

      currentPage = page;
    };

    button.addEventListener('click', handler);
    clickHandlers.set(button, handler);
  });

  // Special AI button handler
  const aiButton = document.getElementById('intelleva-ai');
  if (aiButton) {
    const aiHandler = () => {
      cleanupPageResources(currentPage);
      loadContent({
        page: 'AI',
        userRole,
        mainContent,
        stateCache,
        loadedScripts,
        contentCache
      });
      currentPage = 'AI';
    };
    aiButton.addEventListener('click', aiHandler);
    clickHandlers.set(aiButton, aiHandler);
  }

  // Cleanup function
  return () => {
    navButtons.forEach(button => {
      button.removeEventListener('click', clickHandlers.get(button));
    });
    if (aiButton) {
      aiButton.removeEventListener('click', clickHandlers.get(aiButton));
    }
  };
}


// Load content with cleanup
async function loadContent({ page, userRole, mainContent, stateCache, loadedScripts, contentCache }) {
  try {
    if (stateCache.has(page)) {
      showPage(page, mainContent, stateCache);
      return;
    }

    const content = await fetchContent(page, userRole, contentCache);
    const pageElement = createPageElement(content, mainContent);
    await loadScripts(pageElement, loadedScripts);
    
    // Track chart instances
    const charts = Array.from(pageElement.querySelectorAll('canvas'))
      .map(canvas => Chart.getChart(canvas))
      .filter(chart => chart);
    chartInstances.set(page, charts);

    stateCache.set(page, pageElement);
    showPage(page, mainContent, stateCache);
  } catch (error) {
    mainContent.innerHTML = `<p class="text-center text-red-500">${error.message}</p>`;
  }
}


// fetchUserRole.js
function fetchUserRole() {
  return {
    success: true,
    role: "student",
    firstname: "Abdulrahmon",
    lastname: "Otubu",
    currentTerm: "Second Term",
    teacher: "Ms. Smith",
    grade: "Ss2",
    currentYear: "2024-2025",
    userID: "Abdul2384",
    IMG: "https://f005.backblazeb2.com/file/School-management-system/default.png",
    schoolTerms : [
      { name: "First Term"},
      { name: "Second Term"},
      { name: "Third Term"},
      ],
    userYears: ["2022-2023", "2023-2024", "2024-2025", "2025-2026"]
  }};


function populateNavigation(userRole) {
  const navigationConfig = {
    student: [
      { page: "attendance", icon: "calendar-check", label: "Attendance" },
      { page: "grade", icon: "trending-up", label: "Grades" },
      { page: "dashboard", icon: "layout-dashboard", label: "Dashboard" },
      { page: "class", icon: "book-open", label: "Class" },
      { page: "fees", icon: "dollar-sign", label: "Fees" },
    ],
    teacher: [
      { page: "dashboard", icon: "layout-dashboard", label: "Dashboard" },
      { page: "grades", icon: "trending-up", label: "Grades" },
      { page: "attendance", icon: "calendar-check", label: "Attendance" },
      { page: "finance", icon: "dollar-sign", label: "Finance" },
      { page: "class", icon: "book-open", label: "Classes" },
    ],
    admin: [
      { page: "dashboard", icon: "layout-dashboard", label: "Dashboard" },
      { page: "students", icon: "user", label: "Students" },
      { page: "teachers", icon: "user-check", label: "Teachers" },
      { page: "classes", icon: "book-open", label: "Classes" },
      { page: "finance", icon: "dollar-sign", label: "Finance" },
      { page: "schools", icon: "home", label: "Schools" },
    ]
  };

  const navContainer = document.getElementById("nav");
  navContainer.innerHTML = '';

  const navBar = document.createElement('nav');
  navBar.className =
    'fixed bottom-2 left-2 right-2 flex justify-around bg-white/90 dark:bg-gray-900/90 backdrop-blur-md shadow-md border border-gray-200 dark:border-gray-800 py-2 rounded-xl transition-all duration-300';

  navigationConfig[userRole]?.forEach(({ page, icon, label }) => {
    const button = document.createElement("button");
    button.className = 
      "flex flex-col items-center p-1 transition-all duration-300 transform hover:scale-105 hover:text-teal-600 dark:hover:text-teal-400";
    button.dataset.page = page;
    
    button.innerHTML = `
      <div class="icon-container flex items-center justify-center w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-800 shadow-sm transition-colors duration-300 hover:bg-teal-100 dark:hover:bg-teal-900">
        <i data-lucide="${icon}" class="h-5 w-5 text-gray-700 dark:text-gray-300"></i>
      </div>
      <span class="text-[11px] mt-1 font-medium text-gray-700 dark:text-gray-300">${label}</span>
    `;

    navBar.appendChild(button);
  });

  navContainer.appendChild(navBar);
  lucide.createIcons({ container: navBar });
}

// preloadContent.js
function preloadContent(userRole, contentCache) {
  const pagesToPreload = getPreloadPages(userRole);
  
  pagesToPreload.forEach(async (page) => {
    if (!contentCache.has(page)) {
      try {
        const response = await fetch(`${userRole}/${page}`);
        if (response.ok) {
          const content = await response.text();
          contentCache.set(page, content);
        }
      } catch (error) {
        console.error(`Error preloading ${page}:`, error);
      }
    }
  });
}

// Helpers.js
function getPreloadPages(userRole) {
  const role = userRole.toLowerCase();
  if (role === "student") {
    return ["dashboard", "attendance", "grade", "class", "fees", "profile", "communication", "AI"];
  }
  if (role === "teacher") {
    return ["dashboard", "attendance", "grades", "class", "finance", "profile", "communication", "AI"];
  }
  return ["dashboard", "students", "teacher", "classes", "school", "finance", "profile", "communication", "AI"];
}

async function fetchContent(page, userRole, contentCache) {
  if (contentCache.has(page)) {
    return contentCache.get(page);
  }
  
  const response = await fetch(`${userRole}/${page}`);
  if (!response.ok) throw new Error(`Failed to load ${page}: ${response.statusText}`);
  
  const content = await response.text();
  contentCache.set(page, content);
  return content;
}

function createPageElement(content, mainContent) {
  const pageElement = document.createElement('div');
  pageElement.style.display = 'none';
  pageElement.innerHTML = content;
  mainContent.appendChild(pageElement);
  return pageElement;
}

async function loadScripts(container, loadedScripts) {
  const scripts = Array.from(container.querySelectorAll('script'));
  
  for (const script of scripts) {
    if (script.src && loadedScripts.has(script.src)) {
      script.remove();
      continue;
    }

    const newScript = document.createElement('script');
    if (script.src) {
      newScript.src = script.src;
      loadedScripts.add(script.src);
    } else {
      newScript.textContent = script.textContent;
    }
    
    script.replaceWith(newScript);
    await new Promise(resolve => (newScript.onload = resolve));
  }
}

function showPage(page, mainContent, stateCache) {
  Array.from(mainContent.children).forEach(child => {
    child.style.display = child === stateCache.get(page) ? 'block' : 'none';
  });
  lucide.createIcons({ container: stateCache.get(page) });
}

// Theme management
function initializeTheme(themeToggle) {
  const rootElement = document.documentElement;
  const savedTheme = localStorage.getItem("theme") || "light";

  rootElement.classList.toggle('dark', savedTheme === "dark");
  const clickHandler = () => {
    const isDark = rootElement.classList.toggle('dark');
    localStorage.setItem("theme", isDark ? "dark" : "light");
  };
  themeToggle.addEventListener("click", clickHandler);

  // Cleanup reference
  return () => {
    themeToggle.removeEventListener("click", clickHandler);
  };
}


function initializeNavApp() {
  Data = fetchUserRole()
  const userRole = Data.role;
  if (!userRole) return;

  // Initialize all cache stores
  const stateCache = new Map();
  const loadedScripts = new Set();
  const contentCache = new Map();
  const mainContent = document.querySelector('main');

  // Initialize UI components
  lucide.createIcons();
  initializeTheme(document.getElementById('themeToggle'));
  initializeProfileDropdown();
  populateNavigation(userRole);

  // Set up navigation
  setupNavigation({
    userRole,
    mainContent,
    stateCache,
    loadedScripts,
    contentCache
  });

  // Initial load and preload
  loadContent({
    page: 'dashboard',
    userRole,
    mainContent,
    stateCache,
    loadedScripts,
    contentCache
  });
  preloadContent(userRole, contentCache);
};

document.addEventListener('DOMContentLoaded', () => {

  initializeNavApp();
});
