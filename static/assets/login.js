function loginUser(e) {
  e.preventDefault();

  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value;

  // Registered user
  const storedUser = JSON.parse(localStorage.getItem("BookMyScreen"));

  if (!storedUser) {
    alert("No account found. Please register ❌");
    return;
  }

  // Validate credentials
  if (email === storedUser.email && password === storedUser.password) {

    // Create login session (DO NOT store password)
    const loggedInUser = {
      name: storedUser.name,
      email: storedUser.email,
      phone: storedUser.phone,
      address: storedUser.address
    };

    // Save session
    localStorage.setItem("user", JSON.stringify(loggedInUser));

    alert("Login successful ✅");

    // Redirect
    window.location.href = "index.html";

  } else {
    alert("Invalid credentials ❌");
  }
}
