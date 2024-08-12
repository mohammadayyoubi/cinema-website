const container = document.querySelector(".container2");
const count = document.getElementById("count");
const total = document.getElementById("total");
const movieSelect = document.getElementById("movie2");
const bookingForm = document.getElementById("bookingForm");
const selectedSeatsInput = document.getElementById("selectedSeats");

// Initial ticket price
let ticketPrice = 1;

// Populate UI with selected seats from localStorage
function populateUI() {
  const selectedSeats = JSON.parse(localStorage.getItem("selectedSeats")) || [];
  selectedSeats.forEach(id => {
    const seat = document.getElementById(`seat${id}`);
    if (seat && !seat.classList.contains('sold')) {
      seat.classList.add("selected");
    }
  });
  updateSelectedCount();
}

// Update seat count and total price
function updateSelectedCount() {
  const selectedSeats = document.querySelectorAll(".row .seat.selected");
  const seatsIndex = [...selectedSeats].map(seat => seat.id.replace('seat', ''));
  const selectedSeatsCount = selectedSeats.length;
  count.innerText = selectedSeatsCount;
  total.innerText = selectedSeatsCount * ticketPrice;


}

// Movie select event listener
movieSelect.addEventListener("change", (e) => {
  ticketPrice = +e.target.value;
  setMovieData(e.target.selectedIndex, e.target.value);
  updateSelectedCount();
});

// Function to update the selected seats input field
function updateSelectedSeats() {
  const selectedSeats = Array.from(document.querySelectorAll('.seat.selected'))
    .map(seat => seat.id.replace('seat', ''));
  selectedSeatsInput.value = selectedSeats.join(',');
}

// Form submission event listener
bookingForm.addEventListener('submit', function () {
  // Update the hidden input with selected seats
  updateSelectedSeats();
  // Optionally handle any additional form validation here
});
function selectSeat(seatId) {
  const seatElement = document.getElementById(seatId);

  // Check if the seat is already selected
  if (!seatElement.classList.contains('sold')) {
    if (seatElement.classList.contains('selected')) {
      // Deselect the seat
      seatElement.classList.remove('selected');
      // Remove seatId from selectedSeats array
      updateSelectedCount();

    } else {
      // Select the seat
      seatElement.classList.add('selected');
      // Add seatId to selectedSeats array
      updateSelectedCount();

    }
  } else {
    alert('Seat is sold out!')
  }
}

function redirectToUrl(button) {
  const url = button.getAttribute('data-url');
  window.location.href = url;
}
function redirectTo(select) {
  var url = select.value;
  window.location.href = url;
}

// Initial setup
populateUI();
updateSelectedCount();



function toggle() {
  var blur = document.getElementById('movies');
  blur.classList.toggle('active');
  var popup = document.getElementById('popup');
  popup.classList.toggle('active');
}

function toggleEditButtons() {
  const buttons = document.querySelectorAll('.edit-delete-buttons');
  buttons.forEach(button => {
      button.style.display = button.style.display === 'none' ? 'block' : 'none';
  });
}
//////////////////////////////////////////Edit profile js ///////////////////////////

function openProfilePopup() {
  document.getElementById('popupProfile').style.display = 'block';
}


//////////////////////////// menu popups ////////////////////////////////
function openCategoryPopup() {
  document.getElementById('popupCategory').style.display = 'block';
}
function closeCategoryPopup() {
  document.getElementById('popupCategory').style.display = 'none';
}


function closeItemPopup() {
  document.getElementById('popupItem').style.display = 'none';
}

function openItemPopup() {
  document.getElementById('popupItem').style.display = 'block';
}

