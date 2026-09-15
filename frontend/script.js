console.log("script loaded");

const habitInput = document.getElementById("habit-name"); // refers to habit-name input box
const durationInput = document.getElementById("target-duration");
const result = document.getElementById("result");

const createButton = document.querySelector("button"); // find the first button


function createWeekTable(weekNumber, plannedDuration) {
    return `
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

        <button class="finish-week">Finish Week</button>
    `;
}


createButton.addEventListener("click", function() { // when the button is clicked, run this function

    const habitName = habitInput.value;
    const targetDuration = Number(durationInput.value);

    if (habitName === "" || targetDuration <= 0) { // the button doesn't accept empty habit name or invalid duration
        result.innerHTML = `
            <p>Please enter a habit name and a valid target duration</p>
        `;

        return;
    }

    result.innerHTML = `
        <h2>${habitName}</h2>
        <p>Target duration: ${targetDuration} minutes</p>

        ${createWeekTable(1, targetDuration)}
    `;
});