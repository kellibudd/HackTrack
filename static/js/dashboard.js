"use strict";



function display_dashboard() {
  $.get('/get-team-data', (response) => {
    let athletes = response;
    console.log(athletes);

  $.get('/get-activity-data', (response) => {
    let activities = response;
    console.log(activities);

    for (let athlete of athletes) {
      let tbody = table.append(`<tbody></tbody>`);
      let row = tbody.append(`<tr></tr>`);
      let athlete_img = row.append(`<td scope="row" rowspan="2"><img src="${athlete['prof_pic']}" width="50px" class="rounded-circle" align="left"/></td>`);
      let athlete_name = row.append(`<td scope="row" rowspan="2"><b>${athlete['name']}<b></td>`);
      
      for (let activity of activities) {
        if (activity['user_id'] === athlete['id']) {
          row.append(`<td id="${activity['strava_activity_id']}scope="row">${activity['distance']} mi</td>`);
        };
      };
    };
  });
  });
};

function generateTableHead(table) {
  let thead = table.append(`<thead></thead>`);
  let row = thead.append(`<tr></tr>`);
  for (let column of columns) {
    let th = row.append(`<th id="${column}"" scope="col">${column}</th>`);
  }
}

let columns = [" ", "Athlete", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];


display_dashboard()
let table = $("table");
generateTableHead(table);
// generateTable(table, athletes);