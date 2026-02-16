document.addEventListener("DOMContentLoaded", () => {

  const profileContainer = document.getElementById("profile-container");
  if (!profileContainer) return;

  const user = JSON.parse(localStorage.getItem("user"));

  if (user && user.name && user.email) {
    profileContainer.innerHTML = `
      <div class="bg-gray-800 px-3 py-1 rounded-md flex items-center gap-2 cursor-pointer">
        <img src="../assets/images/crew/profile.jpg" class="w-7 h-7 rounded-full">
        <div class="text-sm leading-tight">
          <p class="font-medium">${user.name}</p>
          <p class="text-gray-400 text-xs">${user.email}</p>
        </div>
      </div>
    `;
  } else {
    profileContainer.innerHTML = `
      <a href="login.html" class="bg-red-600 px-4 py-1 rounded text-sm">
        Login
      </a>
    `;
  }

  profileContainer.classList.remove("hidden");
});
