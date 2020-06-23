"use strict";

let tableColumns = [" ", "Athlete", "Exercise", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];

function generateTableHead(table) {
  let thead = table.append(`<thead></thead>`);
  let row = thead.append(`<tr></tr>`);
  for (let column of tableColumns) {
    let th = row.append(`<th id="${column}" scope="col">${column}</th>`);
  };
};

function display_dashboard() {
  $.get('/get-team-data', (response) => {
    let athletes = response;

  $.get('/get-activity-data', (response) => {
    let activities = response;

    for (let athlete of athletes) {
      let tbody = table.append(`<tbody></tbody>`);
      let row = tbody.append(`<tr id="${athlete['id']}-row"></tr>`);
      let athleteImg = row.append(`<td><img src="${athlete['prof_pic']}" width="50px" class="rounded-circle" align="left"/></td>`);
      let athleteName = row.append(`<th rowspan="2">${athlete['name']}</th>`);
      let run = row.append(`<td id="run-exercise" scope="row">Run</td>`);
      // let crossTrain = row.append(`<tr id="xt-workout" scope="row">Cross Train</tr>`);

      for (let i of Array(9).keys()) {
        row.append(`<td id="user-${athlete['id']}-col${i+1}" scope="row"></td>`)
      };

      let weekMileage = 0

      for (let activity of activities) {
        
        if (activity['user_id'] === athlete['id'] && activity['exercise_type'] === "Run") {
          
          $(`#user-${athlete['id']}-col${activity['weekday']}`).replaceWith(`<td class="activity-data" id="${activity['strava_activity_id']}" scope="row">${activity['distance']} mi</td>`);
          
          weekMileage += activity['distance'];
          // `day${activity['weekday']}Total` = 0;
          // `day${activity['weekday']}Total` += activity['distance'];
          let weekMileageRounded = parseFloat((weekMileage.toFixed(2)));
          $(`#user-${athlete['id']}-col8`).replaceWith(`<td id="user-${athlete['id']}-col8" scope="row"><b>${weekMileageRounded} mi<b></td>`);
        };
      };
      };

  $(".activity-data").on('click', (evt) => {
    let activityID = evt.target.id ;
    $.get(`/api/get-activity-splits/${activityID}`, (response) => {
      console.log(response);
    });
  });

  });
  });

};


display_dashboard()

let table = $("#team-dash");
generateTableHead(table);

