class Tom:
    def __init__(self, tom):

        # Função construtora do objeto
        # Entrada: tom --> Tom da música que será gerada a escala
        # Saída: None --> O objeto é instanciado

        nomeModo = tom.split()
        self.nome = nomeModo[0]
        self.modo = nomeModo[1]

        escala = {
            'C': 65.40638,
            'C#': 69.295647,
            'D': 73.416199,
            'D#': 77.781746,
            'E': 82.406876,
            'F': 87.307053,
            'F#': 92.498604,
            'G': 97.998848,
            'G#': 103.82618,
            'A': 110,
            'A#': 116.540947,
            'B': 123.470818
        }

        self.frequencia = escala[self.nome]

    # -----------------------------------------------------------------------------------------------------------------------

    def get_frequencias(self):

        # Função para criar lista com as frequências das notas da escalas em 5 oitavas
        # Entrada: None --> O próprio objeto istanciado
        # Saída: Lista --> Lista com as frequências das notas musicais da escala

        escala = []
        escala_alt = []
        
        if self.modo == 'major':   
            escala.append(float(f'{self.frequencia:.3f}'))
            escala.append(float(f'{(self.frequencia * 2):.3f}'))
            escala.append(float(f'{(self.frequencia * 4):.3f}'))
            escala.append(float(f'{(self.frequencia * 8):.3f}'))
            escala.append(float(f'{(self.frequencia * 16):.3f}'))
            nota_inicial = self.frequencia
            
            for i in range(2):
                nota = nota_inicial * 1.1224618484
                escala.append(float(f'{nota:.3f}'))
                escala.append(float(f'{(nota * 2):.3f}'))
                escala.append(float(f'{(nota * 4):.3f}'))
                escala.append(float(f'{(nota * 8):.3f}'))
                escala.append(float(f'{(nota * 16):.3f}'))
                nota_inicial = nota

            nota = nota_inicial * 1.059463
            escala.append(float(f'{nota:.3f}'))
            escala.append(float(f'{(nota * 2):.3f}'))
            escala.append(float(f'{(nota * 4):.3f}'))
            escala.append(float(f'{(nota * 8):.3f}'))
            escala.append(float(f'{(nota * 16):.3f}'))
            nota_inicial = nota

            for i in range(3):
                nota = nota_inicial * 1.1224618484
                escala.append(float(f'{nota:.3f}'))
                escala.append(float(f'{(nota * 2):.3f}'))
                escala.append(float(f'{(nota * 4):.3f}'))
                escala.append(float(f'{(nota * 8):.3f}'))
                escala.append(float(f'{(nota * 16):.3f}'))
                nota_inicial = nota

        else:
            escala.append(float(f'{self.frequencia:.3f}'))
            escala.append(float(f'{(self.frequencia * 2):.3f}'))
            escala.append(float(f'{(self.frequencia * 4):.3f}'))
            escala.append(float(f'{(self.frequencia * 8):.3f}'))
            escala.append(float(f'{(self.frequencia * 16):.3f}'))
            nota_inicial = self.frequencia

            nota = nota_inicial * 1.1224618484
            escala.append(float(f'{nota:.3f}'))
            escala.append(float(f'{(nota * 2):.3f}'))
            escala.append(float(f'{(nota * 4):.3f}'))
            escala.append(float(f'{(nota * 8):.3f}'))
            escala.append(float(f'{(nota * 16):.3f}'))
            nota_inicial = nota

            nota = nota_inicial * 1.059463
            escala.append(float(f'{nota:.3f}'))
            escala.append(float(f'{(nota * 2):.3f}'))
            escala.append(float(f'{(nota * 4):.3f}'))
            escala.append(float(f'{(nota * 8):.3f}'))
            escala.append(float(f'{(nota * 16):.3f}'))
            nota_inicial = nota

            for i in range(2):
                nota = nota_inicial * 1.1224618484
                escala.append(float(f'{nota:.3f}'))
                escala.append(float(f'{(nota * 2):.3f}'))
                escala.append(float(f'{(nota * 4):.3f}'))
                escala.append(float(f'{(nota * 8):.3f}'))
                escala.append(float(f'{(nota * 16):.3f}'))
                nota_inicial = nota

            nota = nota_inicial * 1.059463
            escala.append(float(f'{nota:.3f}'))
            escala.append(float(f'{(nota * 2):.3f}'))
            escala.append(float(f'{(nota * 4):.3f}'))
            escala.append(float(f'{(nota * 8):.3f}'))
            escala.append(float(f'{(nota * 16):.3f}'))
            nota_inicial = nota

            nota = nota_inicial * 1.1224618484
            escala.append(float(f'{nota:.3f}'))
            escala.append(float(f'{(nota * 2):.3f}'))
            escala.append(float(f'{(nota * 4):.3f}'))
            escala.append(float(f'{(nota * 8):.3f}'))
            escala.append(float(f'{(nota * 16):.3f}'))
            nota_inicial = nota

        for nota in escala:
            escala_alt.append(int(nota))

        return escala_alt
    
    # -----------------------------------------------------------------------------------------------------------------------

    def get_nome(self):
        return str(self.nome) + str(self.modo)
