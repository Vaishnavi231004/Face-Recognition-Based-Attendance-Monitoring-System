// Function to capture a photo
function capturePhoto() {
    fetch("/capture_photo")
        .then(response => response.json())
        .then(data => alert(data.message || data.error))
        .catch(error => console.error("Error:", error));
  }

// Function to start real-time attendance
  function startRealTimeAttendance() {
    fetch("/start_attendance")
        .then(response => response.json())
        .then(data => alert(data.message || data.error))
        .catch(error => console.error("Error:", error));
  }
  
  
  // Function to download attendance CSV for the month
function downloadCSV() {
  const month = document.getElementById("attendanceMonth").value;
  if (!month) {
      alert("Please select a month before downloading.");
      return;
  }
  
  const url = `/download_csv?month=${encodeURIComponent(month)}`;
  const link = document.createElement("a");
  link.href = url;
  link.download = `Attendance_${month}.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Function to download attendance PDF for the month
function downloadPDF() {
  const month = document.getElementById("attendanceMonth").value;
  if (!month) {
      alert("Please select a month before downloading.");
      return;
  }
  
  const url = `/download_pdf?month=${encodeURIComponent(month)}`;
  const link = document.createElement("a");
  link.href = url;
  link.download = `Attendance_${month}.pdf`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}



  
  // Function to filter the timetable
  function filterTable() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let rows = document.querySelectorAll("#timetableTable tbody tr");
  
    rows.forEach(row => {
        let text = row.innerText.toLowerCase();
        row.style.display = text.includes(input) ? "" : "none";
    });
  }
  
  // Function to sort the timetable columns
  function sortTable(colIndex) {
    let table = document.getElementById("timetableTable");
    let rows = Array.from(table.rows).slice(1);
    let sorted = rows.sort((a, b) =>
        a.cells[colIndex].innerText.localeCompare(b.cells[colIndex].innerText)
    );
  
    sorted.forEach(row => table.appendChild(row));
  }
  
  // Highlight today's timetable row
  function highlightToday() {
    let today = new Date().toLocaleDateString("en-US", { weekday: "long" });
    let rows = document.querySelectorAll("#timetableTable tbody tr");
  
    rows.forEach(row => {
        if (row.cells[0].innerText === today) {
            row.classList.add("highlight");
        }
    });
  }
  
  
  
  
  
  // Attach event listeners to buttons
  document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("captureBtn").addEventListener("click", capturePhoto);
    document.getElementById("startCameraBtn").addEventListener("click", startRealTimeAttendance);
    document.getElementById("downloadCsvBtn").addEventListener("click", downloadCSV);
    document.getElementById("downloadPdfBtn").addEventListener("click", downloadPDF);
  
    // Highlight today's timetable row on load
    highlightToday();
  });