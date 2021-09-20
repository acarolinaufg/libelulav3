class BancoDeDados(db.Model):
    __tablename__ = 'libelula'
    data = db.Column(db.DateTime(), default= datetime.now ,primary_key = True)
    L_501 = db.Column(db.Numeric(10,2))
    L_503 = db.Column(db.Numeric(10,2))
    L_511C = db.Column(db.Numeric(10,2))
    L_511R = db.Column(db.Numeric(10,2))
    L_512 = db.Column(db.Numeric(10,2))
    L_521 = db.Column(db.Numeric(10,2))
    L_551 = db.Column(db.Numeric(10,2))
    L_561 = db.Column(db.Numeric(10,2))
    L_562 = db.Column(db.Numeric(10,2))
    brassagem = db.Column(db.Numeric(10,2))
    centrifuga = db.Column(db.Numeric(10,2))
    filtracao = db.Column(db.Numeric(10,2))

    def to_json(self):
        return{"data": self.data, "L_501": self.L_501, "L_503": self.L_503, "L_511C": self.L_511C,
                "L_511R": self.L_511R, "L_512": self.L_512, "L_521": self.L_521, "L_551": self.L_551,
                 "L_561": self.L_561, "L_562": self.L_562, "brassagem": self.brassagem, "centrifuga": self.centrifuga,
                 "filtracao": self.filtracao}


    #Cadastro
    def criar_dia():
        body = request.get_json()
        dia = BancoDeDados(L_501=body['L_501'],L_503=body['L_503'],L_511C=body['L_511C'],L_511R=body['L_511R'],
            L_512=body['L_512'],L_521=body['L_521'],L_551=body['L_551'],L_561=body['L_561'],L_562=body['L_562'],
            brassagem=body['brassagem'],centrifuga=body['centrifuga'],filtracao=body['filtracao'])

        db.session.add(dia)
        db.session.commit()

        return gera_response(200,"dia",dia_json)

    #Atualizar
    def atualizar_dia(data):
        objeto_banco = BancoDeDados.querry.filter_by(id=data).first()
        body = request.get_json()

        try:
            if('L_501'in body):
                objeto_banco.L_501 = body['L_501']
            if('L_503' in body):
                objeto_banco.L_503 = body['L_503']
            if('L_511C' in body):
                objeto_banco.L_511C = body['L_511C']
            if('L_511R' in body):
                objeto_banco.L_511R = body['L_511R'] 
            if('L_512' in body):
                objeto_banco.L_512 = body['L_512']
            if('L_521' in body):
                objeto_banco.L_521 = body['L_521']
            if('L_551' in body):
                objeto_banco.L_551 = body['L_551']
            if('L_561' in body):
                objeto_banco.L_561 = body['L_561']
            if('L_562' in body):
                objeto_banco.L_562 = body['L_562']
            if('brassagem' in body):
                objeto_banco.brassagem = body['brassagem']
            if('centrifuga' in body):
                objeto_banco.centrifuga = body['centrifuga']
            if('filtracao' in body):
                objeto_banco.filtracao = body['filtracao']  

            db.session.add(objeto_banco)
            db.session.commit()   
            return gera_response(200,'objeto_banco',objeto_banco.to_json(),'Atualizado com Sucesso')

    def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
        body = {}
        body[nome_do_conteudo] = conteudo

        if(mensagem):
            body["mensagem"] = mensagem
    
        return Response(json.dumps(body),status=status, mimetype="application/json")
