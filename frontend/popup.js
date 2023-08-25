// popup.js

// Function to fetch the current tab's URL
function getCurrentTabUrl(callback) {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, function (tabs) {
    var url = tabs[0].url;
    callback(url);
  });
}

// Handle the button click event
document
  .getElementById("fetchUrlButton")
  .addEventListener("click", async function () {
    try {
      const url = await getCurrentTabUrlPromise();

      if (isYouTubeLink(url)) {
        document.getElementById("loremText").style.display = "none";
        document.getElementById("urlDisplay").textContent = "Loading...";
        sendDataToBackend(url); // Send the URL to the backend
        document.getElementById("fetchUrlButton").style.display = "none"; // Hide the Fetch button
        document.getElementById("exitButton").style.display = "block"; // Show the Exit button
        document.getElementById("urlDisplay").classList.add("processed");
      } else {
        alert("This is not a YouTube link.");
        window.close();
      }
    } catch (error) {
      console.error("Error fetching URL:", error);
      document.getElementById("urlDisplay").textContent = "Error fetching URL";
    }
  });
document.getElementById("exitButton").addEventListener("click", function () {
  window.close(); // Close the popup
});
async function sendDataToBackend(url) {
  try {
    const response = await fetch("http://127.0.0.1:5000/send-url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url }),
    });
    const responseData = await response.json();
    console.log("Backend response:", responseData);

    // Display the processed URL from the backend response
    if (responseData.processed_url) {
      document.getElementById("urlDisplay").textContent =
        "Summary: " + responseData.processed_url;
    }
  } catch (error) {
    console.error("Error sending data to backend:", error);
  }
}
// Promisified version of getCurrentTabUrl
function getCurrentTabUrlPromise() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query(
      { active: true, lastFocusedWindow: true },
      function (tabs) {
        if (tabs.length > 0) {
          resolve(tabs[0].url);
        } else {
          reject(new Error("No active tab found."));
        }
      }
    );
  });
}

// Function to check if a URL is a YouTube link
function isYouTubeLink(url) {
  return url.includes("youtube.com") || url.includes("youtu.be");
}
