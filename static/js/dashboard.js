"use strict";

let tableColumns = ["Athlete", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Total Miles"];
// let tableColumns = [" ", "Athlete", "Exercise", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];

function generateTableHead(table) {
  for (let column of tableColumns) {
    let tableHeadRow = $("#head-row");
    tableHeadRow.append(`<th class="table-header" id="${column}" scope="col">${column}</th>`);
  };
};

let table = $("#team-table");
generateTableHead(table);

function display_dashboard() {

  let convertedDate = null

  if (window.location.pathname === "/dashboard") {
      let date = new Date();
      console.log(date)
      convertedDate = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().split("T")[0];
      console.log(convertedDate);
  }
  else {
    convertedDate = window.location.pathname.split("/")[2];
  };

  updatePagination(convertedDate)

  $.get('/get-team-data', (response) => {
    let athletes = response;
    
    $.get(`/api/get-activity-data/${convertedDate}`, (response) => {
      let activities = response;

      for (let athlete of athletes) {
        let tbody = $("#table-body");
        let row = tbody.append(`<tr id="${athlete['id']}-row"></tr>`);
        row.append(`<td><img src="${athlete['prof_pic']}" width="60px" class="rounded-circle" align="left"/></td>`);
        row.append(`<td scope="row">
                      <button class="activity-data btn btn-dark" disabled>${athlete['name']}</button>
                    </td>`);
        // let run = row.append(`<td id="run-exercise" scope="row">Run</td>`);
        // let crossTrain = row.append(`<tr id="xt-workout" scope="row">Cross Train</tr>`);

        for (let i of Array(8).keys()) {
          row.append(`<td id="user-${athlete['id']}-col${i+1}" scope="row"></td>`)
        };

        let weekMileage = 0

        for (let activity of activities) {
          console.log(activity)
          if (activity['user_id'] === athlete['id'] && activity['exercise_type'] === "Run") {
            
            let activityDate = reformatDate(activity['date']);
            let distance = reformatDistance(activity['distance']);
            let workoutTime = reformatWorkoutLength(activity['workout_time']);
            let avgSpeed = reformatAvgSpeed(activity['distance'], activity['workout_time']);
            let elevationGain = reformatElevationGain(activity['elev_gain']);

            $(`#user-${athlete['id']}-col${activity['weekday']}`).replaceWith(
            `<td scope="row">
              <div class="btn-group" role="group" aria-label="Basic example">
                <button type="button" class="activity-data btn btn-light" id="${activity['strava_activity_id']}" 
                  data-container="body" [dynamicPosition="false" data-toggle="popover" data-trigger="hover click" data-placement="bottom"
                  >${distance}</button>
                <button type="button" class="comment btn btn-light" id="${activity['strava_activity_id']}" data-toggle="modal" data-target="#comment-modal"><img class="comment" src="/static/img/chat-left-text-fill.svg" width="15px"></button>
              </div>
            </td>`);
            
            weekMileage += activity['distance'];
            let weekMileageRounded = reformatDistance(weekMileage);
            $(`#user-${athlete['id']}-col8`).replaceWith(
              `<td scope="row" id="user-${athlete['id']}-col8">
                <button class="activity-data btn btn-warning" disabled>${weekMileageRounded}</button>
              </td>`);

            if (activity.hasOwnProperty("splits")) {

              let activitySplits = activity['splits'];
              console.log(activitySplits)
              let splits = []

              for (let key of Object.keys(activitySplits)) {
                // let splits = $('.splits');
                // console.log(splits)
                let split = `${parseInt(key)+1}` + " | " + reformatAvgSpeed(activitySplits[key].distance, activitySplits[key].moving_time)
                // let splitDistance = reformatDistance(activitySplits[key].distance)
                // $(`#${activity['strava_activity_id']}`).data('bs.popover').element.dataset.content = ;
                splits.push(`<p class="split">${split}</p>`)
                // $(`<p class="splits">${splitPace}</p>`).insertAfter(".splits");
              };

              let splitsStr = splits.join('')


              $(`#${activity['strava_activity_id']}`).popover({ 
                            title : 'Activity Details',
                            container: 'body',
                            html: true,
                            content : `<div class=activity-details>
                                        Date: ${activityDate} <br/>
                                        Distance: ${distance} <br/>
                                        Time: ${workoutTime} <br/> 
                                        Average Pace: ${avgSpeed} <br/>
                                        Elevation Gain: ${elevationGain}<br/>
                                        <details>
                                          <summary>See Splits</summary>
                                          ${splitsStr}
                                        </details><br/>
                                      <form id="comment-form" action="/add-comment" method="POST">
                                        Comment:
                                        <textarea rows="1" class="form-control" id="comment-text" name="comment"></textarea><br/>
                                        <input id="activity-id" type="hidden" name="activity-id" value="${activity['strava_activity_id']}">
                                        <input type="submit" class="submit-comment btn btn-warning">
                                      </form>`
              }); 
            }

            else {
              $(`#${activity['strava_activity_id']}`).popover({ 
                            title : 'Activity Details',
                            container: 'body',
                            html: true,
                            content : `<div class=activity-details>
                                        Date: ${activityDate} <br/>
                                        Distance: ${distance} <br/>
                                        Time: ${workoutTime} <br/> 
                                        Average Pace: ${avgSpeed} <br/>
                                        Elevation Gain: ${elevationGain}<br/>
                                      <form id="comment-form" action="/add-comment" method="POST">
                                        Comment:
                                        <textarea rows="1" class="form-control" id="comment-text" name="comment"></textarea><br/>
                                        <input id="activity-id" type="hidden" name="activity-id" value="${activity['strava_activity_id']}">
                                        <input type="submit" class="submit-comment btn btn-warning">
                                      </form>`

              });
            };
          };  
        };
      };
      $(".comment").on('click', (evt) => {
        let activityID = evt.target.id;
        $.get(`/api/get-comments/${activityID}`, (response) => {
          const comments = response;
          $('#comment-modal').modal({
            backdrop: true
          });
          for (let comment of comments) {
            let comment_date = reformatDate(comment['date_utc'])
            $('.comment-modal-body').append(
              `<div class="col py-sm-2"><div class="rounded p-2 bg-light">
                <img src="${comment['author_prof_pic']}" width="55px" class="rounded-circle" align="right"/>
                <h6>${comment['author_name']} on ${comment_date}</h6><br/>
                ${comment['body']}<br/>
                </div></div>`
            );
          };
        });
      });
      $(".close-comment").on('click', (evt) => {
        evt.preventDefault();
          $('#comment-modal').modal({
            backdrop: true
          });
            $('.comment-modal-body').empty();
      });
    });
  });
};

display_dashboard()

function updatePagination(date) {

  date = new Date(date.toString())

  let previousWeek = new Date(date.getFullYear(), date.getMonth(), date.getDate() - 6);
  previousWeek = previousWeek.toISOString().split("T")[0]
  console.log('previous: ', previousWeek)

  let nextWeek = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 8);
  nextWeek = nextWeek.toISOString().split("T")[0]
  console.log('next: ', nextWeek)
  
  let currentDate = new Date()
  console.log('date is ', date)
  if (date.toISOString().split("T")[0] !== new Date(currentDate.getTime() - (currentDate.getTimezoneOffset() * 60000)).toISOString().split("T")[0]) {
    $('#previous-button').replaceWith(`<a href="/dashboard/${previousWeek}" type="button" class="previous btn btn-primary" id="previous-button"><span aria-hidden="true">&larr;</span> Older</a>`)
    $('#next-button').replaceWith(`<a href="/dashboard/${nextWeek}" type="button" class="next btn btn-primary" id="next-button"><span aria-hidden="true">&rarr;</span> Newer</a>`)
  }

  else {
    $('#previous-button').replaceWith(`<a href="/dashboard/${previousWeek}" type="button" class="previous btn btn-primary" id="previous-button"><span aria-hidden="true">&larr;</span> Older</a>`)
  };
};

  // if (window.location.pathname === "/dashboard") {
  //   let today = new Date();
  //   let previousWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
  //   previousWeek = previousWeek.toISOString().split("T")[0];
  //   // let letNewPath = window.location.pathname.replace(`/dashboard/${previousWeek}`);
  //   // console.log(letNewPath)
  // };

  // else {
  //   let currentWeek = window.location.pathname.split("/")[2];
  //   let year = 
  //   let month = 
  //   let day = 
  //   previousWeek = 
  // }

