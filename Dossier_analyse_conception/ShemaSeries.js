{
    $jsonSchema:{
        bsonType: "object",
        title : "Serie",
        required: [
            "nom",
            "mots",
        ],
        properties:{
            "nom" : {
                bsonType : "string"
            },
            // "mots": {
            //     bsonType:"array",
            //     items:{
            //         bsonType:"object",
            //         required : ["mot","poid"],
            //         properties: { 
            //             "mot" : {
            //                 bsonType : "string"
            //             },
            //             "poid" : {
            //                 bsonType : "double"
            //             }
            //         }
            //     }
            // },
            "synopsis" : {
                bsonType : "string"
            },
            "image" : {
                bsonType : "string",
            },
            "saisons" : {
                bsonType: "array",
                items:{
                    bsonType: "object",
                    required: [
                        "nom",
                        "episodes"
                    ],
                    properties:{
                        "nom" : {
                            bsonType : "string"
                        },
                        "episodes": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "required": ["nom", "episode"],
                                "properties": {
                                    "nom": {
                                        "bsonType": "string"
                                    },
                                    "episode": {
                                        "bsonType": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}