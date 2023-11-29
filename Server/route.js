var express = require('express')
var router = express.Router()
var bodyParser = require('body-parser')
const JSONParser = require('./JSONParser')
const cors = require('cors');

parser = new JSONParser('DataBase/Download.json')
router.use(bodyParser.json())
router.use(cors())

router.get('/', function(req, res)
{
   res.send('Welcome!!!');
});

router.get('/teams', function(req, res)
{
	let teams = parser.getTeams()
	console.log('Sending all the teams details....')
    let teamsWithID = [];

    let i = 0;
    for (let i = 0; i < teams.length; i++)
    {
        let team = teams[i]
        let key = i + 1
        let ele = {}
        ele.id = key
        ele.name = team
        teamsWithID.push(ele)
    }

    let jsonTeams = {
        "teams": teamsWithID
    }

    res.send(jsonTeams)
});

router.post('/softList', function(req, res)
{
	let team = req.body
    let teamName = team.team
	let softList = parser.getSoftwareWithDetails(teamName)
    res.send(softList)
});

router.post('/targetMachine', function(req, res)
{
    let bod = req.body
    let ipAddress = bod.ip
    let port = bod.port

    let resp = "Connected to machine ip:" + ipAddress + " port:" + port;

    let response ={ 
        "status" : resp
    }
 
    console.log(response)
    res.send(response)
})

module.exports = router;