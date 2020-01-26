const days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"];
const fullDays = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday"
];
const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

function paddedStringForNum(num) {
  if (num < 10) {
    return "0" + num;
  } else {
    return num;
  }
}

function daysBetweenDates(d1, d2) {
  var diff = Math.abs(d1.getTime() - d2.getTime());
  return diff / (1000 * 60 * 60 * 24);
}

function suffixForDay(d) {
  if (d > 3 && d < 21) return "th";
  switch (d % 10) {
    case 1:
      return "st";
    case 2:
      return "nd";
    case 3:
      return "rd";
    default:
      return "th";
  }
}

function dateFromUTC(utc) {
  var d = new Date(0);
  d.setUTCSeconds(utc);
  return d;
}

function formattedHours(hours) {
  return "" + (hours > 12 ? hours % 12 : hours);
}

function configureNameAnimations() {
  const titleLetters = "andrew".split("");
  for (const letter of titleLetters) {
    const element = document.getElementById("today-title-" + letter);
    const randomTime = 1 + Math.random() * 8;
    element.style.setProperty("--animation-time", randomTime + "s");
    const randomDelayTime = 1 + Math.random() * 10;
    element.style.setProperty("--animation-delay", randomDelayTime + "s");
    const randomOpacity = 0.2 + Math.random() * 0.4;
    element.style.setProperty("--fade-opacity", randomOpacity);
  }
}

