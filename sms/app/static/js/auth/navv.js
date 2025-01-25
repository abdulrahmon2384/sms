// Ensure the DOM is fully loaded before execution
document.addEventListener('DOMContentLoaded', () => {
    if (document.readyState === 'complete') {
      initializeApp();
    } else {
      window.addEventListener('load', initializeApp);
    }
  });
  
  // Function to initialize the app
  function initializeApp() {
    // Fetch the user role asynchronously
    fetchUserRole().then(userRole => {
      if (!userRole) return; // Stop execution if user role is not found
  
      lucide.createIcons();
      const themeToggle = document.getElementById('themeToggle');
      const htmlElement = document.documentElement;
  
      const profileButton = document.getElementById('profileDropdown');
      const dropdownMenu = document.getElementById('dropdownMenu');
      populateNavigation(userRole.trim());
  
      // Function to hide dropdown
      const hideDropdown = (event) => {
        if (!dropdownMenu.contains(event.target) && !profileButton.contains(event.target)) {
          dropdownMenu.classList.add('hidden');
        }
      };
  
      // Event listener for profile button
      profileButton.addEventListener('click', (event) => {
        dropdownMenu.classList.remove('hidden');
        event.stopPropagation(); // Prevent event from triggering the document click listener
      });
  
      // Event listener for clicks outside the dropdown
      document.addEventListener('click', hideDropdown);
      dropdownMenu.classList.add('hidden');
  




      const rootElement = document.documentElement;
      const savedTheme = localStorage.getItem("theme");

      if (savedTheme === "dark") {
            rootElement.classList.add("dark");
      } else if (savedTheme === "light") {
            rootElement.classList.remove("dark");
      }
    
      // Toggle theme on button click
      themeToggle.addEventListener("click", () => {
            if (rootElement.classList.contains("dark")) {
                rootElement.classList.remove("dark");
                localStorage.setItem("theme", "light"); // Save preference as light
            } else {
                rootElement.classList.add("dark");
                localStorage.setItem("theme", "dark"); // Save preference as dark
            }
      });



      
      const navButtons = document.querySelectorAll('nav button');
      const mainContent = document.querySelector('main');
  
      // Redirect Communication link
      const communication = document.getElementById('communication');
      communication.addEventListener('click', () => {
        navButtons.forEach(btn => btn.classList.remove('text-teal-600', 'dark:text-teal-400'));
        loadContent("communication");
      });


      // Redirect Communication link
      const intellevaAI = document.getElementById('intelleva-ai');
      intellevaAI.addEventListener('click', () => {
        navButtons.forEach(btn => btn.classList.remove('text-teal-600', 'dark:text-teal-400'));
        loadContent("AI");
      });


      const contentCache = {};
      let debounceTimer;
  
      // Function to add transition effect
      const applyTransitionEffect = () => {
        mainContent.classList.add('fade-in');
        mainContent.addEventListener('animationend', () => {
          mainContent.classList.remove('fade-in');
        }, { once: true });
      };
  



      const stateCache = {};
      const loadedScripts = new Set();
      const loadedStyles = new Set();
      
      // Function to load page content with caching and state preservation
      const loadContent = (page) => {
        if (stateCache[page]) {
          restoreState(page);
          return;
        }
      
        if (contentCache[page]) {
          updateContent(page, contentCache[page]);
          return;
        }
      
        fetch(`${userRole}/${page}`)
          .then(response => {
            if (!response.ok) throw new Error(`Failed to load ${page}: ${response.statusText}`);
            return response.text();
          })
          .then(content => {
            contentCache[page] = content;
            updateContent(page, content);
          })
          .catch(error => {
            console.error(error);
            mainContent.innerHTML = `<p class="text-center text-red-500">Failed to load content. Please try again.</p>`;
          });
      };
      
      // Function to update content while preserving state
      const updateContent = (page, content) => {
        // Convert the HTML content string to a DOM element
        const tempContainer = document.createElement('div');
        tempContainer.innerHTML = content;
        
        mainContent.innerHTML = tempContainer.innerHTML; // Insert the parsed HTML into main content
        lucide.createIcons({ container: mainContent });
        applyTransitionEffect();
        
        // Wait for all dynamic content to be fully loaded before saving the state
        loadScriptsAndStyles(tempContainer).then(() => {
          storeState(page);
        });
      };
      
      // Store the current page state before navigation
      const storeState = (page) => {
        stateCache[page] = mainContent.innerHTML;
      };
      
      // Restore a previously visited page from stateCache
      const restoreState = (page) => {
        mainContent.innerHTML = stateCache[page];
        lucide.createIcons({ container: mainContent });
        applyTransitionEffect();
      };
      
      // Preload scripts and styles for smoother navigation
      const preloadContent = () => {
        const preloadPages = userRole.toLowerCase() === "student"
          ? ["dashboard", "attendance", "grade", "class", "fees", "profile", "communication", "AI"]
          : userRole.toLowerCase() === "teacher"
          ? ["dashboard", "attendance", "grades", "class", "finance", "profile", "communication", "AI"]
          : ["dashboard", "students", "teacher", "classes", "school", "finance", "profile", "communication", "AI"];
      
        preloadPages.forEach((page) => {
          if (!contentCache[page]) {
            fetch(`${userRole}/${page}`)
              .then(response => response.text())
              .then(content => {
                contentCache[page] = content;
                const tempContainer = document.createElement('div');
                tempContainer.innerHTML = content;
              })
              .catch(error => console.error(`Error preloading ${page}:`, error));
          }
        });
      };
      

      // Preload and execute page-specific scripts and styles
      const preloadPageScripts = (container) => {
        const scripts = container.querySelectorAll("script");
        scripts.forEach((script) => {
          if (script.src && !loadedScripts.has(script.src)) {
            const newScript = document.createElement("script");
            newScript.src = script.src;
            newScript.defer = true;
            document.body.appendChild(newScript);
            loadedScripts.add(script.src);
          }
        });
      
        const styles = container.querySelectorAll("link[rel='stylesheet']");
        styles.forEach((style) => {
          if (!loadedStyles.has(style.href)) {
            const newStyle = document.createElement("link");
            newStyle.rel = "stylesheet";
            newStyle.href = style.href;
            document.head.appendChild(newStyle);
            loadedStyles.add(style.href);
          }
        });
      };
    
      
      // Wait for all scripts to load before storing state
      const loadScriptsAndStyles = (container) => {
        return new Promise((resolve) => {
          const scripts = container.querySelectorAll('script');
          const scriptPromises = Array.from(scripts).map(script => {
            return new Promise((scriptResolve) => {
              const newScript = document.createElement('script');
              if (script.src) {
                newScript.src = script.src;
                newScript.onload = () => scriptResolve();
              } else {
                newScript.textContent = script.textContent;
                newScript.onload = () => scriptResolve();
              }
              document.body.appendChild(newScript);
            });
          });
      
          // Ensure all scripts are loaded before resolving
          Promise.all(scriptPromises).then(resolve);
        });
      };
  
      
      // Debounce click event for smooth navigation
      navButtons.forEach(button => {
        button.addEventListener('click', () => {
          clearTimeout(debounceTimer);
          debounceTimer = setTimeout(() => {
            navButtons.forEach(btn => btn.classList.remove('text-teal-600', 'dark:text-teal-400'));
            button.classList.add('text-teal-600', 'dark:text-teal-400');
      
            const page = button.dataset.page;
            loadContent(page);
          }, 300);
        });
      });
      
      
      // Load initial content and preload other pages
      loadContent('dashboard');
      preloadContent();
  
      // Query the button with the specific data attribute
      const button = document.querySelector('button[data-page="dashboard"]');
      if (button) {
        button.classList.add('text-teal-600', 'dark:text-teal-400');
      }
    });
  }
  
  // Async function to fetch the user role
  async function fetchUserRole() {
    try {
      const response = await fetch('/api/current_user_role', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        if (data.success && data.role) {
          return data.role; // Return the role directly
        }
      }
  
      // Redirect to login page if role is not found or response isn't successful
      window.location.href = "/login";
      return null;
    } catch (error) {
      console.error('Error fetching user role:', error);
      // Redirect to login in case of error
      window.location.href = "/login";
      return null;
    }
  }
  
  // Function to populate navigation
  function populateNavigation(userRole) {
    const navigationButtons = {
        student: [
          { page: "dashboard", icon: "layout-dashboard", label: "Dashboard", textClass: "text-teal-600 dark:text-teal-400" },
          { page: "grade", icon: "trending-up", label: "Grades", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "attendance", icon: "calendar-check", label: "Attendance", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "fees", icon: "dollar-sign", label: "Fees", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "class", icon: "book-open", label: "Class", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "profile", icon: "user-circle", label: "Profile", textClass: "text-gray-600 dark:text-gray-400" }
        ],
        teacher: [
          { page: "dashboard", icon: "layout-dashboard", label: "Dashboard", textClass: "text-teal-600 dark:text-teal-400" },
          { page: "grades", icon: "trending-up", label: "Grades", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "attendance", icon: "calendar-check", label: "Attendance", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "finance", icon: "dollar-sign", label: "Finance", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "class", icon: "book-open", label: "Classes", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "profile", icon: "user-circle", label: "Profile", textClass: "text-gray-600 dark:text-gray-400" }
        ],
        admin: [
          { page: "dashboard", icon: "layout-dashboard", label: "Dashboard", textClass: "text-teal-600 dark:text-teal-400" },
          { page: "students", icon: "user", label: "Students", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "teachers", icon: "user-check", label: "Teachers", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "classes", icon: "book-open", label: "Classes", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "finance", icon: "dollar-sign", label: "Finance", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "schools", icon: "home", label: "Schools", textClass: "text-gray-600 dark:text-gray-400" },
          { page: "profile", icon: "user-circle", label: "Profile", textClass: "text-gray-600 dark:text-gray-400" }
        ]
      };
  
    const navContainer = document.getElementById("nav");
    navContainer.innerHTML = '';
  
    if (navigationButtons[userRole]) {
      const navBar = document.createElement('nav');
      navBar.classList.add('fixed', 'bottom-0', 'left-0', 'right-0', 'flex', 'justify-around', 'border-t', 'border-gray-200', 'bg-white', 'dark:border-gray-800', 'dark:bg-gray-900', 'py-1');
  
      navigationButtons[userRole].forEach(button => {
        const buttonElement = document.createElement("button");
        buttonElement.classList.add("flex", "flex-col", "items-center", "p-1");
        buttonElement.setAttribute("data-page", button.page);
        buttonElement.innerHTML = `
          <i data-lucide="${button.icon}" class="h-5 w-5"></i>
          <span class="text-xs mt-1">${button.label}</span>
        `;
        navBar.appendChild(buttonElement);
      });
  
      navContainer.appendChild(navBar);
    } else {
      console.error("Invalid user role:", userRole);
    }
  }