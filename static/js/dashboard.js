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
            <button type="button" class="activity-data btn btn-light" id="${activity['strava_activity_id']}" data-container="body" data-toggle="popover" data-trigger="hover click" data-placement="top">
            ${activity['distance']} mi<span class="badge badge-warning ml-2"></span></button>

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
      let activityDate = reformatDate(splits['start_date_local'])
      let distance = reformatDistance(splits['distance'])
      let workoutTime = reformatWorkoutLength(splits['moving_time'])
      let avgSpeed = reformatAvgSpeed(splits['distance'], splits['moving_time'])
      let elevationGain = reformatElevationGain(splits['total_elevation_gain'])
    $(`#${splits['id']}`).popover(
      { 
        title : 'Details',
        content : `Date: ${activityDate} <br/>
                  Distance: ${distance} <br/>
                  Time: ${workoutTime} <br/> 
                  Average Pace: ${avgSpeed} <br/>
                  Elevation Gain: ${elevationGain}<br/><br/>
                  Comment:
                  <textarea class="form-control" id="message-text"></textarea><br/>
                  <button type="submit" class="comment btn btn-warning" data-toggle="modal" data-target="#exampleModal">Submit</button>`,
                                  // <a href="#exampleModal" id="${splits['id']}" class="comment btn-sm btn-primary" data-target="#exampleModal">Comment</a>`,
        html: true
      });
    });
    });
  });
  });
};

// $(".comment").on('click', (evt) => {
//   console.log("HELLO!!!!")
//   //   let activityID = evt.target.id ;
//   //   console.log(activityID);
//   // $(".activity-data").popover('hide');
  // $('#exampleModal').modal({
  //   focus: true
  // });
// });
// $('#exampleModal').on('show.bs.modal', function (event) {
//   var button = $(event.relatedTarget) // Button that triggered the modal
//   var recipient = button.data('whatever') // Extract info from data-* attributes
//   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//   var modal = $(this)
//   modal.find('.modal-title').text('New message to ' + recipient)
//   modal.find('.modal-body input').val(recipient)
// });

function reformatDate(activityDate) {
  let formatDate = new Date(activityDate);
  console.log(formatDate)
  let activityMonth = formatDate.getMonth()+1;
  let activityDay = formatDate.getDate()+1;
  let activityYear = formatDate.getFullYear();
  let reformatDate = activityMonth + "-" + activityDay + "-" + activityYear;
  console.log(reformatDate)
  return reformatDate;
};

function reformatWorkoutLength(workoutTime) {

    let time = workoutTime / 3600;
    let hours = Math.floor(time);
    let minutes = Math.floor((time % 1) * 60);
    let seconds = Math.round((((time % 1) * 60) % 1) * 60);
    console.log(time)
    console.log(hours)
    console.log(minutes)
    console.log(seconds)
    if (hours < 1 && seconds > 10) {
        return `${minutes}:${seconds}`;
    }
    else if (hours < 1 && seconds < 10) {
        return `${minutes}:0${seconds}`;
    }
    else if (hours >= 1 && seconds > 10) {
        return `${hours}:${minutes}:${seconds}`;
    }
    else {
        return `${hours}:${minutes}:0${seconds}`;
    };
};

function reformatDistance(distance) {

  distance = distance * 0.000621371
  console.log(distance)
  let miles = Math.floor(distance)
  console.log(miles)
  let decimal = Math.floor(distance % 1 * 100)
  console.log(decimal)
  return `${miles}.${decimal}mi`
};

function reformatAvgSpeed(distance, workoutTime) {

  distance = distance * 0.000621371

  if (distance > 0) {

    let avgTime = (workoutTime / 60) / distance;
    let avgMinutes = Math.floor(avgTime);
    let avgSeconds = Math.round((avgTime % 1) * 60);


    if (avgSeconds < 10) {
      return `${avgMinutes}:0${avgSeconds}/mile`;
    }
    else {
      return `${avgMinutes}:${avgSeconds}/mile`;
    };
  }
  else {
    return 'N/A';
  };
};

function reformatElevationGain(gain) {

  gain = Math.round(gain * 3.28084);

  return `${gain}ft`
};

// function getSplits(split_dict) {
//   for (let split in splits)  {
//     split
//   }
// }  



display_dashboard()




