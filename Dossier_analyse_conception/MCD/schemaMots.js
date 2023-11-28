{
    $jsonSchema: {
      bsonType: 'object',
      title: 'Mots_Series',
      required: [
        'mot',
        'series'
      ],
      properties: {
        mot: {
          bsonType: 'string'
        },
        series: {
          bsonType: 'array',
          items: {
            bsonType: 'object',
            required: [
              'titre',
              'poids'
            ],
            properties: {
              titre: {
                bsonType: 'string'
              },
              poids: {
                bsonType: 'double'
              }
            }
          }
        }
      }
    }
  }