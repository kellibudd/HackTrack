"use strict";

import { reformatDate, reformatDistance } from "./dashboard.js";

function displayIncomingComments() {
  $.get("/get-incoming-comments", (response) => {
    const comments = response;

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
