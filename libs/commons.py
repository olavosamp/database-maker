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
            'gaio', # Gaiola de passarinho

            'corr', # Corrosão
            'ente', # Enterramento do duto
            'trin', # Trincheira
            'alte', # Alteração no duto, podendo não ser dano
            'cruz', # Cruzamento
            'flan', # Flange
            'garr', # Garra
            'asso'  # Assoreamento
            ]

tuboCode = 0            # Ordinal class codes DESATUALIZADO
nadaCode = 1
confCode = 2

tuboSpCode = [1, 0, 0]  # Orthogonal class codes DESATUALIZADO
nadaSpCode = [0, 1, 0]
confSpCode = [0, 0, 1]

# Videos of the following formats are found in the data source
videoFormats = ['wmv', 'mpg', 'vob', 'avi', ]

# SSIM comparison threshold
ssimLim = 0.600
