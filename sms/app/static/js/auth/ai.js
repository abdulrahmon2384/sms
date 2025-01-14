document.addEventListener("DOMContentLoaded", function () {
        console.log('im here');
        const sidebarToggle = document.getElementById("sidebarToggle");
        const sidebar = document.getElementById("sidebar");
        const closeSidebar = document.getElementById("closeSidebar");
    
        // Function to open sidebar
        const openSidebar = () => {
            sidebar.classList.remove("-translate-x-full");
        };
    
        // Function to close sidebar
        const closeSidebarFn = () => {
            sidebar.classList.add("-translate-x-full");
        };
    
        // Event listener for sidebar toggle button
        sidebarToggle.addEventListener("click", function () {
            if (sidebar.classList.contains("-translate-x-full")) {
                openSidebar();
            } else {
                closeSidebarFn();
            }
        });
    
        // Event listener for close button inside the sidebar
        closeSidebar.addEventListener("click", closeSidebarFn);
    
        // Event listener to close sidebar when clicking outside
        document.addEventListener("click", function (event) {
            if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
                closeSidebarFn();
            }
        });
});

/*
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const closeSidebar = document.getElementById('closeSidebar');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

sidebarToggle.addEventListener('click', () => {
    console.log("im here ")
    sidebar.classList.toggle('-translate-x-full');
});

closeSidebar.addEventListener('click', () => {
    console.log("im out")
    sidebar.classList.add('-translate-x-full');
});

userInput.addEventListener('input', () => {
    if (userInput.value.trim() !== '') {
        sendButton.classList.remove('bg-gray-600', 'text-gray-400');
        sendButton.classList.add('bg-gradient-teal', 'text-white');
        sendButton.disabled = false;
    } else {
        sendButton.classList.add('bg-gray-600', 'text-gray-400');
        sendButton.classList.remove('bg-gradient-teal', 'text-white');
        sendButton.disabled = true;
    }
});

sendButton.addEventListener('click', () => {
    if (userInput.value.trim() !== '') {
        console.log('Sending message:', userInput.value);
        userInput.value = '';
        sendButton.classList.add('bg-gray-600', 'text-gray-400');
        sendButton.classList.remove('bg-gradient-teal', 'text-white');
        sendButton.disabled = true;
    }
});

*/