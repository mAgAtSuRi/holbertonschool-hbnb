/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
  });


fetch("header.html")
  .then(response => response.text())
  .then(data => {
  document.getElementById("header-container").innerHTML = data;
  });


fetch("footer.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("footer-container").innerHTML = data
    });
