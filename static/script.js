var socket = io();
var page = 1;

function mark(search, string) {
  if (search.length != 0) {
    var regexp = new RegExp(search, "gi");
    var match = [...string.matchAll(regexp)];
    for (let i = 0; i < match.length; i++) {
      // Add a unique string to prevent wrong replace.
      string = string.replace(match[i], "TVDB" + i);
    }
    for (let i = 0; i < match.length; i++) {
      string = string.replace("TVDB" + i, "<mark>" + match[i] + "</mark>");
    }
    return string;
  } else {
    return string;
  }
}

function search() {
  var screener = document.getElementById("screener").value;
  var query = document.getElementById("search").value;
  socket.emit("search_event", {
    screener: screener,
    query: query,
    page: page,
  });
  socket.on("response", (data) => {
    var compressed = data["r"];
    var res = JSON.parse(
      pako.inflate(compressed, {
        to: "string",
      })
    );
    var res_html = "";
    for (let i = 0; i < res.length; i++) {
      res_html =
        res_html +
        "<tr><td>" +
        res[i][0] +
        "</td><td>" +
        mark(query, res[i][1]) +
        "</td><td>" +
        mark(query, res[i][2]) +
        "</td><td>" +
        mark(query, res[i][3]) +
        "</td></tr>";
    }
    document.getElementById("result").innerHTML = res_html;
  });
}

function set_page(n) {
  page = Number(n);
  chg_page(0);
}

function chg_page(n) {
  page = page + n;
  if (page < 1) {
    page = 1;
  }
  document.getElementById("page").value = page;
  search();
}
