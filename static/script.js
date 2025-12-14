// ---------- Toggle visibility of forms ----------------------------------

const toggleVisibility = (btnId, formId) => {
  const btn = document.getElementById(btnId);
  const form = document.getElementById(formId);

  btn.addEventListener("click", () => {
    form.style.display = form.style.display === "none" || !form.style.display ? "block" : "none";
  });
};

toggleVisibility("alarm_settings_btn", "alarm_form");
toggleVisibility("clockout_settings_btn", "clockout_form");


// ---------- Polling for updates -----------------------------------------

let intervalId = null;

async function updateData() {
  try {
    // Fetch all data in parallel
    const [highscoreRes, scoreStreakRes, habitsRes] = await Promise.all([
      fetch('/update_highscore'),
      fetch('/update_score_and_streak'),
      fetch('/update_habits')
    ]);

    if (!highscoreRes.ok || !scoreStreakRes.ok || !habitsRes.ok) {
      throw new Error("Failed to fetch one or more endpoints");
    }

    const highscoreData = await highscoreRes.json();
    const scoreStreakData = await scoreStreakRes.json();
    const habitsData = await habitsRes.json();

    if ("highscore" in highscoreData) {
      document.getElementById("highscore").textContent = "High Score: " + highscoreData.highscore;
    }

    if ("score" in scoreStreakData) {
      document.getElementById("current_score").textContent = "Current Score: " + scoreStreakData.score;
    }
    if ("streak" in scoreStreakData) {
      document.getElementById("streak").textContent = "Streak: " + scoreStreakData.streak;
    }

    // Turn highscore text darker if score != highscore and both are not 0
    const highscore = highscoreData.highscore;
    const score = scoreStreakData.score;

    if (score !== highscore && highscore !== 0) {
      document.getElementById("highscore").style.color = "#3b0a3e";
    } else {
      // Optional: reset color if no longer equal
      document.getElementById("highscore").style.color = "white";
    }

    // Update habits
    const habits = habitsData.values;
    const isToday = habitsData.is_today;

    for (const [habit, value] of Object.entries(habits)) {
      const el = document.getElementById(habit);
      if (el) {
        el.textContent = value;
        el.style.color = isToday[habit] ? "white" : "black";
      }
    }
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


// ---------- Alarm days ---------------------------------------------------

function toggleDay(day, element) {
  fetch("/toggle_day", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ day })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      element.classList.toggle("on", data.new_value);
      element.classList.toggle("off", !data.new_value);
    } else {
      console.error("Failed to toggle day:", data);
    }
  })
  .catch(err => console.error("Error toggling day:", err));
}
