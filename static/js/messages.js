"use strict";

function displayMessages() {

  $.get('/get-incoming-comments', (response) => {
      const comments = response;
      console.log(comments.length)

      for (let comment of comments) {
        console.log(comment['author_prof_pic'])
        let commentDate = reformatDate(comment['activity_date'])
        let activityDistance = reformatDistance(comment['activity_distance'])
        $('.inbox').append(
          `<button type="button" class="incoming-message list-group-item list-group-item-action">
            <div class="col py-sm-2"><div class="rounded p-2 bg-light" class="comment-stream" id="comment-${comment['id']}">
            <img src="${comment['author_prof_pic']}" width="50px" class="rounded-circle" align="right"/>
            <div class="message-subject">Subject: ${activityDistance} run on ${commentDate}</div>
            <div>${comment['author_name']}</div>
            <div>${comment['body']}</div>
            </div></div>
          </button>`)
      };
  });
};

displayMessages()

function reformatDate(commentDate) {

  let formatDate = new Date(commentDate);
  let activityMonth = formatDate.getMonth()+1;
  let activityDay = formatDate.getDate();
  let activityYear = formatDate.getFullYear();
  let reformatDate = activityMonth + "-" + activityDay + "-" + activityYear;

  return reformatDate;
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