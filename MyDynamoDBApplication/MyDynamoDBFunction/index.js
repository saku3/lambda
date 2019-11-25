"use strict";

exports.handler = (event, context, callback) => {
    if (event["body"]) {
        event = JSON.parse(event["body"]);
    }
    
    var AWS = require("aws-sdk");
    AWS.config.update({
      region: "ap-northeast-1",
    });
    
    var docClient = new AWS.DynamoDB.DocumentClient();
    
    var params = {
        TableName: event.table,
        Item: {
            "ID":  event.ID,
            "message": event.message
        }
    };
    
    docClient.put(params, function(err, data) {
        if (err) {
            callback(null, {
                statusCode: 200,
                headers: {"Content-type": "application/json"},
                body: JSON.stringify({
                    error: {
                        code: err.code,
                        message: err.message,
                    },
                }),
            });
        } else {
            callback(null, {
                statusCode: 200,
                headers: {"Content-type": "application/json"},
                body: JSON.stringify(data, null, 2),
            });
        }
        callback(err);
    });
};
