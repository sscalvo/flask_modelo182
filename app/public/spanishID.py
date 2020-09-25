import re
from wtforms.validators import ValidationError

#WTForms.validator para verificar (server-side) que nos han enviado un
#dni | nie | cif  válido

class SpanishID(object):
    def __init__(self, message=None):
        if not message:
            message = 'Debe ser un documento DNI, NIE, CIF válido'
        self.message = message

    def __call__(self, form, field):
        dni = field.data.upper()
        uletra = ["J", "A", "B", "C", "D", "E", "F", "G", "H", "I"] 
        #dni_regexp = '^[XYZ]?\d{5,8}[A-Z]$'
        dni_regexp = '^([0-9]{8}[A-Z])|[XYZ][0-9]{7}[A-Z]$'

        # NIF ?
        if re.match(dni_regexp, dni): 
            numero = dni[0:-1]
            numero = numero.replace('X', '0', 1)
            numero = numero.replace('Y', '1', 1)
            numero = numero.replace('Z', '2', 1)
            let = dni[-1]
            numero = int(numero) % 23
            letra = 'TRWAGMYFPDXBNJZSQVHLCKET'
            letra = letra[numero]
            if letra != let:
                raise ValidationError(self.message)
            #else:
                #return True
        # CIF ?
        else: 
            regular ='^[ABCDEFGHJKLMNPQRSUVW]\d\d\d\d\d\d\d[0-9,A-J]$'
            if not re.match(regular, dni): 
                raise ValidationError(self.message)
                  
            ultima = dni[-1] 
            par = sum([int(dni[x]) for x in [2,4,6]])
            non = 0
            for zz in [1, 3, 5, 7]:
                nn = 2* int(dni[zz])
                nn = 1 + (nn - 10) if nn > 9 else nn
                non = non + nn

            parcial = par + non
            control = (10 - ( parcial % 10))

            if (control==10): control=0	  	 
            if ((ultima == str(control)) or (ultima == uletra[control])):
                pass
                #return True
            else:
                raise ValidationError(self.message)
            
spanishID = SpanishID