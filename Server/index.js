var express = require('express');
var app = express();
var bodyParser = require('body-parser')
var multer = require('multer')
const cors = require('cors');
var upload = multer()
app.use((req, res, next) => {
   res.setHeader("Access-Control-Allow-Origin", "*");
   res.setHeader("Access-Control-Allow-Methods", "POST, GET, PUT");
   res.setHeader("Access-Control-Allow-Headers", "Content-Type");
   next();
 })
var routes = require('./route.js')

app.use('/installer/', routes)
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }));
app.use(upload.array()); 
app.use(cors())

app.set('view engine', 'pug')
app.set('views', './views')

app.get('/', function(req, res){
   res.send("Testing!!!");
});

app.listen(8000);