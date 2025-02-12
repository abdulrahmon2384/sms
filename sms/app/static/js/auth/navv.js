document.addEventListener('DOMContentLoaded', () => {
  initializeApp();
});

function initializeApp() {
  fetchUserRole().then(Data => {
    const userRole = Data.role;
    if (!userRole) return;

    // Initialize all cache stores first
    const stateCache = new Map();
    const loadedScripts = new Set();
    const contentCache = new Map();
    const mainContent = document.querySelector('main');

    // Initialize UI components
    lucide.createIcons();
    initializeTheme(document.getElementById('themeToggle'));
    initializeProfileDropdown(Data);
    populateNavigation(userRole);

    // Set up navigation with all required parameters
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
  });
}

// Profile dropdown initialization with data
function initializeProfileDropdown(userData) {
  const profileButton = document.getElementById('profileDropdown');
  const dropdownMenu = document.getElementById('dropdownMenu');
  
  document.querySelector("#profileDropdown img").src = userData.image_link;
  document.querySelector("#fullname").textContent = userData.name;

  profileButton.addEventListener('click', (event) => {
    dropdownMenu.classList.toggle('hidden');
    event.stopPropagation();
  });

  document.addEventListener('click', () => dropdownMenu.classList.add('hidden'));
}

// Navigation setup with proper parameter handling
function setupNavigation({ userRole, mainContent, stateCache, loadedScripts, contentCache }) {
  const navButtons = document.querySelectorAll('nav button');
  let currentPage = 'dashboard';

  // Set initial active state
  document.querySelector(`[data-page="dashboard"]`).classList.add('text-teal-600', 'dark:text-teal-400');

  // Main navigation handler
navButtons.forEach(button => {
  button.addEventListener('click', () => {
      const page = button.dataset.page;
      if (currentPage === page) return;

      // Update button states - Reset all buttons
      navButtons.forEach(btn => {
          btn.classList.remove('text-teal-600', 'dark:text-teal-400', 'bg-teal-100', 'dark:bg-teal-900');
      });

      // Highlight the active button
      button.classList.add('text-teal-600', 'dark:text-teal-400', 'bg-teal-100', 'dark:bg-teal-900');

      // Load content with all required parameters
      loadContent({
          page,
          userRole,
          mainContent,
          stateCache,
          loadedScripts,
          contentCache
      });

      currentPage = page;
  });
});



  // Special AI button handler
  document.getElementById('intelleva-ai')?.addEventListener('click', () => {
    loadContent({
      page: 'AI',
      userRole,
      mainContent,
      stateCache,
      loadedScripts,
      contentCache
    });
  });
}

// Updated loadContent with parameter object destructuring
async function loadContent({ page, userRole, mainContent, stateCache, loadedScripts, contentCache }) {
  try {
    if (stateCache.has(page)) {
      showPage(page, mainContent, stateCache);
      return;
    }

    const content = await fetchContent(page, userRole, contentCache);
    const pageElement = createPageElement(content, mainContent);
    await loadScripts(pageElement, loadedScripts);
    
    stateCache.set(page, pageElement);
    showPage(page, mainContent, stateCache);
  } catch (error) {
    mainContent.innerHTML = `<p class="text-center text-red-500">${error.message}</p>`;
  }
}




// fetchUserRole.js
async function fetchUserRole() {
  try {
    const response = await fetch('/api/current_user_role', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'credentials': 'include' // Add this line
      },
    });

    if (response.ok) {
      const data = await response.json();
      if (data.success && data.role) {
        return data;
      }
    }

    window.location.href = "/login";
    return null;
  } catch (error) {
    console.error('Error fetching user role:', error);
    window.location.href = "/login";
    return null;
  }
}

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

  // Create Navigation Bar
  const navBar = document.createElement('nav');
  navBar.className =
    'fixed bottom-2 left-2 right-2 flex justify-around bg-white/90 dark:bg-gray-900/90 backdrop-blur-md shadow-md border border-gray-200 dark:border-gray-800 py-2 rounded-xl transition-all duration-300';

  // Generate Navigation Items
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

// themeManagement.js
function initializeTheme(themeToggle) {
  const rootElement = document.documentElement;
  const savedTheme = localStorage.getItem("theme") || "light";

  rootElement.classList.toggle('dark', savedTheme === "dark");
  themeToggle.addEventListener("click", () => {
    const isDark = rootElement.classList.toggle('dark');
    localStorage.setItem("theme", isDark ? "dark" : "light");
  });
}