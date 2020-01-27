const days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"];

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
    const randomDelayTime = 1 + Math.random() * 5;
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
  element.classList.remove("container-row-detail-red");
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

    let startDate = dateFromUTC(data.startDate);
    let startDateTime = startDate.getTime();
    let endDate = dateFromUTC(data.endDate);
    let endDateTime = endDate.getTime();
    let daysUntil = daysBetweenDates(startDate, now);


    let hours = startDate.getHours();
    let hourString = formattedHours(hours);
    let suffix = hours > 12 ? "pm" : "am";
    let min = startDate.getMinutes();
    let minString = min == 0 ? "" : ":" + paddedStringForNum(min);



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
    } else if (now.getDate() == startDate.getDate()) {
      let suffix = startDate.getHours() > 12 ? "PM" : "AM";
      element.innerHTML =
        "" +
        formattedHours(startDate.getHours()) +
        ":" +
        paddedStringForNum(startDate.getMinutes()) +
        " " +
        suffix;
      updateContainerRowDetailColor(element, "container-row-detail-grey-blue");
    } else if (daysUntil < 7) {
      element.innerHTML = days[startDate.getDay()];
      updateContainerRowDetailColor(element, "container-row-detail-grey");
    } else {
      element.innerHTML = "" + (startDate.getMonth() + 1) + "/" + startDate.getDate();
      updateContainerRowDetailColor(element, "container-row-detail-grey");
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

function lastfmRowClicked(element_id) {
  element = document.getElementById(element_id);
  let metadata = element.dataset;
  let song = metadata.name;
  let artist = metadata.artist;
  let xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    "/spotify/play_track?track_name=" +
    song +
    "&artist=" +
    artist,
    true
  );
  xhr.onreadystatechange = function () {
    if (this.readyState != 4) return;
    console.log(this.status);
    console.log(this.response);
    
    if (this.status == 200) {

    } else {
    }
  };
  xhr.send();
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
  let metadata = document.getElementById("now-playing-metadata");

  let songElement = document.getElementById("now-playing-song")
  let playlistElement = document.getElementById("now-playing-playlist")
  let imageElement = document.getElementById("now-playing-image");
  let buttonElement = document.getElementById("spotify-playlist-selection-button")
  let imageContainer = document.getElementById("now-playing-image-container");

  let xhr = new XMLHttpRequest();
  xhr.open("GET", "/spotify/now_playing", true);
  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return;

    let response = JSON.parse(this.responseText);
    if (this.status == 200 && "tn" in response && response["tn"] != undefined) {
      
      if (
        metadata.dataset.trackUri != response["turi"] ||
        metadata.dataset.playlistUri != response["puri"]
      ) {
        buttonElement.innerHTML = "ADD";
      }

      songElement.innerHTML = response["tn"];
      playlistElement.innerHTML = response["pn"];

      metadata.dataset.trackUri = response["turi"];
      metadata.dataset.playlistUri = response["puri"];

      imageElement.src = "/spotify/now_playing.jpeg?destination=" + imageElement.dataset.destination;
      imageElement.style.visibility = "visible";
      imageContainer.style.backgroundColor = "red";
    } else {
      songElement.innerHTML = "-";
      playlistElement.innerHTML = "-";

      metadata.dataset.trackUri = "";
      metadata.dataset.playlistUri = "";

      imageElement.src = "/spotify/now_playing.jpeg";
      imageElement.style.visibility = "hidden";
      imageContainer.style.backgroundColor = "rgb(32, 32, 32)";
    }
  };
  xhr.send();
}

function colorForAmount(element, amount) {
  if (amount > 80) {
    updateContainerRowDetailColor(element, "container-row-detail-red");
  } else if (amount > 70) {
    updateContainerRowDetailColor(element, "container-row-detail-blue");
  } else if (amount > 60) {
    updateContainerRowDetailColor(element, "container-row-detail-grey-blue");
  } else if (amount > 30) {
    updateContainerRowDetailColor(element, "container-row-detail-grey");
  } else {
    updateContainerRowDetailColor(element, "container-row-detail-green");
  }
}

function getMonitorUpdate() {
  let cpuElement = document.getElementById("monitor-cpu")
  let memoryElement = document.getElementById("monitor-memory")
  let batteryElement = document.getElementById("monitor-battery")

  let xhr = new XMLHttpRequest();
  xhr.open("GET", "/monitor/now", true);
  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return;

    let response = JSON.parse(this.responseText);
    if (this.status == 200) {
      let cpu = response['cpu']
      cpuElement.innerHTML = cpu + '%';
      colorForAmount(cpuElement, cpu);

      let mem = response['mem']
      memoryElement.innerHTML = mem + '%';
      colorForAmount(memoryElement, mem)

      let bat = response['bat-l']
      batteryElement.innerHTML = bat + '%';
      colorForAmount(batteryElement, 1 - bat)
    }
  };
  xhr.send();
  setTimeout(function() { getMonitorUpdate(); }, 2000 + (Math.random() * 5000));
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

function updateStocks() {
  let xhr = new XMLHttpRequest();
  xhr.open("GET", "/stocks/now", true);
  xhr.onreadystatechange = function() {
    if (this.readyState != 4) return;

    let response = JSON.parse(this.responseText);
    let responseDict = {}
    for (let item of response) {
      responseDict[item['name']] = item['percent']
    }
    if (this.status == 200) {
      let elements = document.getElementsByClassName('stock-detail')
      for (let element of elements) {
        let symbol = element.dataset.symbol
        let percent = responseDict[symbol]
        element.innerHTML = percent
        if (percent[0] == '-') {
          updateContainerRowDetailColor(element, "container-row-detail-red");
        } else {
          updateContainerRowDetailColor(element, "container-row-detail-green");
        }
      }
    }
  };
  xhr.send();
  setTimeout(function() { updateStocks(); }, 4000 + (Math.random() * 5000));
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
  setInterval(updateWeather, 1000 * 60 * 30);

  spotifyGetNowPlaying();
  setInterval(spotifyGetNowPlaying, 2000);

  getMonitorUpdate();
  updateStocks();

  windowResized();
  window.onresize = windowResized;
}
