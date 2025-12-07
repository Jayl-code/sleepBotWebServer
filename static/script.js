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
    fetch('/update_highscore')
      .then(response => response.json())
      .then(data => {
        if ("highscore" in data) {
        document.getElementById("highscore").textContent =
          "High Score: " + data.highscore;
      }
      });
    fetch('/update_score_and_streak')
      .then(response => response.json())
      .then(data => {
        if ("score" in data) {
        document.getElementById("current_score").textContent =
          "Current Score: " + data.score;
      }
      if ("streak" in data) {
        document.getElementById("streak").textContent =
          "Streak: " + data.streak;
      }
      });
      fetch("/update_habits")
        .then(response => response.json())
        .then(data => {
            // Data from Flask
            const habits = data.values;
            const isToday = data.is_today;

            // Example: update HTML elements
            for (const habit in habits) {
                document.getElementById(habit).textContent = habits[habit];

                if (isToday[habit]) {
                    document.getElementById(habit).style.color = "white";
                } else {
                    document.getElementById(habit).style.color = "black";
                }
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

// ----------Alarm days---------------------------------------------------

function toggleDay(day, element) {
    fetch("/toggle_day", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ day: day })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            if (data.new_value) {
                element.classList.remove("off");
                element.classList.add("on");
            } else {
                element.classList.remove("on");
                element.classList.add("off");
            }
        }
    });
}