function updateCountdownComponent(id, date) {
  const now = new Date().getTime();
  const distance = date - now;

  const days = Math.floor(distance / (1000 * 60 * 60 * 24));
  const hours = Math.floor(
    (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
  );
  const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((distance % (1000 * 60)) / 1000);

  const element = document.getElementById("countdown-" + id);
  element.getElementsByClassName(
    "color-countdown-days"
  )[0].innerHTML = paddedStringForNum(days);
  element.getElementsByClassName(
    "color-countdown-hours"
  )[0].innerHTML = paddedStringForNum(hours);
  element.getElementsByClassName(
    "color-countdown-min"
  )[0].innerHTML = paddedStringForNum(minutes);
  element.getElementsByClassName(
    "color-countdown-sec"
  )[0].innerHTML = paddedStringForNum(seconds);
}

function updateContainerRowDetailColor(element, colorClass) {
  element.classList.remove("container-row-detail-green");
  element.classList.remove("container-row-detail-blue");
  element.classList.remove("container-row-detail-grey");
  element.classList.remove("container-row-detail-grey-blue");
  element.classList.add(colorClass);
}

function updateContainerRowDetails() {
  const now = new Date();
  const nowTime = now.getTime();
  const details = document.getElementsByClassName(
    "component-container-tableview-row-detail"
  );
  for (let element of details) {
    let data = element.dataset;
    if (data.type == null) {
      continue;
    }

    if (data.type == "countdown") {
      if (data.dateFormat == "hour-range") {
        let startDate = dateFromUTC(data.startDate);
        let startDateTime = startDate.getTime();
        let endDate = dateFromUTC(data.endDate);
        let endDateTime = endDate.getTime();

        if (nowTime - endDate > 0) {
          element.innerHTML = "DONE";
          updateContainerRowDetailColor(element, "container-row-detail-green");
        } else if (nowTime - startDate > 0) {
          let distance = endDateTime - nowTime;
          const minutes = Math.floor(distance / (1000 * 60));
          const seconds = Math.floor((distance % (1000 * 60)) / 1000);
          element.innerHTML =
            "T-" +
            paddedStringForNum(minutes) +
            ":" +
            paddedStringForNum(seconds);
          updateContainerRowDetailColor(element, "container-row-detail-blue");
        } else {
          let suffix = endDate.getHours() > 12 ? "PM" : "AM";
          element.innerHTML =
            "" +
            formattedHours(startDate.getHours()) +
            ":" +
            paddedStringForNum(startDate.getMinutes()) +
            " - " +
            formattedHours(endDate.getHours()) +
            ":" +
            paddedStringForNum(endDate.getMinutes()) +
            " " +
            suffix;
          updateContainerRowDetailColor(element, "container-row-detail-grey");
        }
      }
    } else if (data.type == "static") {
      let startDate = dateFromUTC(data.startDate);
      let startDateTime = startDate.getTime();
      let daysUntil = daysBetweenDates(startDate, now);

      const includeHour = data.dateFormat == "single-date-day-and-hour";

      let hours = startDate.getHours();
      let hourString = formattedHours(hours);
      let suffix = hours > 12 ? "pm" : "am";
      let min = startDate.getMinutes();
      let minString = min == 0 ? "" : ":" + paddedStringForNum(min);
      let prefix;
      if (startDate.getDate() == now.getDate()) {
        prefix = "Today";
        updateContainerRowDetailColor(element, "container-row-detail-blue");
      } else if (daysUntil < 1) {
        let dayNames = includeHour ? days : fullDays;
        prefix = dayNames[startDate.getDay()];
        updateContainerRowDetailColor(
          element,
          "container-row-detail-grey-blue"
        );
      } else if (daysUntil < 7) {
        let dayNames = includeHour ? days : fullDays;
        prefix = dayNames[startDate.getDay()];
        updateContainerRowDetailColor(element, "container-row-detail-grey");
      }

      if (typeof prefix == "undefined") {
        element.innerHTML =
          "" + (startDate.getMonth() + 1) + "/" + startDate.getDate();
        updateContainerRowDetailColor(element, "container-row-detail-grey");
      } else {
        if (includeHour) {
          element.innerHTML = prefix + ", " + hourString + minString + suffix;
        } else {
          element.innerHTML = prefix;
        }
      }
    }
  }
}

function updateTodayDate() {
  const now = new Date();
  const day = now.getDate();
  const hours = now.getHours();
  const min = now.getMinutes();
  const suffix = hours > 12 ? "PM" : "AM";

  document.getElementById("header-today-date").innerHTML =
    months[now.getMonth()] +
    " " +
    day +
    suffixForDay(day) +
    ", " +
    formattedHours(hours) +
    ":" +
    paddedStringForNum(min) +
    " " +
    suffix;
}

function updateWeather() {
  const elements = document.getElementsByClassName("weather-container");
  for (let element of elements) {
    let data = element.dataset;
    if (data == null) {
      continue;
    }
    let latitude = data.latitude;
    let longitude = data.longitude;
    let apiKey = data.apiKey;
    let url =
      "http://api.openweathermap.org/data/2.5/weather?units=imperial&lat=" +
      latitude +
      "&lon=" +
      longitude +
      "&APPID=" +
      apiKey;
    fetch(url)
      .then(response => {
        return response.json();
      })
      .then(json => {
        let place = json["name"];
        let temp = json["main"]["temp"];

        element.getElementsByClassName(
          "container-single-row-title"
        )[0].innerHTML = place;

        element.getElementsByClassName(
          "container-single-row-detail"
        )[0].innerHTML = "" + temp.toFixed(1) + "°";

        element.style.opacity = 1;
      })
      .catch(error => {
        element.getElementsByClassName(
          "container-single-row-detail"
        )[0].innerHTML = "-";
        console.error("Error:", error);
      });
  }
}

function spotifyPlaylistSelectionChanged() {
  document.getElementById("spotify-playlist-selection-button").innerHTML =
    "ADD";
}

function spotifyPlaylistAddButtonClicked() {
  document.getElementById("spotify-add-to-playlist").style.opacity = 0.5;

  let playlistURISelection = document.getElementById(
    "spotify-playlist-selection"
  );
  let addButton = document.getElementById("spotify-playlist-selection-button");

  let selectedPlaylist =
    playlistURISelection.options[playlistURISelection.selectedIndex];
  let nowPlayingTrackURI = document.getElementById("now-playing-metadata")
    .dataset.trackUri;

  console.log(selectedPlaylist);

  let xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    "/spotify/add_track?now_playing_track_uri=" +
      nowPlayingTrackURI +
      "&selected_playlist_uri=" +
      selectedPlaylist.value,
    true
  );
  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return;
    if (this.status == 200) {
      addButton.innerHTML = "ADDED";
    } else {
      addButton.innerHTML = "ERROR";
      setTimeout(function() {
        addButton.innerHTML = "ADD";
      }, 1000 * 5);
    }
    document.getElementById("spotify-add-to-playlist").style.opacity = 1;
  };
  xhr.send();
}

