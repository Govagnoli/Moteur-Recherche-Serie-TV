{
    $jsonSchema: {
        bsonType: 'object',
        title: 'Utilisateur',
        required: [
            'identifiant',
            'mdp',
            'role'
        ],
        properties: {
            identifiant: {
                bsonType: 'string'
            },
            mdp: {
                bsonType: 'string'
            },
            role: {
                bsonType: 'array',
                'enum': [
                    'administration',
                    'utilisateur'
                ]
            },
            date_exp: {
                bsonType: 'string',
                pattern : '^[0-9]{2}\/[0-9]{2}$'
            },
            email: {
                bsonType: 'string',
                pattern : '^[0-9]{3}$'
            },
            cvc: {
                bsonType: 'string',
                pattern : '^[0-9]{2}\/[0-9]{2}$'
            },
            num_carte_bank: {
                bsonType: 'string',
                pattern : '^[0-9]{16}$'
            },
            adresse: {
                bsonType: 'string'
            },
            pays: {
                bsonType: 'string'
            }
        }
    }
}