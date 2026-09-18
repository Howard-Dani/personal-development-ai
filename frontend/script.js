const habitInput = document.getElementById("habit-name");
const durationInput = document.getElementById("target-duration");
const result = document.getElementById("result");

const createButton = document.querySelector(".create-habit");
let durationGoal = null;
let lastWeekReadiness = null;


function createWeekTable(weekNumber, plannedDuration) {
    return `
        <div class="week-block" data-week="${weekNumber}">

            <h3>Week ${weekNumber}</h3>

            <table>
                <tr>
                    <th>Day</th>
                    <th>Planned duration</th>
                    <th>Actual duration</th>
                </tr>

                <tr>
                    <td>Sunday</td>
                    <td>${plannedDuration}</td>
                    <td><input type="number" min="0"></td>
                </tr>

                <tr>
                    <td>Monday</td>
                    <td>${plannedDuration}</td>
                    <td><input type="number" min="0"></td>
                </tr>

                <tr>
                    <td>Tuesday</td>
                    <td>${plannedDuration}</td>
                    <td><input type="number" min="0"></td>
                </tr>

                <tr>
                    <td>Wednesday</td>
                    <td>${plannedDuration}</td>
                    <td><input type="number" min="0"></td>
                </tr>

                <tr>
                    <td>Thursday</td>
                    <td>${plannedDuration}</td>
                    <td><input type="number" min="0"></td>
                </tr>

                <tr>
                    <td>Friday</td>
                    <td>${plannedDuration}</td>
                    <td><input type="number" min="0"></td>
                </tr>

                <tr>
                    <td>Saturday</td>
                    <td>${plannedDuration}</td>
                    <td><input type="number" min="0"></td>
                </tr>
            </table>

            <button
                class="finish-week"
                data-week="${weekNumber}"
                data-planned-duration="${plannedDuration}">
                Finish Week
            </button>

            <p class="week-error"></p>

        </div>
    `;
}


createButton.addEventListener("click", function() {

    const habitName = habitInput.value.trim();
    const targetDuration = Number(durationInput.value);

    if (habitName === "" || !Number.isFinite(targetDuration) || targetDuration <= 0) {
        result.innerHTML = `
            <p class="form-error">
                Please enter a habit name and a valid target duration.
            </p>
        `;

        return;
    }

    durationGoal = targetDuration;
    lastWeekReadiness = null;

    result.innerHTML = `
        <h2></h2>
        <p>Target duration: ${targetDuration} minutes</p>

        ${createWeekTable(1, targetDuration)}
    `;
    result.querySelector("h2").textContent = habitName;
});


result.addEventListener("click", async function(event) {

    if (!event.target.classList.contains("finish-week")) {
        return;
    }

    const button = event.target;
    if (button.disabled) {
        return;
    }

    const weekNumber = Number(
        event.target.dataset.week
    );

    const plannedDuration = Number(
        event.target.dataset.plannedDuration
    );

    const weekBlock = event.target.closest(".week-block");

    const errorMessage = weekBlock.querySelector(".week-error");

    errorMessage.textContent = "";

    const inputs = weekBlock.querySelectorAll(
        'input[type="number"]'
    );

    const actualDurations = [];

    for (const input of inputs) {

        if (input.value === "") {
            errorMessage.textContent =
                "Please fill in all 7 days.";

            return;
        }

        const actualDuration = Number(input.value);

        if (!Number.isFinite(actualDuration) || actualDuration < 0) {
            errorMessage.textContent =
                "Please enter a valid, non-negative duration for each day.";

            return;
        }

        actualDurations.push(actualDuration);
    }

    button.disabled = true;
    button.textContent = "Finishing Week…";
    createButton.disabled = true;

    for (const input of inputs) {
        input.disabled = true;
    }

    let weekResult;
    try {
        const response = await fetch("/finish-week", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                week_number: weekNumber,
                planned_duration: plannedDuration,
                duration_goal: durationGoal,
                actual_durations: actualDurations,
                last_week_readiness: lastWeekReadiness
            })
        });

        if (!response.ok) {
            const error = await response.json().catch(() => null);
            throw new Error(typeof error?.detail === "string"
                ? error.detail
                : `Unable to finish week (HTTP ${response.status}). Please try again.`);
        }

        weekResult = await response.json();
        if (!Number.isFinite(weekResult.next_duration) || weekResult.next_duration < 0 ||
            !Number.isFinite(weekResult.weekly_readiness)) {
            throw new Error("The server returned an invalid result. Please try again.");
        }
    } catch (error) {
        errorMessage.textContent = error instanceof TypeError
            ? "Cannot reach the server. Check your connection and try again."
            : error.message;
        button.disabled = false;
        button.textContent = "Finish Week";
        for (const input of inputs) {
            input.disabled = false;
        }
        return;
    } finally {
        createButton.disabled = false;
    }

    const nextDuration = weekResult.next_duration;
    lastWeekReadiness = weekResult.weekly_readiness;
    button.textContent = "Week Completed";

    weekBlock.classList.add("completed-week");

    const nextWeekNumber = weekNumber + 1;

    const nextWeekAlreadyExists = result.querySelector(
        `.week-block[data-week="${nextWeekNumber}"]`
    );

    if (nextWeekAlreadyExists) {
        return;
    }

    result.insertAdjacentHTML(
        "beforeend",
        `
            <div class="week-result">
                <p>
                    Your target duration for next week is
                    <strong>${nextDuration} minutes</strong>.
                </p>
            </div>

            ${createWeekTable(
                nextWeekNumber,
                nextDuration
            )}
        `
    );
});