function spotifyPlaylistRemoveButtonClicked() {
  let metadata = document.getElementById("now-playing-metadata");
  let nowPlayingTrackURI = metadata.dataset.trackUri;
  let nowPlayingPlaylistURI = metadata.dataset.playlistUri;

  let xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    "/spotify/remove_track?now_playing_track_uri=" +
      nowPlayingTrackURI +
      "&now_playing_playlist_uri=" +
      nowPlayingPlaylistURI,
    true
  );
  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return;
    if (this.status == 200) {
      spotifyGetNowPlaying();
    }
  };
  xhr.send();
}

function spotifyGetNowPlaying() {
  let xhr = new XMLHttpRequest();
  xhr.open("GET", "/spotify/now_playing", true);
  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return;

    let response = JSON.parse(this.responseText);
    if (this.status == 200 && "tn" in response && response["tn"] != undefined) {
      let metadata = document.getElementById("now-playing-metadata");

      if (
        metadata.dataset.trackUri != response["turi"] ||
        metadata.dataset.playlistUri != response["puri"]
      ) {
        document.getElementById("spotify-playlist-selection-button").innerHTML =
          "ADD";
      }

      document.getElementById("now-playing-song").innerHTML = response["tn"];
      document.getElementById("now-playing-playlist").innerHTML =
        response["pn"];

      metadata.dataset.trackUri = response["turi"];
      metadata.dataset.playlistUri = response["puri"];

      let image = document.getElementById("now-playing-image");
      image.src = "/spotify/now_playing.jpeg";
      image.style.visibility = "visible";
      let imageContainer = document.getElementById(
        "now-playing-image-container"
      );
      imageContainer.style.backgroundColor = "red";
    } else {
      document.getElementById("now-playing-song").innerHTML = "Not Playing";
      document.getElementById("now-playing-playlist").innerHTML = "-";
      let metadata = document.getElementById("now-playing-metadata");
      metadata.dataset.trackUri = "";
      metadata.dataset.playlistUri = "";

      let image = document.getElementById("now-playing-image");
      image.src = "/spotify/now_playing.jpeg";
      image.style.visibility = "hidden";
      let imageContainer = document.getElementById(
        "now-playing-image-container"
      );
      imageContainer.style.backgroundColor = "rgb(32, 32, 32)";
    }
  };
  xhr.send();
}

function windowResized() {
  let normalMargin = 40;
  let width = Math.max(900, window.innerWidth);
  if (width < 1000) {
    let margin = normalMargin - (1000 - width) / 5;
    let topMargin = normalMargin / 2 - (1000 - width) / 20;
    document.documentElement.style.setProperty(
      "--column-margin",
      margin + "px"
    );
    document.documentElement.style.setProperty(
      "--top-column-margin",
      topMargin + "px"
    );
  } else {
    document.documentElement.style.setProperty(
      "--column-margin",
      normalMargin + "px"
    );
    document.documentElement.style.setProperty(
      "--top-column-margin",
      normalMargin / 2 + "px"
    );
  }
}

function start() {
  configureNameAnimations();

  let countdownID = "XYZ";
  let endDate = new Date("Nov 2, 2020 10:00").getTime();
  updateCountdownComponent(countdownID, endDate);
  setInterval(updateCountdownComponent.bind(null, countdownID, endDate), 1000);

  updateContainerRowDetails();
  setInterval(updateContainerRowDetails, 1000);

  updateTodayDate();
  setInterval(updateTodayDate, 1000);

  updateWeather();

  setInterval(spotifyGetNowPlaying, 1000);

  windowResized();
  window.onresize = windowResized;
}