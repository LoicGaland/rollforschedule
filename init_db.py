from app import db, Table, Player, app

with app.app_context():
    db.drop_all()
    db.create_all()

    ldi = Table(
        title='Les Démons Intérieurs',
        description='La conclusion de l\'aventure des héros de Roquesaltes'
    )
    rnp = Table(
        title='Les Plaies Ouvertes',
        description='Cinq questeurs en quête de justice et de vengeance'
    )
    anathazerin = Table(
        title='Anathazerïn',
        description=(
            'La recherche d\'une cité ancestrale '
            'qui pourrait sauver le Mitan'
        )
    )
    weebland = Table(
        title='Weebland',
        description='Choo choo motherfucker!'
    )

    loic = Player(username="Loïc")
    sandra = Player(username="Sandra")
    william = Player(username="William")
    yohan = Player(username="Yohan")
    mathilde = Player(username="Mathilde")
    renise = Player(username="Renise")
    alexis = Player(username="Alexis")
    adrien = Player(username="Adrien")
    sergio = Player(username="Sergio")

    ldi.players.append(loic)
    ldi.players.append(sandra)
    ldi.players.append(william)
    ldi.players.append(yohan)
    ldi.players.append(mathilde)

    rnp.players.append(loic)
    rnp.players.append(sandra)
    rnp.players.append(william)
    rnp.players.append(yohan)
    rnp.players.append(renise)
    rnp.players.append(alexis)

    anathazerin.players.append(loic)
    anathazerin.players.append(alexis)
    anathazerin.players.append(sandra)

    weebland.players.append(loic)
    weebland.players.append(renise)
    weebland.players.append(alexis)
    weebland.players.append(adrien)
    weebland.players.append(sergio)


    db.session.add_all([ldi, rnp, anathazerin, weebland])
    db.session.add_all(
        [loic, sandra, william, yohan, mathilde, renise, alexis, adrien, sergio]
    )

    db.session.commit()
