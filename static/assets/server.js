const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

let otpStore = {}; // { mobile: otp }

// SEND OTP
app.post("/send-otp", async (req, res) => {
  const { mobile } = req.body;
  const otp = Math.floor(100000 + Math.random() * 900000);

  otpStore[mobile] = otp;

  try {
    await axios.get("https://www.fast2sms.com/dev/bulkV2", {
      params: {
        authorization: "YOUR_FAST2SMS_API_KEY",
        route: "otp",
        variables_values: otp,
        numbers: mobile
      }
    });

    res.json({ success: true, message: "OTP sent successfully" });
  } catch (error) {
    res.json({ success: false, message: "OTP failed to send" });
  }
});

// VERIFY OTP
app.post("/verify-otp", (req, res) => {
  const { mobile, otp } = req.body;

  if (otpStore[mobile] == otp) {
    delete otpStore[mobile];
    res.json({ success: true, message: "Login Successful" });
  } else {
    res.json({ success: false, message: "Invalid OTP" });
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
