var express = require("express");
var app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.all('/', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
 });

app.post("/interactions", (req, res) => {
	res.json({'type': 1});
	console.log(req, req.body)
});
app.get("/interactions", (req, res) => {
	res.json({'type': 1});
});

app.listen(5000);
