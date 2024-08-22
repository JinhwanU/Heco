// 지도 베이스

var infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
var mapContainer = document.getElementById("map");
var mapOption = {
  center: new kakao.map.LatLng(37.566826, 126.9786567),
  level: 3,
};

var map = new kakao.maps.Map(mapContainer, mapOption);

// 장소 검색

var ps = new kakao.maps.services.Places(); // 객체 생성
ps.keywordSearch("헬스장", placesSearchB); // 키워드 입력

function placesSearchB(data, status, pagination) {
  if (status === kakao.maps.services.Status.OK) {
    var bounds = new kakao.maps.LatLngBounds();

    for (var i = 0; i < data.length; i++) {
      displayMarker(data[i]);
      bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
    }

    map.setBounds(bounds);
  }
}

// Geolocation

if (navigator.geolocation) {
  // Geolocation 사용이 가능 할 때
  navigator.geolocation.getCurrentPosition(function (position) {
    var lat = position.coords.latitude; // 위도
    var lon = position.coords.longitude; // 경도

    var onPosition = new kakao.maps.LatLng(lat, lon); // 현재 위치 좌표 생성
    console.log("현재 위치는: ", onPosition);

    // displayMarker(onPosition, message);
  });
} else {
  // Geolocation 사용이 불가능 할 때
  var onPosition = new kakao.maps.LatLng(37.566826, 126.9786567);
  var message = "<div>Geolocation을 사용 할 수 없습니다.</div>";

  // displayMarker(onPosition, message);
}

// 지도에 표시

function displayMarker(place) {
  var marker = new kakao.maps.Marker({
    map: map,
    position: new kakao.maps.LatLng(place.y, place.x),
  });

  kakao.maps.event.addListener(marker, "click", function () {
    infowindow.setContent(
      '<div style="padding:5px;font-size:12px;">' + place.place_name + "</div>"
    );
    infowindow.open(map, marker);
  });
}

map.setCenter(onPosition); // 중심좌표 설정