//   let activityID = evt.target.id;
//   $.get(`/api/get-comments/${activityID}`, (response) => {
//     const comments = response;
// display_dashboard()

// <a href="/dashboard/"

// function getWeek() {



//   let counter = 0
 
//   console.log('hi im inside the get previous week')

  // let today = new Date();
  // let previousWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7)
  // previousWeek = previousWeek.toISOString().split("T")[0]
//   $("#table-body").empty()
//   $("#next-button").removeAttr("hidden")
//   display_dashboard(previousWeek);
// };

// function getDashboardDate() {

//   let date = 
// }

function reformatDate(activityDate) {

  let formatDate = new Date(activityDate);
  let activityMonth = formatDate.getMonth()+1;
  let activityDay = formatDate.getDate();
  let activityYear = formatDate.getFullYear();
  let reformatDate = activityMonth + "-" + activityDay + "-" + activityYear;

  return reformatDate;
};

function reformatWorkoutLength(workoutTime) {

    let time = workoutTime / 3600;
    let hours = Math.floor(time);
    let minutes = Math.floor((time % 1) * 60);
    let seconds = Math.round((((time % 1) * 60) % 1) * 60);

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
  let miles = Math.floor(distance)
  let decimal = Math.round(distance % 1 * 100)

  if (decimal >= 100 && miles === 0) {
    let miles = decimal/100;
    return `${miles}.00 mi`
  }
  else if (miles >= 1 && decimal < 10) {
    return `${miles}.0${decimal} mi`;
  }
  else if (miles < 1 && decimal < 10) {
    return `0.0${decimal} mi`;
  }
  else if (miles < 1 && decimal >= 10) {
    return `0.${decimal} mi`;
  }
  return `${miles}.${decimal} mi`;
};

function reformatAvgSpeed(distance, workoutTime) {

  distance = distance * 0.000621371

  if (distance > 0) {

    let avgTime = (workoutTime / 60) / distance;
    let avgMinutes = Math.floor(avgTime);
    let avgSeconds = Math.round((avgTime % 1) * 60);

    if (avgSeconds < 10) {
      return `${avgMinutes}:0${avgSeconds}/mi`;
    }
    else {
      return `${avgMinutes}:${avgSeconds}/mi`;
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




