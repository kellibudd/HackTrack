"use strict";

let tableColumns = [" ", "Athlete", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];
// let tableColumns = [" ", "Athlete", "Exercise", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];

function generateTableHead(table) {
  for (let column of tableColumns) {
    let tableHeadRow = $("#head-row");
    tableHeadRow.append(`<th id="${column}" scope="col">${column}</th>`);
  };
};

let table = $("#team-table");
generateTableHead(table);

function display_dashboard() {
  $.get('/get-team-data', (response) => {
    let athletes = response;

  $.get('/get-activity-data', (response) => {
    let activities = response;

    for (let athlete of athletes) {
      let tbody = $("#table-body");
      let row = tbody.append(`<tr id="${athlete['id']}-row"></tr>`);
      row.append(`<td><img src="${athlete['prof_pic']}" width="50px" class="rounded-circle" align="left"/></td>`);
      row.append(`<th rowspan="2">${athlete['name']}</th>`);
      // let run = row.append(`<td id="run-exercise" scope="row">Run</td>`);
      // let crossTrain = row.append(`<tr id="xt-workout" scope="row">Cross Train</tr>`);

      for (let i of Array(9).keys()) {
        row.append(`<td id="user-${athlete['id']}-col${i+1}" scope="row"></td>`)
      };

      let weekMileage = 0

      for (let activity of activities) {
        
        if (activity['user_id'] === athlete['id'] && activity['exercise_type'] === "Run") {
          
          $(`#user-${athlete['id']}-col${activity['weekday']}`).replaceWith(
          `<td scope="row">
            <button type="button" class="activity-data btn btn-light" id="${activity['strava_activity_id']}" data-container="body" data-toggle="popover" data-trigger="focus" data-placement="top">
            ${activity['distance']} mi</button>
          </td>`);
          
          weekMileage += activity['distance'];
          // `day${activity['weekday']}Total` = 0;
          // `day${activity['weekday']}Total` += activity['distance'];
          let weekMileageRounded = parseFloat((weekMileage.toFixed(2)));
          $(`#user-${athlete['id']}-col8`).replaceWith(
            `<td scope="row" id="user-${athlete['id']}-col8">
              <button class="activity-data btn btn-dark"><b>${weekMileageRounded} mi<b></button>
            </td>`);
        };  
      };
    };
    // infinite loop - need to fix
  $(".activity-data").on('click', (evt) => {
    let activityID = evt.target.id ;
    console.log("hi!!");
    $.get(`/api/get-activity-splits/${activityID}`, (response) => {
      console.log(response);
      const splits = response;
      
    $(`#${splits['id']}`).popover(
      { 
        title : 'Details',
        content : `Time: ${splits['moving_time']}\n Elevation: ${splits['total_elevation_gain']}\n Average Pace: ${splits['average_speed']}`
      });
    });
    });
  });
  });
};


// let collapse_el = $(".card-body")
display_dashboard()




