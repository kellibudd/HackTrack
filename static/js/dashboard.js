"use strict";

let tableColumns = ["Athlete", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];
// let tableColumns = [" ", "Athlete", "Exercise", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Total"];

function generateTableHead(table) {
  for (let column of tableColumns) {
    let tableHeadRow = $("#head-row");
    tableHeadRow.append(`<th class="align-middle" id="${column}" scope="col">${column}</th>`);
  };
};

let table = $("#team-table");
generateTableHead(table);

function display_dashboard() {
  $.get('/get-team-data', (response) => {
    let athletes = response;

    let curr_date = new Date()
    let dateConverted = curr_date.toISOString()
    console.log(dateConverted)
    $.get(`/api/get-activity-data/${dateConverted}`, (response) => {
      let activities = response;

      for (let athlete of athletes) {
        let tbody = $("#table-body");
        let row = tbody.append(`<tr id="${athlete['id']}-row"></tr>`);
        row.append(`<td><img src="${athlete['prof_pic']}" width="60px" class="rounded-circle" align="left"/></td>`);
        row.append(`<td class="align-middle" scope="row">
                      <button class="activity-data btn btn-dark" disabled>${athlete['name']}</button>
                    </td>`);
        // let run = row.append(`<td id="run-exercise" scope="row">Run</td>`);
        // let crossTrain = row.append(`<tr id="xt-workout" scope="row">Cross Train</tr>`);

        for (let i of Array(9).keys()) {
          row.append(`<td id="user-${athlete['id']}-col${i+1}" scope="row"></td>`)
        };

        let weekMileage = 0

        for (let activity of activities) {
          
          if (activity['user_id'] === athlete['id'] && activity['exercise_type'] === "Run") {
            
            let activityDate = reformatDate(activity['date']);
            let distance = reformatDistance(activity['distance']);
            let workoutTime = reformatWorkoutLength(activity['workout_time']);
            let avgSpeed = reformatAvgSpeed(activity['distance'], activity['workout_time']);
            let elevationGain = reformatElevationGain(activity['elev_gain']);

            $(`#user-${athlete['id']}-col${activity['weekday']}`).replaceWith(
            `<td class="align-middle" scope="row">
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
              `<td class="align-middle" scope="row" id="user-${athlete['id']}-col8">
                <button class="activity-data btn btn-warning" disabled>${weekMileageRounded}</button>
              </td>`);

            $(".popover-div").append(`<p>Date: ${activityDate}</p><br/>
                                      Distance: ${distance} <br/>
                                      Time: ${workoutTime} <br/> 
                                      Average Pace: ${avgSpeed} <br/>
                                      Elevation Gain: ${elevationGain}<br/>
                                      <details>
                                        <summary class="splits-summary">See Splits</summary>
                                      </details><br/>
                                      <form id="comment-form" action="/add-comment" method="POST">
                                        Comment:
                                        <textarea rows="1" class="form-control" id="comment-text" name="comment"></textarea><br/>
                                        <input id="activity-id" type="hidden" name="activity-id" value="${activity['strava_activity_id']}">
                                        <input type="submit" class="submit-comment btn btn-warning">
                                      </form>`)

            if (activity.hasOwnProperty("splits")) {

              let activitySplits = activity['splits'];

              for (let key of Object.keys(activitySplits)) {
                $(".splits-summary").append(`<p>${activitySplits[key].average_speed}</p>`)
                console.log(activitySplits[key].average_speed)
              };
            };

            $(`#${activity['strava_activity_id']}`).popover({ 
              title : 'Details',
              container: 'body',
              html: true,
              content : $(".popover-div")
            });
          };  
        };
      };
      $(".comment").on('click', (evt) => {
        let activityID = evt.target.id;
        $.get(`/api/get-comments/${activityID}`, (response) => {
          console.log(response);
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
  if (decimal < 10) {
    return `${miles}.0${decimal}mi`;
  };
  return `${miles}.${decimal}mi`;
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




