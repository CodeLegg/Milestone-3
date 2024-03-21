let sections = document.querySelectorAll("section");

window.onscroll = () => {
  sections.forEach((sec) => {
    let top = window.scrollY;
    let offset = sec.offsetTop - 150;
    let height = sec.offsetHeight;

    if (top >= offset && top < offset + height) {
      sec.classList.add("show-animate");
    } else {
      sec.classList.remove("show-animate");
    }
  });
};

document.addEventListener("DOMContentLoaded", function () {
  var deleteCommentModal = document.getElementById("deleteCommentModal");
  deleteCommentModal.addEventListener("show.bs.modal", function (event) {
    var button = event.relatedTarget;
    var commentId = button.getAttribute("data-comment-id");
    var deleteCommentForm = document.getElementById("deleteCommentForm");
    deleteCommentForm.action = "/comment/" + commentId + "/delete";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var deleteReplyModal = document.getElementById("deleteReplyModal");
  deleteReplyModal.addEventListener("show.bs.modal", function (event) {
    var button = event.relatedTarget;
    var replyId = button.getAttribute("data-reply-id");
    var deleteReplyForm = document.getElementById("deleteReplyForm");
    deleteReplyForm.action = "/comment/" + replyId + "/delete";
  });
});
