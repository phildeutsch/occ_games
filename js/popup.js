function myFunction() {
  swal({
    title: "Enter player",
    text: "Please enter the player name:",
    type: "input",
    showCancelButton: true,
    closeOnConfirm: false,
    animation: "pop",
    inputPlaceholder: "Write something"
  },
  function(inputValue){
    if (inputValue === false) return false;

    if (inputValue === "") {
      swal.showInputError("You need to enter a name!");
      return false
    }

    swal("Nice!", "Player added: " + inputValue, "success");
  })
}
