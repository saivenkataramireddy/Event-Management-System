function total_events_view() {
    document.querySelector(".total_event").style.display = "block";
    document.querySelector(".total_users").style.display = "none";
}

function total_users_view() {
    document.querySelector(".total_users").style.display = "block";
    document.querySelector(".total_event").style.display = "none";
}

function form_close() {
    document.querySelector(".total_event").style.display = "none";
    document.querySelector(".add_event").style.display = "none";
}
function add_event() {
    document.querySelector(".add_event").style.display = "block";
}

function event_edit(id, name, description, budget, date, location) {
    document.querySelector(".event_editing").style.display = "block";
    document.getElementById("edit_name").value = name;
    document.getElementById("edit_description").value = description;
    document.getElementById("edit_budget").value = budget;
    document.getElementById("edit_date").value = date;
    document.getElementById("edit_location").value = location;
    document.getElementById("editForm").action = `/edit_event/${id}/`;
}
function form_close2() {
    document.querySelector(".total_users").style.display = "none";
}

function form_close3() {
    document.querySelector(".event_editing").style.display = "none";
}
function confirmDelete() {
    return confirm("Are you sure you want to delete this event?");
}

function user_edit(id, name, password, address, phone) {
    document.querySelector('.user_edit_form').style.display = 'block';
    document.querySelector('#edit_username').value = name;
    document.querySelector('#edit_password').value = password;
    document.querySelector('#edit_address').value = address;
    document.querySelector('#edit_phone').value = phone;
    document.querySelector('#editUserForm').action = `/edit_user/${id}/`;
}

function form_close4(){
    document.querySelector(".user_edit_form").style.display="none"
}

function user_dash(){
    document.querySelector(".our_events").style.display="block"
}
function form_close5(){
    document.querySelector(".our_events").style.display="none"
}

function edit_balance(){
    document.querySelector(".event_balance").style.display="block"
}
