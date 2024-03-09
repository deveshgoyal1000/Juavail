fetch("http://172.20.10.4:9999/avail")
.then(function(res){
  return res.json();
})
.then(function(data) {
  let day = document.querySelector("day")
  day.innerHTML = data.day;
  let lec = document.querySelector("lec")
  lec.innerHTML = data.lec;
  let time = document.querySelector("time")
  time.innerHTML = data.time;

  let cont = document.querySelector("main")
  var ans = "";
  for (let p of data.empty_rooms){
    ans += `<div class="box"><p>${p}</p></div>`;
  }
  console.log(ans);
  cont.innerHTML = ans;
});

