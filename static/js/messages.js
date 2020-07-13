"use strict";

function displayIncomingComments() {
  $.get("/get-incoming-comments", (response) => {
    const comments = response;
    // console.log(comments.length)

    for (let comment of comments) {
      let activityDate = reformatDate(comment["activity_date"]);
      let activityDistance = reformatDistance(comment["activity_distance"]);
      $(".received").append(
        `<div class="incoming-comment">
            <div class="col py-sm-2"><div class="rounded p-2 bg-light" class="comment-stream" id="comment-${comment["id"]}">
            <img src="${comment["author_prof_pic"]}" width="50px" class="rounded-circle" align="right"/>
            <div class="message-subject">From: ${comment["author_name"]}</div>
            <div class="message-subject">Run Details: ${activityDistance} on ${activityDate}</div><br>
            <div>${comment["body"]}</div>
            </div></div>
          </div>`
      );
    }
  });
}

displayIncomingComments();

function displayOutgoingComments() {
  $.get("/get-outgoing-comments", (response) => {
    const comments = response;
    console.log(comments.length);

    for (let comment of comments) {
      let activityDate = reformatDate(comment["activity_date"]);
      let activityDistance = reformatDistance(comment["activity_distance"]);
      $(".sent").append(
        `<div class="outgoing-comment">
            <div class="col py-sm-2"><div class="rounded p-2 bg-light" class="comment-stream" id="comment-${comment["id"]}">
            <img src="${comment["recipient_prof_pic"]}" width="50px" class="rounded-circle" align="right"/>
            <div class="message-subject">To: ${comment["recipient_name"]}</div>
            <div class="message-subject">Run Details: ${activityDistance} on ${activityDate}</div><br>
            <div>${comment["body"]}</div>
            </div></div>
          </div>`
      );
    }
  });
}

displayOutgoingComments();

function reformatDate(commentDate) {
  let formatDate = new Date(commentDate);
  let activityMonth = formatDate.getMonth() + 1;
  let activityDay = formatDate.getDate();
  let activityYear = formatDate.getFullYear();
  let reformatDate = activityMonth + "-" + activityDay + "-" + activityYear;

  return reformatDate;
}

function reformatDistance(distance) {
  distance = distance * 0.000621371;
  console.log(distance);
  let miles = Math.floor(distance);
  console.log(miles);
  let decimal = Math.round((distance % 1) * 100);
  console.log(decimal);
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
