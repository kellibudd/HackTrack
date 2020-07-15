"use strict";

let tableColumns = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
// let tableColumns = [" ", "Athlete", "Exercise", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];

function generateTableHead(table) {
  let tableHeadRow = $("#head-row");

  tableHeadRow.append(
    `<th class="table-header" id="athlete-header" scope="col">Athlete</th>`
  );

  for (let column of tableColumns) {
    tableHeadRow.append(`<th class="table-header" id="${column}" scope="col">
                        <span class="weekday-span">${column}</span><br>
                        <span class="${column}-date-span"></span>
                        </th>`);
  }

  tableHeadRow.append(
    `<th class="table-header" id="total-miles-header" scope="col">Total Miles</th>`
  );
}

let table = $("#team-table");
generateTableHead(table);

function display_dashboard() {
  let convertedDate = null;

  if (window.location.pathname === "/dashboard") {
    let date = new Date();
    convertedDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000)
      .toISOString()
      .split("T")[0];
  } else {
    convertedDate = window.location.pathname.split("/")[2];
  }

  displayWeekDates(convertedDate);

  updatePagerLinks(convertedDate);

  $.get("/get-team-data", (response) => {
    let athletes = response;

    $.get(`/api/get-activity-data/${convertedDate}`, (response) => {
      let activities = response;

      for (let athlete of athletes) {
        let tbody = $("#table-body");
        let row = tbody.append(`<tr id="${athlete["id"]}-row"></tr>`);
        row.append(
          `<td class="athlete-img"><img src="${athlete["prof_pic"]}" class="table-data rounded-circle" align="left"/></td>`
        );
        row.append(`<td scope="row">
                      <button class="table-data btn btn-dark" disabled>${athlete["f_name"]}</button>
                    </td>`);
        // let run = row.append(`<td id="run-exercise" scope="row">Run</td>`);
        // let crossTrain = row.append(`<tr id="xt-workout" scope="row">Cross Train</tr>`);

        for (let i of Array(8).keys()) {
          row.append(
            `<td class="table-data" id="user-${athlete["id"]}-col${
              i + 1
            }" scope="row"></td>`
          );
        }

        let weekMileage = 0;

        for (let activity of activities) {
          if (
            activity["user_id"] === athlete["id"] &&
            activity["exercise_type"] === "Run"
          ) {
            let activityDate = reformatDate(activity["date"]);
            let distance = reformatDistance(activity["distance"]);
            let workoutTime = reformatWorkoutLength(activity["workout_time"]);
            let avgSpeed = reformatAvgSpeed(
              activity["distance"],
              activity["workout_time"]
            );
            let elevationGain = reformatElevationGain(activity["elev_gain"]);

            $(`#user-${athlete["id"]}-col${activity["weekday"]}`).replaceWith(
              `<td scope="row">
              <button type="button" class="table-data btn btn-light" id="popover-${activity["strava_activity_id"]}" 
                data-container="body" [dynamicPosition="false" data-toggle="popover" data-trigger="hover click" data-placement="bottom"
                >${distance}</button>
            </td>`
            );

            weekMileage += activity["distance"];
            let weekMileageRounded = reformatDistance(weekMileage);
            $(`#user-${athlete["id"]}-col8`).replaceWith(
              `<td scope="row" id="user-${athlete["id"]}-col8">
                <button class="table-data btn btn-warning" disabled>${weekMileageRounded}</button>
              </td>`
            );

            let splitSummary = "";

            if (activity["splits"] !== null) {
              let activitySplits = activity["splits"];
              let splits = [];

              for (let key of Object.keys(activitySplits)) {
                let split =
                  `${parseInt(key) + 1}` +
                  " | " +
                  reformatAvgSpeed(
                    activitySplits[key].distance,
                    activitySplits[key].moving_time
                  );
                splits.push(`<p class="split">${split}</p>`);
              }

              splits = splits.join("");

              splitSummary = `<details>
                                <summary>See Splits</summary>
                                ${splits}
                              </details>`;
            }

            $(`#popover-${activity["strava_activity_id"]}`).popover({
              title: "Activity Details",
              container: "body",
              html: true,
              content: `<div class=activity-details>
                                      <div>Date: ${activityDate}</div>
                                      <div>Distance: ${distance}</div>
                                      <div>Time: ${workoutTime}</div>
                                      <div>Average Pace: ${avgSpeed}</div>
                                      <div>Elevation Gain: ${elevationGain}</div>
                                      <div>${splitSummary}</div><br/>
                                      <div></div>
                                    </div>
                                    <form id="comment-form" action="/add-comment" method="POST">
                                      Comment:
                                      <textarea rows="1" class="form-control" id="comment-text" name="comment"></textarea><br/>
                                      <input id="activity-id" type="hidden" name="activity-id" value="${activity["strava_activity_id"]}">
                                      <input type="submit" class="submit-comment btn btn-warning">
                                    </form>`,
            });
          }
        }
      }
    });
  });
}

