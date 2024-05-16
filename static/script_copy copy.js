// Tambahkan ini ke file script_copy.js Anda
document.addEventListener("DOMContentLoaded", () => {
  const yesButtons = document.querySelectorAll(".btn-yes");
  const noButtons = document.querySelectorAll(".btn-no");

  function handleClick(event) {
      const button = event.currentTarget;
      const siblings = button.parentNode.children;

      // Remove .btn-active class from all siblings
      Array.from(siblings).forEach(sibling => {
          sibling.classList.remove("btn-active");
      });

      // Add .btn-active class to the clicked button
      button.classList.add("btn-active");
  }

  yesButtons.forEach(button => {
      button.addEventListener("click", handleClick);
  });

  noButtons.forEach(button => {
      button.addEventListener("click", handleClick);
  });
});
