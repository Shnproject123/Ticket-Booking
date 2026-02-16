// WAIT FOR DOM (THIS FIXES THE ISSUE)
document.addEventListener("DOMContentLoaded", () => {

  console.log("Register JS loaded ✅");

  // INIT EMAILJS
  emailjs.init("4zoUdEYEQiVsoCDJN");

  // DOM ELEMENTS
  const nameInput = document.getElementById("name");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const otpInput = document.getElementById("otp");
  const otpSection = document.getElementById("otpSection");
  const sendOtpBtn = document.getElementById("sendOtpBtn");

  let generatedOTP = "";

  // CLICK HANDLER (NO INLINE HTML)
  sendOtpBtn.addEventListener("click", () => {
    console.log("Send OTP clicked ✅");

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirm = confirmPassword.value;

    if (!name || !email || !password || password !== confirm) {
      alert("Invalid details ❌");
      return;
    }

    generatedOTP = Math.floor(100000 + Math.random() * 900000).toString();

    console.log("Generated OTP:", generatedOTP);

    emailjs.send("service_d9louke", "template_8sj0g2k", {
      email: email,
      otp: generatedOTP,
      
    })
    .then(() => {
      otpSection.style.display = "block";
      sendOtpBtn.disabled = true;
      alert("OTP sent successfully ✅");
    })
    .catch(err => {
      console.error("EmailJS Error:", err);
      alert("OTP failed ❌");
    });
  });

  // VERIFY OTP
  window.verifyOTP = function () {
    if (otpInput.value.trim() !== generatedOTP) {
      alert("Wrong OTP ❌");
      return;
    }

    localStorage.setItem("bookflixUser", JSON.stringify({
      name: nameInput.value,
      email: emailInput.value,
      password: passwordInput.value
    }));

    alert("Registration successful ✅");
    location.href = "login.html";
  };
});
