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
toggleVisibility("expand_button", "test");

// ---------- Visibility change updates -----------------------------------------

document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
        location.reload();
    }
});

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
