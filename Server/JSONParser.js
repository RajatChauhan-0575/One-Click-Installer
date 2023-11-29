const fs = require('fs')

class JSONParser
{
    constructor(filePath)
    {
        if (JSONParser.instance)
        {
            return JSONParser.instance;
        }

        this.filePath = this.filePath
        this.dataObject = JSON.parse(fs.readFileSync(filePath))
        JSONParser.instance = this
    }

    static getInstance(filePath)
    {
        if (!JSONParser.instance)
        {
            JSONParser.instance = new JSONParser(filePath)
        }

        return JSONParser.instance
    }

    getTeams()
    {
        return Object.keys(this.dataObject)
    }

    getSoftwareWithDetails(team)
    {
        return this.dataObject[team]
    }

    fetchData(team)
    {
        return this.dataObject.team
    }
}

module.exports = JSONParser;