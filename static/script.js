// ----------Toggle visibility of forms ----------------------------------

const alarmSettingsBtn = document.getElementById("alarm_settings_btn");
    const alarmForm = document.getElementById("alarm_form");

    alarmSettingsBtn.addEventListener("click", () => {
      alarmForm.style.display = alarmForm.style.display === "none" ? "block" : "none";
    });

const clockoutSettingsBtn = document.getElementById("clockout_settings_btn");
    const clockoutForm = document.getElementById("clockout_form");

    clockoutSettingsBtn.addEventListener("click", () => {
      clockoutForm.style.display = clockoutForm.style.display === "none" ? "block" : "none";
    });

// ----------Polling for updates -----------------------------------------

let intervalId = null;

function updateData() {
  try {
    fetch('/update_data')
      .then(response => response.json())
      .then(data => {
        if ("streak" in data) {
        document.getElementById("streak").textContent =
          "Streak: " + data.streak;
      }
      if ("highscore" in data) {
        document.getElementById("highscore").textContent =
          "High Score: " + data.highscore;
      }
      if ("current_score" in data) {
        document.getElementById("current_score").textContent =
          "Current Score: " + data.current_score;
      }
      });
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

function startPolling() {
  if (!intervalId) {
    updateData();
    intervalId = setInterval(updateData, 15000);
  }
}

function stopPolling() {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
}

// Visibility-based polling
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') startPolling();
  else stopPolling();
});

if (document.visibilityState === 'visible') startPolling();
