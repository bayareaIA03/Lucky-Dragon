function initMap() {
    // The location of restaurant
    const lucky_dragon = { lat: 33.86209776918847, lng: -84.59738277607032};
    const map = new google.maps.Map(document.getElementById("map"),{
      zoom: 17,
      center: lucky_dragon,
    });
    const marker = new google.maps.Marker({
      position: lucky_dragon,
      map: map,
    });
  }