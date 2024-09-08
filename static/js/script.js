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

function closeProfilePopuo(){
  document.getElementById('popupProfile').style.display = 'none';
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

function openEditCategory(categoryId, categoryName) {
  document.getElementById('Ecategory-id').value = categoryId;
  document.getElementById('Ecategory-name').value = categoryName;
  document.getElementById('editCategoryModal').style.display = 'block';
  document.getElementById('modalOverlay').style.display = 'block';
}

function closeEditCategory() {
  document.getElementById('editCategoryModal').style.display = 'none';
}

function openEditItem(itemID, itemName, itemPrice,itemDiscreption, itemCategory) {
  document.getElementById('Eitem-id').value = itemID;
  document.getElementById('Eitem-name').value = itemName;
  document.getElementById('Eitem-price').value = itemPrice;
  document.getElementById('Eitem-description').value = itemDiscreption;
  document.getElementById('Eitem-category').value = itemCategory;
  document.getElementById('popupEditItem').style.display = 'block';
}

function closeEditItem() {
  document.getElementById('popupEditItem').style.display = 'none';
}

function displayFileName(input) {
  const fileLabel = document.getElementById('fileLabel');
  const fileName = input.files[0] ? input.files[0].name : '- please choose an image for the item';
  fileLabel.textContent = fileName;
}

function displayFileNameEdit(input) {
  const fileLabel = document.getElementById('custom-fileInput');
  const fileName = input.files[0] ? input.files[0].name : '- please choose an image for the item';
  fileLabel.textContent = fileName;
}


// -------------------profile image js--------------------------------------
// function previewImage(event) {
//   const file = event.target.files[0];
//   const reader = new FileReader();

//   reader.onload = function(e) {
//       document.getElementById('profilePicture').src = e.target.result;
//   }

//   if (file) {
//       reader.readAsDataURL(file);
//   }
// }
