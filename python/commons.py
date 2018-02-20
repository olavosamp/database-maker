import dirs

tuboCode = 0            # Ordinal class code
nadaCode = 1
confCode = 2

tuboSpCode = [1, 0, 0]  # Maximally sparse class code
nadaSpCode = [0, 1, 0]
confSpCode = [0, 0, 1]

# String class codes used in csv files
classes = [ 'tubo', # Duto
            'nada', # Nada
            'conf', # Confuso
            'repr', # Reparo
            'dano', # Dano
            'loop', # Loop
            'corc', # Corcova
            'torc', # Torção
            'ondl', # Ondulação
            'gaio'  # Gaiola de passarinho
            ]

# Videos of the following formats are found in the data source
videoFormats = ['wmv', 'mpg', 'vob', 'avi']

# SSIM comparison threshold
ssimLim = 0.600