display_dashboard();

function displayWeekDates(date) {
  date = new Date(date.toString());

  let i = 1;

  while (i < 8) {
    let firstWeekday = new Date(
      date.getFullYear(),
      date.getMonth(),
      date.getDate() - date.getDay() + i
    )
      .toString()
      .split(" ");
    $(`.${firstWeekday[0]}-date-span`).replaceWith(
      `<span class="${firstWeekday[0]}-date-span">${firstWeekday[1]} ${firstWeekday[2]}</span><br>`
    );
    i += 1;
  }
}

function updatePagerLinks(date) {
  date = new Date(date.toString());

  let previousWeek = new Date(
    date.getFullYear(),
    date.getMonth(),
    date.getDate() - 6
  );
  previousWeek = previousWeek.toISOString().split("T")[0];

  let nextWeek = new Date(
    date.getFullYear(),
    date.getMonth(),
    date.getDate() + 8
  );
  nextWeek = nextWeek.toISOString().split("T")[0];

  $("#previous-button").attr("href", `/dashboard/${previousWeek}`);

  let currentDate = new Date();

  if (
    date.toISOString().split("T")[0] !==
    new Date(currentDate.getTime() - currentDate.getTimezoneOffset() * 60000)
      .toISOString()
      .split("T")[0]
  ) {
    $("#next-button").attr("href", `/dashboard/${nextWeek}`);
    $("#next-button").removeAttr("hidden");
  }
}

function reformatDate(activityDate) {
  let formatDate = new Date(activityDate);
  let activityMonth = formatDate.getMonth() + 1;
  let activityDay = formatDate.getDate();
  let activityYear = formatDate.getFullYear();
  let reformatDate = activityMonth + "-" + activityDay + "-" + activityYear;

  return reformatDate;
}
export { reformatDate };

function reformatWorkoutLength(workoutTime) {
  let time = workoutTime / 3600;
  let hours = Math.floor(time);
  let minutes = Math.floor((time % 1) * 60);
  let seconds = Math.round((((time % 1) * 60) % 1) * 60);

  if (hours < 1 && seconds > 10) {
    return `${minutes}:${seconds}`;
  } else if (hours < 1 && seconds < 10) {
    return `${minutes}:0${seconds}`;
  } else if (hours >= 1 && minutes < 10 && seconds < 10) {
    return `${hours}:0${minutes}:0${seconds}`;
  } else if (hours >= 1 && minutes < 10 && seconds > 10) {
    return `${hours}:0${minutes}:${seconds}`;
  } else if (hours >= 1 && minutes > 10 && seconds < 10) {
    return `${hours}:${minutes}:0${seconds}`;
  } else {
    return `${hours}:${minutes}:${seconds}`;
  }
}

function reformatDistance(distance) {
  distance = distance * 0.000621371;
  let miles = Math.floor(distance);
  let decimal = Math.round((distance % 1) * 100);

  if (decimal >= 100 && miles === 0) {
    miles = decimal / 100;
    return `${miles}.00 mi`;
  } else if (miles >= 1 && decimal >= 100) {
    miles = miles + decimal / 100;
    return `${miles}.00 mi`;
  } else if (miles >= 1 && decimal < 10) {
    return `${miles}.0${decimal} mi`;
  } else if (miles < 1 && decimal < 10) {
    return `0.0${decimal} mi`;
  } else if (miles < 1 && decimal >= 10) {
    return `0.${decimal} mi`;
  }
  return `${miles}.${decimal} mi`;
}
export { reformatDistance };

function reformatAvgSpeed(distance, workoutTime) {
  distance = distance * 0.000621371;

  if (distance > 0) {
    let avgTime = workoutTime / 60 / distance;
    let avgMinutes = Math.floor(avgTime);
    let avgSeconds = Math.round((avgTime % 1) * 60);

    if (avgSeconds < 10) {
      return `${avgMinutes}:0${avgSeconds}/mi`;
    } else if (avgSeconds == 60) {
      avgMinutes = avgMinutes + 1;
      return `${avgMinutes}:00/mi`;
    } else {
      return `${avgMinutes}:${avgSeconds}/mi`;
    }
  } else {
    return "N/A";
  }
}

function reformatElevationGain(gain) {
  gain = Math.round(gain * 3.28084);

  return `${gain}ft`;
}
